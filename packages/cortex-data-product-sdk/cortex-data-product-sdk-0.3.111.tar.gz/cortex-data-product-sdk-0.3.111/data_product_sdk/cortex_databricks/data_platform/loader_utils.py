from collections.abc import Iterable, Callable
from typing import List

from pyparsing import Diagnostics
from data_product_sdk.cortex_databricks.data_platform.aws_utils import S3
from data_product_sdk.cortex_databricks.data_platform.databricks_utils import (
    reset_autoloader_checkpoint,
    __delete_checkpoint_location,
)
from data_product_sdk.cortex_databricks.data_platform.kafka_utils import (
    create_topics_if_not_exists,
    DEFAULT_BOOTSTRAP_SERVERS,
)
from data_product_sdk.cortex_databricks.data_platform.processing_utils import (
    process_dataframe,
)
from data_product_sdk.cortex_databricks.data_platform.profiling_utils import (
    calculate_profilling,
    get_link_table

)
from data_product_sdk.cortex_databricks.data_platform.schema_utils import (
    get_schema_from_s3,
)
from data_product_sdk.cortex_databricks.data_platform.spark_utils import (
    get_spark_session,
    ENVIRONMENT,
    check_table_exists,
    get_table_partitions,
    drop_table_duplicates,
    build_matching_sort_condition,
    set_comment_table

)
from delta.tables import DeltaTable
from pyspark.sql import SparkSession
from pyspark.sql.dataframe import DataFrame
from pyspark.sql.types import StructType
from data_product_sdk.databricks.spark import DatabricksSpark

import datetime
import json
import os
import re

LANDING_BUCKET = f"cortex-data-platform-landing-area-{ENVIRONMENT}"
BRONZE_BUCKET = f"cortex-databricks-bronze-{ENVIRONMENT}"
SILVER_BUCKET = f"cortex-databricks-silver-{ENVIRONMENT}"
GOLD_BUCKET = f"cortex-databricks-gold-{ENVIRONMENT}"
DIAMOND_BUCKET = f"cortex-databricks-diamond-{ENVIRONMENT}"

BRONZE_DB_NAME = f"cortex_databricks_bronze_{ENVIRONMENT}"
SILVER_DB_NAME = f"cortex_databricks_silver_{ENVIRONMENT}"
GOLD_DB_NAME = f"cortex_databricks_gold_{ENVIRONMENT}"
DIAMOND_DB_NAME = f"cortex_databricks_diamond_{ENVIRONMENT}"


def __verify_parameters(function):
    def wrapper(*args, **kwargs):
        insert_modes_avalables = ["append", "upsert", "overwrite"]
        insert_mode = kwargs.get("insert_mode", "append")
        if insert_mode in insert_modes_avalables:
            return function(*args, **kwargs)
        else:
            raise ValueError(
                f"Argument insert_mode is '{kwargs.get('insert_mode')}' but should be one of {insert_modes_avalables}"
            )

    return wrapper


def __get_partition_type(partition_value: str):
    try:
        datetime.datetime.strptime(partition_value, "%Y-%m-%d")
        return "date"
    except ValueError:
        return "string"


def __resolve_partition_columns(path: str):
    pattern = r"(\w+)=(.*?)\/"
    partitions = re.findall(pattern, path)
    partitions = {i[0]: __get_partition_type(i[1]) for i in partitions}

    return partitions


def __list_partition_columns(s3_path: str):
    s3_bucket, s3_key = S3.get_bucket_key_from_s3_url(s3_url=s3_path)
    s3_client = S3(bucket_name=s3_bucket)
    s3_files = s3_client.list_s3_files(prefix=s3_key)  # TODO: TRAZER APENAS AS PASTAS
    if not s3_files:
        raise FileNotFoundError(f'No files found in the provided path: "{s3_path}"')
    s3_files = (__resolve_partition_columns(i["Key"]) for i in s3_files)

    partitions = dict()
    for i in s3_files:
        for k, v in i.items():
            if partitions.get(k, v) != v:
                v = "string"
            partitions.update({k: v})

    return partitions


def __build_schema_hints(js_schema: dict):
    if js_schema is None:
        return None
    fields = {
        i["name"]: i["type"] for i in js_schema["fields"] if isinstance(i["type"], str)
    }
    schema_hints = ", ".join((f"{name} {type}" for name, type in fields.items()))

    return schema_hints


