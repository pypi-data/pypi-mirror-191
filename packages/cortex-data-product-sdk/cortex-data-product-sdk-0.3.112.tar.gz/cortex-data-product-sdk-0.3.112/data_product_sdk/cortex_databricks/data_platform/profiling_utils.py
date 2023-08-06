import json

import pyspark.sql.functions as F
from pyspark.sql import DataFrame
import os
from data_product_sdk.cortex_databricks.data_platform.spark_utils import (
    get_spark_session
)


def calculate_profilling(df: DataFrame, layer: str):
    df_count = df.count()
    df_count_distinct = df.distinct().count()

    fields = []
    for column in df.columns:
        field_type = _get_type(df, column)
        result = calculate_by_field(df, column, field_type, df_count)
        fields.append(result)

    #frequent_fields = _treat_most_frequent_fields(df) if layer == "bronze" else None

    descriptive_statistics = _treat_descriptive_statistics(fields, df_count, df_count_distinct)
    profilling = _treat_returned_profilling(descriptive_statistics)

    return profilling


def calculate_by_field(data, field, field_type, df_count):

    calc_result = {
        'field': field,
        'type': field_type,
        'countRows': 0,
        'countRowsDistinct': 0,
        'countRowsMissing': 0,
        'countRowsPercentage': 0.0,
        'countRowsMissingPercentage': 0.0,
        'distribution': [],
    }

    field_data = data.select(field).filter(F.col(field).isNotNull())

    _get_field_count_metrics(field_data, field, field_type, df_count, calc_result)

    _get_field_distribution_metric(field_data, field, field_type, df_count, calc_result)

    return calc_result


def _treat_object(fields, data, parent, field, df_count):
    data_nested = data.select(F.col(field+".*"))
    for column_nested in data_nested.columns:
        field_type = _get_type(data_nested, column_nested)
        if field_type == "object":
            parent_nested = parent + "." + column_nested
            parent = _treat_object(fields, data_nested, parent_nested, column_nested, df_count)
        elif field_type == "array":
            parent_nested = parent + "." + column_nested
            parent = _treat_array(fields, data_nested, parent_nested, column_nested, df_count)
        else:
            result = calculate_by_field(data_nested, column_nested, field_type, df_count)
            result["field"] = parent + "." + result["field"]
            fields.append(result)

    return fields


def _treat_array(fields, data, parent, field, df_count):
    data_nested = data.select(F.explode(field).alias(field))
    data_nested = data_nested.select(field+".*","*").drop(field)

    for column_nested in data_nested.columns:
        field_type = _get_type(data_nested, column_nested)
        if field_type == "object":
            parent_nested = parent + "." + column_nested
            parent = _treat_object(fields, data_nested, parent_nested, column_nested)
        elif field_type == "array":
            parent_nested = parent + "." + column_nested
            parent = _treat_array(fields, data_nested, parent_nested, column_nested)
        else:
            result = calculate_by_field(data_nested, column_nested, field_type, df_count)
            result["field"] = parent + "." + result["field"]
            fields.append(result)

    return fields


def _get_type(data, field):
    field_type = ""
    for t in data.dtypes:
        if t[0] == field:
            field_type = t[1]
            break

    return _check_field_type(field_type)


def _check_field_type(field_type):
    if field_type.startswith("struct<"):
        field_type = "object"
    elif field_type.startswith("array<bigint>"):
        field_type = "array-bigint"
    elif field_type.startswith("array<string>"):
        field_type = "array-string"
    elif field_type.startswith("array<boolean>"):
        field_type = "array-boolean"
    elif field_type.startswith("array<double>"):
        field_type = "array-double"
    elif field_type.startswith("array<"):
        field_type = "array"

    return field_type


def _treat_descriptive_statistics(fields, df_count, df_count_distinct):
    descriptive_statistics = {
        'countFields': len(fields),
        'countRows': df_count,
        'countRowsDistinct': df_count_distinct,
        'fields': fields,
    }

    # if frequent_fields is not None:
    #     descriptive_statistics['mostFrequentFields'] = frequent_fields

    return descriptive_statistics


def _treat_returned_profilling(descriptive_statistics):
    profilling = {
        "descriptiveStatistics": descriptive_statistics
    }

    return {
        "profilling": profilling
    }


def _get_field_count_metrics(field_data, field, field_type, df_count, calc_result):
    field_count = field_data.count()
    field_count_distinct = field_data.distinct().count()
    field_count_missing = df_count - field_count
    field_count_percentage = _calc_percentage_ratio_from_n1_to_n2(field_count, df_count)
    field_count_missing_percentage = _calc_percentage_ratio_from_n1_to_n2(field_count_missing, df_count)

    if _is_numeric(field=field_type) or field_type == "timestamp":
        calc_result['max'] = field_data.agg({field: "max"}).collect()[0][0]
        calc_result['min'] = field_data.agg({field: "min"}).collect()[0][0]

    calc_result['countRows'] = field_count
    calc_result['countRowsDistinct'] = field_count_distinct
    calc_result['countRowsMissing'] = field_count_missing
    calc_result['countRowsPercentage'] = field_count_percentage
    calc_result['countRowsMissingPercentage'] = field_count_missing_percentage

    return calc_result


def _calc_percentage_ratio_from_n1_to_n2(n1, n2):
    diff = 100 * float(n1) / n2
    return round(diff, 2)


