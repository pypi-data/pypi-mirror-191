from typing import Any

import base64
import boto3
import json
import logging


class AwsSecretsManager:
    def __init__(self, region_name: str = "us-east-1") -> None:
        self.client = boto3.resource("secretsmanager", region_name=region_name)

    def get_secret_value(self, *, secret_id: str) -> Any:
        try:
            response = self.client.get_secret_value(SecretId=secret_id)
            if response and "SecretBinary" in response:
                return base64.b64decode(response["SecretBinary"])
            elif response and "SecretString" in response:
                return json.loads(response["SecretString"])
        except Exception as e:
            logging.error(f"Error: {e}")