def __rename_invalid_columns(df: DataFrame) -> DataFrame:
    invalid_characters = "[ ,;{}()\n\t=\\/']"
    for col in df.columns:
        replace_col = re.sub(invalid_characters, "_", col)
        if col != replace_col:
            print(
                f"INVALID COLUMN NAME: {col} RENAMED AUTOMATICALLY TO -> {replace_col}"
            )
        df = df.withColumnRenamed(col, replace_col)

    return df


def build_table_path(bucket_name: str, data_pack_name: str, dataset_name: str):
    assert bucket_name in (
        BRONZE_BUCKET,
        SILVER_BUCKET,
        GOLD_BUCKET,
        DIAMOND_BUCKET
    ), f"bucket name must be one of {BRONZE_BUCKET}, {SILVER_BUCKET}, {GOLD_BUCKET} or {DIAMOND_BUCKET}"
    table_location = f"s3a://{bucket_name}/{data_pack_name}/{dataset_name}"

    return table_location


def build_checkpoint_path(
    bucket_name: str, data_pack_name: str, dataset_name: str, input_table_name: str = ""
):
    """
    :param bucket_name: bucket in S3 where the checkpoint is stored
    :param data_pack_name: name of the data_pack
    :param dataset_name: name of the dataset
    :param input_table_name: input_table if exists
    :return:
    """
    assert bucket_name == BRONZE_BUCKET or (
        input_table_name and bucket_name in (SILVER_BUCKET, GOLD_BUCKET, DIAMOND_BUCKET)
    ), f"bucket name must be one of {BRONZE_BUCKET}, {SILVER_BUCKET}, {GOLD_BUCKET} or {DIAMOND_BUCKET} and {input_table_name} must be valid when using {SILVER_BUCKET}, {GOLD_BUCKET} or {DIAMOND_BUCKET}"
    checkpoint_location = f"s3://{bucket_name}/_databricks_autoloader_checkpoints/{data_pack_name}/{dataset_name}/{input_table_name}"

    return checkpoint_location


def read_table(
    spark_session: SparkSession, db_name: str, table_name: str, where=None
) -> DataFrame:
    table_name = f"{db_name}.{table_name}"

    if where is None:
        df = spark_session.readStream.format("delta").table(tableName=table_name)
    else:
        df = (
            spark_session.readStream.format("delta")
            .table(tableName=table_name)
            .filter(where)
        )

    return df

def read_table_no_stream(
    spark_session: SparkSession, db_name: str, table_name: str, where=None
) -> DataFrame:
    table_name = f"{db_name}.{table_name}"

    if where is None:
        df = spark_session.read.format("delta").table(tableName=table_name)
    else:
        df = (
            spark_session.read.format("delta")
            .table(tableName=table_name)
            .filter(where)
        )

    return df


def read_data(
    spark_session: SparkSession,
    data_input_path: str,
    dict_schema_or_struct_schema: dict,
    data_type: str,
    read_options: dict = None,
    infer_schema=False,
    data_pack_name=None,
    dataset_name=None,
):
    if type(dict_schema_or_struct_schema) == dict:
        assert (
            dict_schema_or_struct_schema or infer_schema
        ), f"js_schema not provided while infer_schema is {infer_schema}. Please provide a schema or turn schema inference on"
    if read_options is None:
        read_options = dict()

    df = (
        spark_session.readStream.format("cloudFiles")
        .option("cloudFiles.format", data_type)
        .options(**read_options)
    )
    if infer_schema and type(dict_schema_or_struct_schema) == dict:
        schema_hints = __build_schema_hints(js_schema=dict_schema_or_struct_schema)
        schema_location = os.path.dirname(data_input_path)
        schema_location = os.path.join(schema_location, "_databricks_autoloader_schema")
        schema_location = os.path.join(schema_location, data_pack_name)
        schema_location = os.path.join(schema_location, dataset_name)
        schema_options = {
            "cloudFiles.schemaLocation": schema_location,
            "cloudFiles.schemaHints": schema_hints,
        }
        df = df.options(**schema_options)
    if type(dict_schema_or_struct_schema) == dict:
        partitions = __list_partition_columns(data_input_path)
        for partition, partition_type in partitions.items():
            partition = {
                "metadata": dict(),
                "name": partition,
                "nullable": True,
                "type": partition_type,
            }
            dict_schema_or_struct_schema["fields"].append(partition)
        schema = StructType.fromJson(dict_schema_or_struct_schema)
    else:
        schema = dict_schema_or_struct_schema

    df = df.schema(schema)

    return df.load(path=data_input_path)


