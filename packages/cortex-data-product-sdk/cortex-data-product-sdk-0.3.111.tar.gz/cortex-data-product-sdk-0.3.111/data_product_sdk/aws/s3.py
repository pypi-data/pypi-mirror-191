import boto3


class AwsS3:
    def __init__(self, region_name: str = "us-east-1") -> None:
        self.client = boto3.client("s3", region_name=region_name)
