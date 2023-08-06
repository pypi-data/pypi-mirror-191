import boto3
import logging


class AwsDynamoDb:
    def __init__(self, table_name: str, region_name: str = "us-east-1") -> None:
        self.resource = boto3.resource("dynamodb", region_name=region_name)
        self.table = self.resource.Table(table_name)

    def get_item(self, *, key: str) -> dict:
        try:
            return self.table.get_item(Key={"id": key})
        except Exception as e:
            logging.error(f"Error: {e}")

    def put_item(self, *, item: str) -> dict:
        try:
            return self.table.put_item(Item=item)
        except Exception as e:
            logging.error(f"Error: {e}")

    def query(self, *, index_name, key_condition_expression: dict) -> dict:
        try:
            return self.table.query(
                IndexName=index_name, KeyConditionExpression=key_condition_expression
            )
        except Exception as e:
            logging.error(f"Error: {e}")