def __write_function(
    micro_batch_df: DataFrame,
    db_name,
    table_name,
    sort_fields: list,
    upsert_fields: list = None,
    spark=None,
):
    if spark is None:
        spark = get_spark_session("upsert_data")
    match_condition = build_matching_sort_condition(
        sort_fields=sort_fields,
        existing_df_name="current_df",
        inserting_df_name="micro_batch_df",
    )

    micro_batch_df = micro_batch_df.sort(*sort_fields, ascending=False).drop_duplicates(
        subset=upsert_fields
    )
    current_df_name = "current_df"
    micro_batch_df_name = "micro_batch_df"
    upsert_condition = " AND ".join(
        [f"{current_df_name}.{i} = {micro_batch_df_name}.{i}" for i in upsert_fields]
    )
    table_name = f"{db_name}.{table_name}"

    current_df = DeltaTable.forName(spark, table_name)

    current_df.alias(current_df_name).merge(
        micro_batch_df.alias(micro_batch_df_name), upsert_condition
    ).whenMatchedUpdateAll(match_condition).whenNotMatchedInsertAll().execute()

    print(f"Created table {table_name} and loaded data")

    return True


# TODO: ADICIONAR PARAMETRO DE PATH
def write_table(
    df: DataFrame,
    checkpoint_location: str,
    db_name: str,
    table_name: str,
    insert_mode: str,
    spark=None,
    partition_columns=None,
    write_options: dict = None,
    sort_fields: list = None,
    upsert_fields: list = None,
):
    if partition_columns is None:
        partition_columns = list()
    if sort_fields is None:
        sort_fields = list()
    if write_options is None:
        write_options = dict()
    if spark is None:
        spark = get_spark_session("upsert_data")

    stream = (
        df.writeStream.trigger(once=True)
        .format("delta")
        .option("checkpointLocation", checkpoint_location)
        .option("header", "true")
        .option("mergeSchema", "true")
        .options(**write_options)
    )

    table_exists = check_table_exists(
        spark=spark, db_name=db_name, table_name=table_name
    )

    if insert_mode == "overwrite" and table_exists:
        truncate_table(spark=spark, table_name=f"{db_name}.{table_name}")

    if sort_fields and upsert_fields and insert_mode=="upsert":
        if table_exists:
            print(
                f"TABLE EXIST - upsert_fields: {upsert_fields} - sort_fields: {sort_fields}"
            )

            return stream.foreachBatch(
                lambda df, epochId: __write_function(
                    micro_batch_df=df,
                    db_name=db_name,
                    table_name=table_name,
                    sort_fields=sort_fields,
                    upsert_fields=upsert_fields,
                    spark=spark,
                )
                if not df.first() == None
                else None
            ).start()
        else:
            stream = stream.toTable(
                tableName=f"{db_name}.{table_name}", partitionBy=partition_columns
            )
            stream.awaitTermination()
            drop_table_duplicates(
                db_name=db_name,
                table_name=table_name,
                unique_id_fields=upsert_fields,
                sort_fields=sort_fields,
                spark=spark,
            )
            return stream

    return stream.toTable(
        tableName=f"{db_name}.{table_name}", partitionBy=partition_columns
    )


def __apply_profiling(df: DataFrame, profiling_s3_bucket, profiling_s3_key, layer: str):
    if df.count() == 0:
        raise ValueError("Dataframe is empty, profile aborted")
    else:
        profile_js = calculate_profilling(df, layer)
        __save_database_profile(profile_js, layer)
        save_database_profile_history(profile_js, profiling_s3_bucket)
        profile_js = json.dumps(profile_js)
        s3_client = S3(bucket_name=profiling_s3_bucket)

        return s3_client.put_object(profile_js, s3_key=profiling_s3_key)


def __save_database_profile(profile_js, layer, spark=None):
    if layer == "bronze":
        table = "cortex.data_governance_quality.bronze_profile"
    elif layer == "silver":
        table = "cortex.data_governance_quality.silver_profile"
    elif layer == "gold":
        table = "cortex.data_governance_quality.gold_profile"
    else:
        table = "cortex.data_governance_quality.diamond_profile"

    if spark is None:
        spark = get_spark_session("upsert_data")

    profile_js = profile_js["profilling"]["descriptiveStatistics"]["fields"]
    df = spark.createDataFrame(profile_js)
    df.write.option("header", "true").format('delta').mode('append').option("mergeSchema", "true").saveAsTable(table)

    # if layer == "bronze":
    #     frequent_fields = profile_js["profilling"]["descriptiveStatistics"]["mostFrequentFields"]
    #     df_frequent = spark.createDataFrame(pd.json_normalize(frequent_fields))
    #     df_frequent.write.option("header", "true").format('delta').mode('append').option("mergeSchema", "true").saveAsTable(table)


