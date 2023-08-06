from pyspark.sql.types import StructType, StructField, IntegerType, StringType

from data_product_sdk.cortex_databricks.data_platform.loader_utils import __get_partition_type, read_table, __verify_parameters, __resolve_partition_columns, __list_partition_columns, __build_schema_hints, __rename_invalid_columns, build_table_path, build_checkpoint_path
import logging
import pytest
from pyspark.sql import SparkSession, DataFrame
import boto3
from moto import mock_s3
import json


@__verify_parameters
def verify_parameters_test(x, y, *args, **kwargs):
    return x+y


def test__verify_parameters():
    assert verify_parameters_test(2, 3, insert_mode="append") == 5

def test__get_partition_type():
    assert __get_partition_type("2022-10-18") == "date"

def test__resolve_partition_columns():
    assert  len(__resolve_partition_columns("./foo/bar")) == 0


@mock_s3
def test__list_partition_columns():
    bucket_name = "my_bucket"
    items = [{"name":"path1/QNfyngdTn1obYs5kOOV6KzZG=/", "value":"foo"},{"name":"path1/ZS=dw\qQI?zG4JBE3}-slX($9 R&ui/K&Kcc(d9@jxs3;< &{=.G_D#}KM8/", "value":"bar"},{"name":"path1/T23Wq_6mvTfHc1aC2c7Th3PNxbJN0PkcSt9RxTff8KhJ1wXJCarGkIPpTD7KrcIvA0eazbpC4Pj8gA2wvNrQuM=/", "value":"xpto"}]
    s3 = boto3.resource('s3', region_name='us-east-1')
    s3.create_bucket(Bucket=bucket_name)
    for item in items:
        object = s3.Object(bucket_name, item.get("name"))
        object.put(Body=item.get("value"))

    res = __list_partition_columns(f"s3://{bucket_name}/path1")
    assert len(res) == 3


def test__build_schema_hints():
    file = open("tests/mock_data/receita_federal_schema.json", "r")
    schema = json.load(file)
    file.close()
    res = __build_schema_hints(js_schema=schema)
    assert res == 'receita_federal_simples_cnpj_basico string, receita_federal_simples_opcao string, receita_federal_simples_opcao_data string, receita_federal_simples_opcao_exclusao_data string, receita_federal_simples_opcao_mei string, receita_federal_simples_opcao_mei_data string, receita_federal_simples_opcao_mei_exclusao_data string'


def test__rename_invalid_columns(spark_session: SparkSession):
    df = spark_session.createDataFrame(
    [
        (1, "foo"),
        (2, "bar"),
    ],
    ["(id)", "{label}"]
)
    res = __rename_invalid_columns(df)
    assert all(item in ["_id_","_label_"] for item in res.columns) == True


def test_build_table_path():
    bucket_name = "cortex-databricks-bronze-dev"
    data_pack_name = "foo"
    dataset_name = "bar"
    res = build_table_path(bucket_name=bucket_name, data_pack_name=data_pack_name, dataset_name=dataset_name)
    assert res == f"s3a://{bucket_name}/{data_pack_name}/{dataset_name}"


def test_build_checkpoint_path():
    bucket_name="cortex-databricks-bronze-dev"
    data_pack_name="foo"
    dataset_name="bar"
    input_table_name="xpto"
    res = build_checkpoint_path(bucket_name=bucket_name, data_pack_name=data_pack_name, dataset_name=dataset_name, input_table_name= input_table_name)
    assert res == 's3://cortex-databricks-bronze-dev/_databricks_autoloader_checkpoints/foo/bar/xpto'


def quiet_py4j():
    """Suppress spark logging for the test context."""
    logger = logging.getLogger('py4j')
    logger.setLevel(logging.WARN)


@pytest.fixture(scope="session")
def spark_session(request) -> SparkSession:
    """Fixture for creating a spark context."""

    spark = (SparkSession
             .builder
             .master('local[2]')
             .appName('pytest-pyspark-local-testing')
             .enableHiveSupport()
             .getOrCreate())
    request.addfinalizer(lambda: spark.stop())

    quiet_py4j()
    return spark


def test_read_table(spark_session: SparkSession) -> DataFrame:
    # prepare
    db_name = 'teste'
    table_name = 'test'
    schema = StructType([
        StructField('cortex_id', IntegerType(), True),
        StructField('label', StringType(), True),
        StructField('year', IntegerType(), True),
        StructField('month', IntegerType(), True),
        StructField('day', IntegerType(), True),
    ])

    spark_session.sql(f"CREATE DATABASE IF NOT EXISTS {db_name}")
    spark_session.catalog.setCurrentDatabase(db_name)
    if not spark_session._jsparkSession.catalog().tableExists(db_name, table_name):
        spark_session.catalog.createTable(tableName=table_name, schema=schema)

    # execute
    df = read_table(spark_session=spark_session, db_name='teste', table_name='test')
    df.printSchema()

    # assert
    assert not set(df.schema).symmetric_difference(set(schema))
    return df


def test_write_table(spark_session: SparkSession):
    # prepare
    db_name = 'teste'
    input_table = 'input_table'
    schema = StructType([
        StructField('cortex_id', IntegerType(), True),
        StructField('label', StringType(), True),
        StructField('year', IntegerType(), True),
        StructField('month', IntegerType(), True),
        StructField('day', IntegerType(), True),
    ])
    df = spark_session.createDataFrame(
        [
            (1, "foo", 2022, 5, 1),
            (2, "bar", 2022, 5, 1),
        ],
        schema=schema
    )

    spark_session.sql(f"DROP DATABASE {db_name} CASCADE ")
    spark_session.sql(f"CREATE DATABASE IF NOT EXISTS {db_name}")
    spark_session.catalog.setCurrentDatabase(db_name)
    df.write.format('parquet').saveAsTable(input_table, mode='append', partitionBy=['year', 'month', 'day'])

    # execute
    output_table = 'output_table'
    partition_columns = ['year', 'month', 'day']
    checkpoint_location = 'test_location/checkpoint/test'
    df = read_table(spark_session=spark_session, db_name=db_name, table_name=input_table)
    # write_table(df=df, checkpoint_location=checkpoint_location, db_name=db_name, table_name=output_table, spark=spark_session, partition_columns=partition_columns) # TODO: FALHA POIS FORMATO DELTA SO EXISTE NO DATABRICKS
    stream = df.writeStream.trigger(once=True) \
        .format('parquet') \
        .option('checkpointLocation', checkpoint_location) \

    stream.toTable(tableName=f'{db_name}.{output_table}', partitionBy=partition_columns)

    # assert
