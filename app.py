import boto3
import json
import subprocess
from botocore.exceptions import ClientError
from typing import Any, Dict
from IPython.display import HTML
import uuid


class S3Manager:
    def __init__(self, region="us-east-1"):
        self.region = region

        self.s3 = boto3.client(
            "s3",
            region_name=region
        )

    # 1. Create bucket
    def create_bucket(self, bucket_name):
        try:
            if self.region == "us-east-1":
                self.s3.create_bucket(Bucket=bucket_name)
            else:
                self.s3.create_bucket(
                    Bucket=bucket_name,
                    CreateBucketConfiguration={
                        "LocationConstraint": self.region
                    }
                )
            print(f"Bucket created: {bucket_name}")

        except ClientError as e:
            print("Error creating bucket:", e)

    # 2. Get bucket policy (dictionary)
    def get_bucket_policy(self, bucket_name):
        try:
            response = self.s3.get_bucket_policy(Bucket=bucket_name)
            policy_dict = json.loads(response["Policy"])
            return policy_dict

        except ClientError as e:
            print("No policy or error:", e)
            return None

    # 3. Get bucket configuration (dictionary)
    def get_bucket_config(self, bucket_name):
        try:
            response = self.s3.get_bucket_location(Bucket=bucket_name)
            return response  # already a dict

        except ClientError as e:
            print("Error getting config:", e)
            return None

    # 4. Upload image
    def upload_image(self, bucket_name, file_path, key=None):
        try:
            if key is None:
                key = file_path.split("/")[-1]

            self.s3.upload_file(file_path, bucket_name, key)
            print(f"Uploaded {file_path} to {bucket_name}/{key}")

        except ClientError as e:
            print("Upload failed:", e)


if __name__ == "__main__":
    ACCESS_KEY = "YOUR_ACCESS_KEY"
    SECRET_KEY = "YOUR_SECRET_KEY"

    bucket_name = "my-unique-bucket-123456"

    s3_manager = S3Manager(ACCESS_KEY, SECRET_KEY)

    # Create bucket
    s3_manager.create_bucket(bucket_name)

    # Upload image
    s3_manager.upload_image(bucket_name, "image.jpg")

    # Get policy
    policy = s3_manager.get_bucket_policy(bucket_name)
    print("Policy:", policy)

    # Get config
    config = s3_manager.get_bucket_config(bucket_name)
    print("Config:", config)