def __apply_processing_function(
    df: DataFrame, func: Callable, args: list, kwargs: dict
):
    if args is None:
        args = list()
    if kwargs is None:
        kwargs = dict()
    return func(df, *args, **kwargs)


def __apply_processing_functions(
    df: DataFrame,
    funcs: List[Callable],
    funcs_args: List[List],
    funcs_kwargs: List[dict],
):
    assert (
        len(funcs) == len(funcs_args) == len(funcs_kwargs)
    ), "The size of all the parameters (functions, args and kwargs) must be equal"
    for func, args, kwargs in zip(funcs, funcs_args, funcs_kwargs):
        df = __apply_processing_function(df=df, func=func, args=args, kwargs=kwargs)
    return df


def apply_processing_function(df: DataFrame, func, func_args, func_kwargs):
    if func is None:
        return df
    if isinstance(func, Iterable):
        return __apply_processing_functions(
            df=df, funcs=func, funcs_args=func_args, funcs_kwargs=func_kwargs
        )
    else:
        return __apply_processing_function(
            df=df, func=func, args=func_args, kwargs=func_kwargs
        )

# função que grava as métricas de qualidade no databricks
def save_database_profile_history(quality_js, profiling_s3_bucket, spark=None):
    if profiling_s3_bucket.find("bronze") >= 0:
        table = "cortex.data_governance_quality.bronze_profile_history"
    elif profiling_s3_bucket.find("silver") >= 0:
        table = "cortex.data_governance_quality.silver_profile_history"
    else:
        table = "cortex.data_governance_quality.gold_profile_history"

    if spark is None:
        spark = get_spark_session("upsert_data")

    fields=quality_js["profilling"]["descriptiveStatistics"]["fields"]
    df = spark.createDataFrame(fields)
    df.write.option("header", "true").format('delta').mode('append').option("mergeSchema", "true").saveAsTable(table)

    # if profiling_s3_bucket.find("bronze") >= 0:
    #     frequent_fields=quality_js["profilling"]["descriptiveStatistics"]["mostFrequentFields"]
    #     df = spark.createDataFrame(pd.json_normalize(frequent_fields))
    #     df.write.option("header", "true").format('delta').mode('append').option("mergeSchema", "true").saveAsTable(table)


def apply_profiling(df: DataFrame, data_pack_name: str, dataset_name: str, layer: str):
    # TODO: PARTICIONAR POR DATA
    profiling_s3_key = f"_databricks_profiling/{data_pack_name}/{dataset_name}.json"
    print(f"START PROFILING: {profiling_s3_key}")
    df.printSchema()
    df.show(5)
    __apply_profiling(
        df=df, profiling_s3_bucket=BRONZE_BUCKET, profiling_s3_key=profiling_s3_key, layer=layer
    )

    return True


def set_owner_to(spark, db_table, owner: str):
    print(f"ALTER TABLE {db_table} OWNER TO `{owner}`")
    spark.sql(f"ALTER TABLE {db_table} OWNER TO `{owner}`")

    return True


def truncate_table(spark, table_name):
    spark.sql(f"TRUNCATE TABLE {table_name}")
    print(f"TABLE {table_name} truncated")

    return True


def set_tbl_properties(spark, db_table, tbl_properties):
    array_properties = []
    for k in tbl_properties:
        text = f'"{k}"= "{tbl_properties[k]}"'
        array_properties.append(text)

    properties = ",".join(array_properties)
    print(f"ALTER TABLE {db_table} SET TBLPROPERTIES ({properties})")
    spark.sql(f"ALTER TABLE {db_table} SET TBLPROPERTIES ({properties})")

    return True


