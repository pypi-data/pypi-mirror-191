import boto3
import logging


class AwsGlueDatabrew:
    def __init__(self, region_name: str = "us-east-1") -> None:
        self.client = boto3.client("databrew", region_name=region_name)

    def start_job_run(self, *, job_name: str) -> dict:
        try:
            return self.client.start_job_run(Name=job_name)
        except Exception as e:
            logging.error(f"Error: {e}")
