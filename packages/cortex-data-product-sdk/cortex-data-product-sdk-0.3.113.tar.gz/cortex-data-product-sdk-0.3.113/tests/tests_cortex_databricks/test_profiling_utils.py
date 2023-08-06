from data_product_sdk.cortex_databricks.data_platform.profiling_utils import _calc_percentage_ratio_from_n1_to_n2, _treat_numeric_distribution, calculate_profilling, calculate_by_field, _get_type, _check_field_type, _treat_descriptive_statistics, _treat_returned_profilling, _get_field_count_metrics, _get_field_distribution_metric, _treat_boolean_distribution, _treat_string_distribution, _treat_timestamp_distribution, _treat_default_distribution
from pyspark.sql import SparkSession
import pytest
import logging
import pyspark.sql.functions as F

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

def test_calculate_profilling(spark_session: SparkSession):
    df = spark_session.createDataFrame(
    [
        (1, "foo"),
        (2, "bar"),
    ],
    ["id", "label"]
)
    res = calculate_profilling(df)
    assert len(res) > 0


def test_calculate_by_field(spark_session: SparkSession):
    df = spark_session.createDataFrame(
    [
        (1, "foo"),
        (2, "bar"),
    ],
    ["id", "label"]
)
    data = df
    field = "label"
    field_type = str
    df_count = df.count()
    res = calculate_by_field(data, field, field_type, df_count)
    assert len(res) > 0

def test__get_type(spark_session: SparkSession):
    df = spark_session.createDataFrame(data=[
    {
        "id": 10,
        "label": 100

    }
])
    data = df
    field = "id"
    res = _get_type(data, field)
    assert res == "bigint"

def test__check_field_type():
    res = _check_field_type("array")
    assert res == "array"

def test__treat_descriptive_statistics(spark_session: SparkSession):
    df = spark_session.createDataFrame(data=[
    {
        "id": 10,
        "label": 100

    }
])
    fields= ["id", "label"]
    df_count = df.count()
    df_count_distinct = df.distinct().count()
    res = _treat_descriptive_statistics(fields, df_count, df_count_distinct)
    assert len(res) == 4

def test__treat_returned_profilling():
    res = _treat_returned_profilling({'countFields': 2, 'countRows': 1, 'countRowsDistinct': 1, 'fields': ['id', 'label']})
    assert len(res) == 1

def test__get_field_count_metrics(spark_session: SparkSession):
    df = spark_session.createDataFrame(data=[
    {
        "id": 10,
        "label": 100

    }
])
    field_data = df
    df_count = df.count()
    calc_result = dict()
    res = _get_field_count_metrics(field_data, df_count, calc_result)
    assert len(res) == 5

def test__calc_percentage_ratio_from_n1_to_n2():
    res = _calc_percentage_ratio_from_n1_to_n2(11, 3)
    assert res == 366.67

def test__get_field_distribution_metric(spark_session: SparkSession):
    df = spark_session.createDataFrame(data=[
    {
        "id": 10,
        "label": 100

    }
])
    field_data = df
    field = "id"
    field_type = "int"
    df_count = df.count()
    calc_result = {"distribution":[]}

    res = _get_field_distribution_metric(field_data, field, field_type, df_count, calc_result)
    assert len(res) == 10

def test__treat_boolean_distribution(spark_session: SparkSession):
    df = spark_session.createDataFrame(data=[
    {
        "id": 10,
        "label": 100

    }
])
    dist = df
    field = "id"
    df_count = df.count()
    calc_result = []

    res = _treat_boolean_distribution(df_count, dist, field, calc_result)
    assert len(res) == 1

def test__treat_numeric_distribution(spark_session: SparkSession):
    df = spark_session.createDataFrame(data=[
    {
        "id": 10,
        "label": 100

    }
])

    dist = df
    field = "id"
    distribution = []

    res = _treat_numeric_distribution(dist, field, distribution)
    assert len(res) == 10

def test__treat_string_distribution(spark_session: SparkSession):
    df = spark_session.createDataFrame(data=[
    {
        "id": 10,
        "label": 100

    }
])

    dist = df
    field = "id"
    distribution = []

    res = _treat_string_distribution(df.count(), dist, field, distribution)
    assert len(res) == 1

def test__treat_timestamp_distribution(spark_session: SparkSession):
    df = spark_session.createDataFrame(data=[
    {
        "id": 10,
        "label": 100

    }
])

    dist = df
    field = "id"
    distribution = []

    res = _treat_timestamp_distribution(df.count(), dist, field, distribution)
    assert len(res) == 4

def test__treat_default_distribution(spark_session: SparkSession):
    df = spark_session.createDataFrame(data=[
    {
        "id": 10,
        "label": 100

    }
])

    dist = df
    field = "id"
    distribution = []
    res = _treat_default_distribution(df.count(), dist, field, distribution)
    assert len(res) == 1