@__verify_parameters
def landing_to_bronze(
    data_input_path,
    data_type: str,
    data_pack_name,
    dataset_name,
    insert_mode=None,
    schema_path_or_struct_schema=None,
    partition_columns=None,
    spark=None,
    read_options: dict = None,
    write_options: dict = None,
    profiling=False,
    infer_schema=False,
    reset_checkpoint=False,
    table_owner='data-production',
    catalog_name=None,
    output_db_name=None,
    tbl_properties=None,
    upsert_fields: list = None,
):
    """
    Perform the ingestion of data into the bronze_layer database

    :param data_input_path: s3 input path where the data is located
    :param data_type: the type of the data used as the parameter cloudFiles.format. Examples: 'csv', 'parquet', 'json'
    :param data_pack_name: name of the data_pack
    :param dataset_name: name of the dataset
    :param schema_path_or_struct_schema: path in s3 of the json containing the schema of the data or StructType. If not provided, is expected 'infer_schema' to be True
    :param partition_columns: the columns of the data to use as partition columns
    :param spark: the SparkSession object to use
    :param read_options: the read_options dictionary to be forwarded to spark
    :param write_options: the write_options dictionary to be forwarded to spark
    :param profiling: flag that indicates if the data profiling will be executed
    :param infer_schema: flag that indicates if the schema will be infered by spark
    :param reset_checkpoint: flag that indicates if the Autoloader checkpoint will be deleted
    :param catalog_name: unity catalog name
    :param output_db_name: database where the data will be written
    :param tbl_properties: properties to add to table
    :param upsert_fields: fields to use when upserting
    :return:
    """
    if spark is None:
        spark = get_spark_session(app_name=dataset_name)
    if partition_columns is None:
        partition_columns = list()

    if reset_checkpoint:
        reset_autoloader_checkpoint(
            bucket_name=BRONZE_BUCKET,
            data_pack_name=data_pack_name,
            dataset_name=dataset_name,
        )
    if output_db_name is None:
        output_db_name = BRONZE_DB_NAME

    if type(schema_path_or_struct_schema) == str:
        schema = get_schema_from_s3(schema_path_or_struct_schema)
    else:
        schema = schema_path_or_struct_schema

    if catalog_name is None:
        catalog_name = "hive_metastore"

    if os.getenv("ENVIRONMENT") != "LOCAL":
        spark.sql(f"USE CATALOG {catalog_name}")

    if insert_mode is None:
        insert_mode = "append"

    df = read_data(
        spark,
        data_input_path=data_input_path,
        dict_schema_or_struct_schema=schema,
        data_type=data_type,
        read_options=read_options,
        infer_schema=infer_schema,
        data_pack_name=data_pack_name,
        dataset_name=dataset_name,
    )

    if type(schema) == dict:
        df = process_dataframe(df, js_schema=schema)

    df = __rename_invalid_columns(df)

    checkpoint_location = build_checkpoint_path(
        bucket_name=BRONZE_BUCKET,
        data_pack_name=data_pack_name,
        dataset_name=dataset_name,
    )

    db_name = f"{catalog_name}.{output_db_name}"

    stream = write_table(
        df,
        checkpoint_location=checkpoint_location,
        db_name=db_name,
        table_name=dataset_name,
        insert_mode=insert_mode,
        spark=spark,
        partition_columns=partition_columns,
        write_options=write_options,
        upsert_fields=upsert_fields,
    )

    db_table = f"{db_name}.{dataset_name}"


    if catalog_name != "hive_metastore":
        set_owner_to(spark, db_table, table_owner)

    if tbl_properties:
        set_tbl_properties(spark, db_table, tbl_properties)

    if profiling:
        stream.awaitTermination()
        df = spark.read.table(db_table)
        apply_profiling(
            df=df, data_pack_name=data_pack_name, dataset_name=dataset_name, layer="bronze"
        )


    databricks_obj = DatabricksSpark()
    databricks_obj.set_table_all_privileges(catalog_name=catalog_name,
                    database_name=output_db_name,
                    spark_session=spark,
                    table_modifiers=["data-platform"],
                    table_name=dataset_name)

    return True


