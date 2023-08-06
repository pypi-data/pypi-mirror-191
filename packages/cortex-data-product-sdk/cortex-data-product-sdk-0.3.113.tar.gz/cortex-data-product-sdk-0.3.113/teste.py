from data_product_sdk.cortex_databricks.data_platform.loader_utils import (
    landing_to_bronze,
)

if __name__ == "__main__":
    landing_to_bronze(
        data_input_path="data_input_path",
        data_type="delta",
        data_pack_name="teste",
        dataset_name="teste2",
        insert_mode="appendf",
        schema_path=None,
        partition_columns=None,
        spark=None,
        read_options=None,
        write_options=None,
        profiling=False,
        infer_schema=False,
        reset_checkpoint=False,
        catalog_name=None,
        db_name=None,
        tbl_properties=None,
    )
