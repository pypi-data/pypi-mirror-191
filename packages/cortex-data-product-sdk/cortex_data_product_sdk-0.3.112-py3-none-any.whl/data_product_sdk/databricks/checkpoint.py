class DatabricksCheckpoint:
    def __init__(self) -> None:
        pass

    @staticmethod
    def get_checkpoint_location(
        *,
        bucket_name: str,
        data_pack_name: str,
        dataset_name: str,
        table_name: str,
    ):
        return f"s3://{bucket_name}/_databricks_checkpoint/{data_pack_name}/{dataset_name}/{table_name}"