@__verify_parameters
def bronze_to_silver(
    input_table_name,
    data_pack_name,
    dataset_name,
    insert_mode,
    input_db_name=None,
    output_db_name=None,
    partition_columns=None,
    spark=None,
    write_options: dict = None,
    processing_function=None,
    processing_function_args=None,
    processing_function_kwargs=None,
    table_owner='data-production',
    profiling=False,
    reset_checkpoint=False,
    catalog_name=None,
    where=None,
    tbl_properties=None,
    sort_fields: list = None,
    upsert_fields: list = None,
    governance_options=None
):
    if spark is None:
        spark = get_spark_session(app_name=dataset_name)
    if partition_columns is None:
        partition_columns = list()
    if reset_checkpoint:
        reset_autoloader_checkpoint(
            bucket_name=SILVER_BUCKET,
            data_pack_name=data_pack_name,
            dataset_name=dataset_name,
            input_table_name=input_table_name,
        )
    if insert_mode is None:
        insert_mode = "append"

    if input_db_name is None:
        input_db_name = BRONZE_DB_NAME

    if output_db_name is None:
        output_db_name = SILVER_DB_NAME

    if catalog_name is None:
        catalog_name = "hive_metastore"

    if os.getenv("ENVIRONMENT") != "LOCAL":
        spark.sql(f"USE CATALOG {catalog_name}")

    input_db_name = f"{catalog_name}.{input_db_name}"
    output_db_name = f"{catalog_name}.{output_db_name}"

    if sort_fields is None:
        sort_fields = get_table_partitions(
            spark=spark, db_name=input_db_name, table_name=input_table_name
        )

    df = read_table(
        spark, db_name=input_db_name, table_name=input_table_name, where=where
    )

    if df.first() == None:
        print("Dataframe is empty")
        return True

    df = apply_processing_function(
        df=df,
        func=processing_function,
        func_args=processing_function_args,
        func_kwargs=processing_function_kwargs,
    )

    checkpoint_location = build_checkpoint_path(
        bucket_name=SILVER_BUCKET,
        data_pack_name=data_pack_name,
        dataset_name=dataset_name,
        input_table_name=input_table_name,
    )
    stream = write_table(
        df,
        checkpoint_location=checkpoint_location,
        db_name=output_db_name,
        table_name=dataset_name,
        insert_mode=insert_mode,
        spark=spark,
        partition_columns=partition_columns,
        write_options=write_options,
        sort_fields=sort_fields,
        upsert_fields=upsert_fields,
    )

    output_db_table = f"{output_db_name}.{dataset_name}"

    if catalog_name != "hive_metastore":
        set_owner_to(spark, output_db_table, table_owner)

    if tbl_properties:
        set_tbl_properties(spark, output_db_table, tbl_properties)

    if profiling:
        stream.awaitTermination()
        df = spark.read.table(output_db_table)
        apply_profiling(
            df=df, data_pack_name=data_pack_name, dataset_name=dataset_name, layer="silver"
        )

    if governance_options:
        if tbl_properties:
            try:
                columns = [
                            'id_datapack',
                            'table_name',
                            'description',
                            'security_level',
                            'data_owner',
                            'cycle_collection',
                            'volumetry',
                            'columns_count',
                            'rows_count',
                            'last_update',
                            'create_date',
                            'table_url',
                            'layer'
                        ]
                values = [
                        (
                            tbl_properties.get('cortex.source'),
                            tbl_properties.get('cortex.tableName'),
                            tbl_properties.get('cortex.description'),
                            tbl_properties.get('cortex.securityLevel'),
                            tbl_properties.get('cortex.dataOwner'),
                            tbl_properties.get('cortex.cycleCollection'),
                            tbl_properties.get('cortex.volumetry'),
                            tbl_properties.get('cortex.columnsCount'),
                            tbl_properties.get('cortex.rowsCount'),
                            tbl_properties.get('cortex.lastUpdate'),
                            tbl_properties.get('cortex.createDate'),
                            get_link_table(catalog_name, 'silver', tbl_properties.get('cortex.tableName')),
                            'silver'
                        )
                    ]
                df_governance = spark.createDataFrame(values, columns)
                df_governance.write.option("header", "true")\
                    .format('delta')\
                    .mode('append')\
                    .saveAsTable("cortex.data_governance_quality.tables")
                print(f"""
                catalog_name : {catalog_name},
                output_db_table : {output_db_table},
                description : {tbl_properties.get('cortex.description')},
                """)
                set_comment_table(catalog_name, f"silver.{tbl_properties.get('cortex.tableName')}", tbl_properties.get('cortex.description'))

            except Exception as e:
                print(e)
        else:
            print("ERROR : properties not found")
    return True


