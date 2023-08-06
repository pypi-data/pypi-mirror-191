import boto3
import logging


class AwsSqs:
    def __init__(self, region_name: str = "us-east-1") -> None:
        self.client = boto3.resource("sqs", region_name=region_name)

    def send_message(
        self,
        *,
        message_attributes: dict = None,
        message_body: str,
        queue_url: str,
    ):
        try:
            return self.client.send_message(
                MessageAttributes=message_attributes,
                MessageBody=message_body,
                QueueUrl=queue_url,
            )
        except Exception as e:
            logging.error(f"Error: {e}")
