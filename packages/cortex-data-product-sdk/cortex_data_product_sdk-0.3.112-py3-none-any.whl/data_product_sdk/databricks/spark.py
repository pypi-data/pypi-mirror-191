from pyspark.sql import SparkSession
from pyspark.sql.dataframe import DataFrame
from pyspark.sql.types import StructType
from typing import Any, List

import logging
import re


class DatabricksSpark:
    def __init__(self) -> None:
        pass

    @staticmethod
    def get_schema_hints(*, schema_json: dict) -> Any:
        try:
            if schema_json is None:
                return None
            fields = {
                field["name"]: field["type"]
                for field in schema_json["fields"]
                if isinstance(field["type"], str)
            }
            return ", ".join((f"{name} {type}" for name, type in fields.items()))
        except Exception as e:
            logging.error(f"Error: {e}")

    @staticmethod
    def get_spark_session(*, application_name: str) -> SparkSession:
        try:
            return (
                SparkSession.builder.appName(application_name)
                .config("spark.hadoop.hive.exec.dynamic.partition", "true")
                .config("spark.hadoop.hive.exec.dynamic.partition.mode", "nonstrict")
                .config("spark.sql.sources.partitionOverwriteMode", "dynamic")
                .enableHiveSupport()
                .getOrCreate()
            )
        except Exception as e:
            logging.error(f"Error: {e}")

    @staticmethod
    def read_data(
        *,
        data_path: str,
        data_type: str,
        read_options: dict = None,
        schema: StructType,
        spark_session: SparkSession,
    ):
        try:
            if read_options is None:
                read_options = dict()
            data_frame = (
                spark_session.readStream.format("cloudFiles")
                .option("cloudFiles.format", data_type)
                .options(**read_options)
            )
            data_frame = data_frame.schema(schema=schema)
            return data_frame.load(path=data_path)
        except Exception as e:
            logging.error(f"Error: {e}")

    @staticmethod
    def read_table(
        *,
        catalog_name: str,
        database_name: str,
        spark_session: SparkSession,
        table_name: str,
    ) -> DataFrame:
        try:
            table = f"{catalog_name}.{database_name}.{table_name}"
            return spark_session.readStream.format("delta").table(tableName=table)
        except Exception as e:
            logging.error(f"Error: {e}")

    @staticmethod
    def rename_invalid_columns(*, data_frame: DataFrame) -> DataFrame:
        try:
            invalid_characters = "[ ,;{}()\n\t=\\/']"
            for column in data_frame.columns:
                column_replace = re.sub(invalid_characters, "_", column)
                data_frame = data_frame.withColumnRenamed(column, column_replace)
            return data_frame
        except Exception as e:
            logging.error(f"Error: {e}")

    @staticmethod
    def set_catalog(
        *,
        catalog_name: str,
        spark_session: SparkSession,
    ) -> None:
        try:
            spark_session.sql(f"USE CATALOG {catalog_name}")
        except Exception as e:
            logging.error(f"Error: {e}")

    @staticmethod
    def set_table_modifiers(
        *,
        catalog_name: str,
        database_name: str,
        spark_session: SparkSession,
        table_modifiers: List[str],
        table_name: str,
    ) -> None:
        try:
            for table_modifier in table_modifiers:
                spark_session.sql(
                    f"GRANT MODIFY ON TABLE {catalog_name}.{database_name}.{table_name} TO `{table_modifier}`"
                )
        except Exception as e:
            logging.error(f"Error: {e}")

    @staticmethod
    def set_table_all_privileges(
        *,
        catalog_name: str,
        database_name: str,
        spark_session: SparkSession,
        table_modifiers: List[str],
        table_name: str,
    ) -> None:
        try:
            for table_modifier in table_modifiers:
                spark_session.sql(
                    f"GRANT ALL PRIVILEGES ON TABLE {catalog_name}.{database_name}.{table_name} TO `{table_modifier}`"
                )
                print(f"GRANTED ALL PRIVILEGES ON TABLE {catalog_name}.{database_name}.{table_name} TO `{table_modifier}`")
        except Exception as e:
            logging.error(f"Error: {e}")

    @staticmethod
    def set_table_owner(
        *,
        catalog_name: str,
        database_name: str,
        spark_session: SparkSession,
        table_name: str,
        table_owner: str,
    ) -> None:
        try:
            spark_session.sql(
                f"ALTER TABLE {catalog_name}.{database_name}.{table_name} OWNER TO `{table_owner}`"
            )
        except Exception as e:
            logging.error(f"Error: {e}")

    @staticmethod
    def set_properties(
        *,
        catalog_name: str,
        database_name: str,
        spark_session: SparkSession,
        table_name: str,
        table_properties: dict,
    ) -> None:
        try:
            table_properties_list = []
            for table_property in table_properties:
                table_properties_list.append(
                    f"'{table_property}' = '{table_properties[table_property]}'"
                )
            properties = ", ".join(table_properties_list)
            spark_session.sql(
                f"ALTER TABLE {catalog_name}.{database_name}.{table_name} SET TBLPROPERTIES ({properties})"
            )
        except Exception as e:
            logging.error(f"Error: {e}")

    @staticmethod
    def set_table_selectors(
        *,
        catalog_name: str,
        database_name: str,
        spark_session: SparkSession,
        table_name: str,
        table_selectors: List[str],
    ) -> None:
        try:
            for table_selector in table_selectors:
                spark_session.sql(
                    f"GRANT SELECT ON TABLE {catalog_name}.{database_name}.{table_name} TO `{table_selector}`"
                )
        except Exception as e:
            logging.error(f"Error: {e}")

    @staticmethod
    def write_table(
        *,
        catalog_name: str,
        checkpoint_location: str,
        data_frame: DataFrame,
        database_name: str,
        partition_columns: List[str] = None,
        table_name: str,
        write_options: dict = None,
    ):
        try:
            if partition_columns is None:
                partition_columns = list()
            if write_options is None:
                write_options = dict()
            stream = (
                data_frame.writeStream.trigger(once=True)
                .format("delta")
                .option("checkpointLocation", checkpoint_location)
                .options(**write_options)
            )
            return stream.toTable(
                tableName=f"{catalog_name}.{database_name}.{table_name}",
                partitionBy=partition_columns,
            )
        except Exception as e:
            logging.error(f"Error: {e}")