@__verify_parameters
def silver_to_gold(
    input_table_name,
    data_pack_name,
    dataset_name,
    insert_mode,
    input_db_name=None,
    output_db_name=None,
    partition_columns=None,
    spark=None,
    write_options: dict = None,
    processing_function=None,
    processing_function_args=None,
    processing_function_kwargs=None,
    table_owner='data-production',
    profiling=False,
    sort_fields: list = None,
    upsert_fields: list = None,
    reset_checkpoint=False,
    catalog_name=None,
    where=None,
    tbl_properties=None,
    governance_options=None,
):
    if spark is None:
        spark = get_spark_session(app_name=dataset_name)
    if partition_columns is None:
        partition_columns = list()
    if upsert_fields is None:
        upsert_fields = ["cortex_id"]
    if input_db_name is None:
        input_db_name = SILVER_DB_NAME
    if output_db_name is None:
        output_db_name = GOLD_DB_NAME

    if catalog_name is None:
        catalog_name = "hive_metastore"

    if os.getenv("ENVIRONMENT") != "LOCAL":
        spark.sql(f"USE CATALOG {catalog_name}")

    input_db_name = f"{catalog_name}.{input_db_name}"
    output_db_name = f"{catalog_name}.{output_db_name}"

    if sort_fields is None:
        sort_fields = get_table_partitions(
            spark=spark, db_name=input_db_name, table_name=input_table_name
        )
    if reset_checkpoint:
        reset_autoloader_checkpoint(
            bucket_name=GOLD_BUCKET,
            data_pack_name=data_pack_name,
            dataset_name=dataset_name,
            input_table_name=input_table_name,
        )
    if insert_mode is None:
        insert_mode = "append"

    if insert_mode == "upsert":
        df = read_table_no_stream(
            spark, db_name=input_db_name, table_name=input_table_name, where=where
        )
    else:
        df = read_table(
            spark, db_name=input_db_name, table_name=input_table_name, where=where
        )

    if df.first() == None:
        print("Dataframe is empty")
        return True

    df = apply_processing_function(
        df=df,
        func=processing_function,
        func_args=processing_function_args,
        func_kwargs=processing_function_kwargs,
    )

    checkpoint_location = build_checkpoint_path(
        bucket_name=GOLD_BUCKET,
        data_pack_name=data_pack_name,
        dataset_name=dataset_name,
        input_table_name=input_table_name,
    )
    stream = write_table(
        df,
        checkpoint_location=checkpoint_location,
        db_name=output_db_name,
        table_name=dataset_name,
        insert_mode=insert_mode,
        spark=spark,
        partition_columns=partition_columns,
        write_options=write_options,
        sort_fields=sort_fields,
        upsert_fields=upsert_fields,
    )

    output_db_table = f"{output_db_name}.{dataset_name}"

    if catalog_name != "hive_metastore":
        set_owner_to(spark, output_db_table, table_owner)

    if tbl_properties:
        set_tbl_properties(spark, output_db_table, tbl_properties)

    if profiling:
        stream.awaitTermination()
        df = spark.read.table(output_db_table)
        apply_profiling(
            df=df, data_pack_name=data_pack_name, dataset_name=dataset_name, layer="gold"
        )
    if governance_options:
        if tbl_properties:
            try:
                columns = [
                            'id_datapack',
                            'table_name',
                            'description',
                            'security_level',
                            'data_owner',
                            'cycle_collection',
                            'volumetry',
                            'columns_count',
                            'rows_count',
                            'last_update',
                            'create_date',
                            'exposures',
                            'table_url'
                            'layer'
                        ]
                values = [
                        (
                            tbl_properties.get('cortex.source'),
                            tbl_properties.get('cortex.tableName'),
                            tbl_properties.get('cortex.description'),
                            tbl_properties.get('cortex.securityLevel'),
                            tbl_properties.get('cortex.dataOwner'),
                            tbl_properties.get('cortex.cycleCollection'),
                            tbl_properties.get('cortex.volumetry'),
                            tbl_properties.get('cortex.columnsCount'),
                            tbl_properties.get('cortex.rowsCount'),
                            tbl_properties.get('cortex.lastUpdate'),
                            tbl_properties.get('cortex.createDate'),
                            tbl_properties.get('cortex.exposures'),
                            get_link_table(catalog_name, 'gold', tbl_properties.get('cortex.tableName')),
                            'gold'
                        )
                    ]
                df_governance = spark.createDataFrame(values, columns)
                df_governance.write.option("header", "true")\
                    .format('delta')\
                    .mode('append')\
                    .saveAsTable("cortex.data_governance_quality.tables")
                set_comment_table(catalog_name, f"gold.{tbl_properties.get('cortex.tableName')}", tbl_properties.get('cortex.description'))

            except Exception as e:
                print(e)
        else:
            print("ERROR : properties not found")