def _get_field_distribution_metric(field_data, field, field_type, df_count, calc_result):
    if field_type == "boolean":
        return _treat_boolean_distribution(df_count, field_data, field, calc_result['distribution'])

    elif field_type == "int" or field_type == "bigint" or field_type == "double":
        return _treat_numeric_distribution(field_data, field, calc_result['distribution'])

    elif field_type == "string":
        return _treat_string_distribution(df_count, field_data, field, calc_result['distribution'])

    elif field_type == "timestamp":
        return _treat_timestamp_distribution(df_count, field_data, field, calc_result['distribution'])

    elif field_type == "object":
        pass

    else:
        return _treat_default_distribution(df_count, field_data, field, calc_result['distribution'])


def _treat_boolean_distribution(df_count, dist, field, distribution, limit=30):
    field_count = dist.count()
    dist = dist.groupBy(field).count()\
        .sort('count', ascending=False)\
        .limit(limit)

    for row in dist.toJSON().collect():
        row_json = json.loads(row)
        treat_dist = {
            'summary': str(row_json[field]).lower(),
            'value': str(row_json["count"]),
            'fieldDistributionPercentage': str(_calc_percentage_ratio_from_n1_to_n2(row_json["count"], field_count)),
            'totalDistributionPercentage': str(_calc_percentage_ratio_from_n1_to_n2(row_json["count"], df_count))
        }
        distribution.append(treat_dist)

    return distribution


def _treat_numeric_distribution(dist, field, distribution):
    dist = dist.withColumnRenamed(field, "value")
    dist = dist.summary("count", "min", "5%", "25%",
                        "50%", "75%", "95%", "max",
                        "mean", "stddev")
    for row in dist.toJSON().collect():
        distribution.append(json.loads(row))

    return distribution


def _treat_string_distribution(df_count, dist, field, distribution, limit=30):
    field_count = dist.count()
    dist = dist.groupBy(field).count()\
        .sort('count', ascending=False)\
        .limit(limit)

    for row in dist.toJSON().collect():
        row_json = json.loads(row)
        treat_dist = {
            'summary': row_json[field],
            'value': str(row_json["count"]),
            'fieldDistributionPercentage': str(_calc_percentage_ratio_from_n1_to_n2(row_json["count"], field_count)),
            'totalDistributionPercentage': str(_calc_percentage_ratio_from_n1_to_n2(row_json["count"], df_count))
        }
        distribution.append(treat_dist)

    return distribution


def _treat_timestamp_distribution(df_count, dist, field, distribution):
    field_count = dist.count()
    dist = dist.withColumn("min", F.lit(dist.agg({'id': 'min'}).collect()[0][0]))
    dist = dist.withColumn("max", F.lit(dist.agg({'id': 'max'}).collect()[0][0]))

    for row in dist.toJSON().collect():
        for attr, value in json.loads(row).items():
            treat_dist = {
                'summary': attr,
                'value': str(value),
                'fieldDistributionPercentage': str(_calc_percentage_ratio_from_n1_to_n2(value, field_count)),
                'totalDistributionPercentage': str(_calc_percentage_ratio_from_n1_to_n2(value, df_count))
        }
            distribution.append(treat_dist)

    return distribution


def _treat_default_distribution(df_count, dist, field, distribution, limit=30):
    field_count = dist.count()
    dist = dist.groupBy(field).count()\
        .sort('count', ascending=False)\
        .limit(limit)

    for row in dist.toJSON().collect():
        row_json = json.loads(row)
        treat_dist = {
            'summary': str(row_json[field]).lower(),
            'value': str(row_json["count"]),
            'fieldDistributionPercentage': str(_calc_percentage_ratio_from_n1_to_n2(row_json["count"], field_count)),
            'totalDistributionPercentage': str(_calc_percentage_ratio_from_n1_to_n2(row_json["count"], df_count))
        }
        distribution.append(treat_dist)

    return distribution


def _is_numeric(field):
    return field == "int" or field == "bigint" or field == "double"


def _treat_most_frequent_fields(df: DataFrame, limit=30):
    fields = []
    for column in df.columns:
        field_data = (
            df.select(column)
            .filter(F.col(column).isNotNull())
            .groupBy(column)
            .count()
            .sort("count", ascending=False)
            .limit(limit)
        )
        # TODO: Verificar a validação por tipo de campo
        for row in field_data.toJSON().collect():
            row_json = json.loads(row)
            fields.append({
                "field": column,
                "summary": row_json[column],
                "count": row_json["count"]
            })
    return fields


def get_volumetry(catalog, stage, table_name, df: DataFrame, spark=None):
    if spark is None:
        spark = get_spark_session("upsert_data")
    table = spark.sql(f""" SELECT * FROM  {catalog}.{stage}.{table_name} """)
    
    return table.count() + df.count()

def get_details(catalog, stage, table_name, spark=None):
    if spark is None:
        spark = get_spark_session("upsert_data")
    df_details = spark.sql(f""" DESCRIBE DETAIL {catalog}.{stage}.{table_name} """)
    temp_list = df_details.select("lastModified", "createdAt").collect()
    last_update = temp_list[0][0]
    create_date = temp_list[0][1]
    return last_update, create_date

def get_rows_count(df : DataFrame):
    return df.count()

def get_columns_count(df : DataFrame):
    return len(df.columns)

def get_link_table(catalog, schema, table):
    workspace_domain = os.getenv("DATABRICKS_WORKSPACE_DOMAIN") 
    return f"{workspace_domain}/explore/data/{catalog}/{schema}/{table}"