@__verify_parameters
def gold_to_diamond(
    input_table_name,
    data_pack_name,
    dataset_name,
    insert_mode,
    input_db_name=None,
    output_db_name=None,
    partition_columns=None,
    spark=None,
    write_options: dict = None,
    processing_function=None,
    processing_function_args=None,
    processing_function_kwargs=None,
    table_owner='data-production',
    profiling=False,
    sort_fields: list = None,
    upsert_fields: list = None,
    reset_checkpoint=False,
    catalog_name=None,
    where=None,
    tbl_properties=None,
):
    if spark is None:
        spark = get_spark_session(app_name=dataset_name)
    if partition_columns is None:
        partition_columns = list()
    if upsert_fields is None:
        upsert_fields = ["cortex_id"]
    if input_db_name is None:
        input_db_name = GOLD_DB_NAME
    if output_db_name is None:
        output_db_name = DIAMOND_DB_NAME

    if catalog_name is None:
        catalog_name = "hive_metastore"

    if os.getenv("ENVIRONMENT") != "LOCAL":
        spark.sql(f"USE CATALOG {catalog_name}")

    input_db_name = f"{catalog_name}.{input_db_name}"
    output_db_name = f"{catalog_name}.{output_db_name}"

    if sort_fields is None:
        sort_fields = get_table_partitions(
            spark=spark, db_name=input_db_name, table_name=input_table_name
        )
    if reset_checkpoint:
        reset_autoloader_checkpoint(
            bucket_name=DIAMOND_BUCKET,
            data_pack_name=data_pack_name,
            dataset_name=dataset_name,
            input_table_name=input_table_name,
        )
    if insert_mode is None:
        insert_mode = "append"

    df = read_table(
        spark, db_name=input_db_name, table_name=input_table_name, where=where
    )

    if df.first() == None:
        print("Dataframe is empty")
        return True

    df = apply_processing_function(
        df=df,
        func=processing_function,
        func_args=processing_function_args,
        func_kwargs=processing_function_kwargs,
    )

    checkpoint_location = build_checkpoint_path(
        bucket_name=DIAMOND_BUCKET,
        data_pack_name=data_pack_name,
        dataset_name=dataset_name,
        input_table_name=input_table_name,
    )
    stream = write_table(
        df,
        checkpoint_location=checkpoint_location,
        db_name=output_db_name,
        table_name=dataset_name,
        insert_mode=insert_mode,
        spark=spark,
        partition_columns=partition_columns,
        write_options=write_options,
        sort_fields=sort_fields,
        upsert_fields=upsert_fields,
    )

    output_db_table = f"{output_db_name}.{dataset_name}"

    if catalog_name != "hive_metastore":
        set_owner_to(spark, output_db_table, table_owner)

    if tbl_properties:
        set_tbl_properties(spark, output_db_table, tbl_properties)

    if profiling:
        stream.awaitTermination()
        df = spark.read.table(output_db_table)
        apply_profiling(
            df=df, data_pack_name=data_pack_name, dataset_name=dataset_name, layer="diamond"
        )

    return True

def gold_to_kafka(
    input_table_name,
    topic_name,
    input_db_name=None,
    spark=None,
    write_options: dict = None,
    kafka_security_protocol="SSL",
    kafka_bootstrap_servers=DEFAULT_BOOTSTRAP_SERVERS,
    processing_function=None,
    processing_function_args=None,
    processing_function_kwargs=None,
    reset_checkpoint=False,
    catalog_name=None,
    where=None,
):
    topics = [topic_name]
    create_topics_if_not_exists(
        topics=topics, bootstrap_servers=kafka_bootstrap_servers
    )
    checkpoint_location = f"s3://{GOLD_BUCKET}/_databricks_autoloader_checkpoints/kafka/{input_db_name}/{input_table_name}"
    if spark is None:
        spark = get_spark_session(app_name=input_table_name)

    if reset_checkpoint:
        __delete_checkpoint_location(
            bucket_name=GOLD_BUCKET, checkpoint_location=checkpoint_location
        )
    if write_options is None:
        write_options = dict()
    if input_db_name is None:
        input_db_name = GOLD_DB_NAME
    if catalog_name is None:
        catalog_name = "hive_metastore"
    if os.getenv("ENVIRONMENT") != "LOCAL":
        spark.sql(f"USE CATALOG {catalog_name}")

    input_db_name = f"{catalog_name}.{input_db_name}"

    if sort_fields is None:
        sort_fields = get_table_partitions(
            spark=spark, db_name=input_db_name, table_name=input_table_name
        )

    df = read_table(
        spark, db_name=input_db_name, table_name=input_table_name, where=where
    )

    if df.first() == None:
        print("Dataframe is empty")
        return True

    df = apply_processing_function(
        df=df,
        func=processing_function,
        func_args=processing_function_args,
        func_kwargs=processing_function_kwargs,
    )

    stream = (
        df.selectExpr("CAST(cortex_id AS STRING) as key", "to_json(struct(*)) AS value")
        .writeStream.trigger(once=True)
        .format("kafka")
        .option("checkpointLocation", checkpoint_location)
        .option("kafka.bootstrap.servers", kafka_bootstrap_servers)
        .option("topic", topic_name)
        .option("kafka.security.protocol", kafka_security_protocol)
        .options(**write_options)
    )
    stream.start()
