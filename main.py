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

    # 2. Upload file
    def upload(self, bucket_name, file_path, key=None):
        try:
            if key is None:
                key = file_path.split("/")[-1]

            self.s3.upload_file(file_path, bucket_name, key)
            print(f"Uploaded {file_path} to {bucket_name}/{key}")

        except ClientError as e:
            print("Upload failed:", e)
            

    # 3. put bucket configuration (dictionary)
    def put_bucket_config(self, bucket_name):
        try:
            with open('public_access_configuration.json', 'r') as file:
                public_access_block_configuration = json.load(file)
            self.s3.put_public_access_block(Bucket=bucket_name,PublicAccessBlockConfiguration=public_access_block_configuration)    

        except ClientError as e:
            print("Error getting config:", e)
            return None
        
    # 4. put bucket policy (dictionary)    
    def put_bucket_policy(self, bucket_name):
        try:
            with open('policy.json', 'r') as file:
                policy = json.load(file)
            response = self.s3.put_bucket_policy(Bucket=bucket_name, Policy=policy)
            print("Policy was added")

        except ClientError as e:
            print("No policy or error:", e)
            return None
        
    # 5. Download file from S3 bucket 
    def download_object_from_s3(self, bucket_name, key , local_file_path) :
  
    
        try:
            # Download the file to a local directory
            self.s3.download_file(bucket_name, key, local_file_path)
            print(f"{key} was downloded in {local_file_path}")
        except Exception as e:
            print(f"Error downloading or printing JSON file: {e}")

        
    # 6. Get bucket policy (dictionary)
    def get_bucket_policy(self, bucket_name):
        try:
            response = self.s3.get_bucket_policy(Bucket=bucket_name)
            policy_dict = json.loads(response["Policy"])
            return policy_dict

        except ClientError as e:
            print("No policy or error:", e)
            return None
    
    # 7. Get bucket configuration (dictionary)
    def get_bucket_config(self, bucket_name):
        try:
            response = self.s3.get_bucket_location(Bucket=bucket_name)
            return response  # already a dict

        except ClientError as e:
            print("Error getting config:", e)
            return None
        
    #8. add versioning    
    def set_versioning(self, bucket_name, enable=True):
        try:
            status = "Enabled" if enable else "Suspended"

            self.s3.put_bucket_versioning(
                Bucket=bucket_name,
                VersioningConfiguration={
                    "Status": status
                }
            )

            print(f"Versioning {status} for bucket: {bucket_name}")

        except ClientError as e:
            print("Error setting versioning:", e)

    #9.listing object in the bucket
    def list_objects(self, bucket_name, prefix=None):
        try:
            kwargs = {"Bucket": bucket_name}

            # Optional: filter by "folder"
            if prefix:
                kwargs["Prefix"] = prefix

            response = self.s3.list_objects_v2(**kwargs)

            if "Contents" not in response:
                print("No objects found.")
                return []

            objects = []
            for obj in response["Contents"]:
                key = obj["Key"]
                size = obj["Size"]
                print(f"{key} ({size} bytes)")
                objects.append(key)

            return objects

        except ClientError as e:
            print("Error listing objects:", e)
            return []
        
    #10. list versions
    def list_object_versions(self, bucket_name, prefix=None):
        try:
            kwargs = {"Bucket": bucket_name}

            if prefix:
                kwargs["Prefix"] = prefix

            paginator = self.s3.get_paginator("list_object_versions")

            versions_list = []

            for page in paginator.paginate(**kwargs):

                # Actual versions
                if "Versions" in page:
                    for v in page["Versions"]:
                        print(f"{v['Key']} | VersionId: {v['VersionId']} | Latest: {v['IsLatest']}")
                        versions_list.append(v)

                # Delete markers (important!)
                if "DeleteMarkers" in page:
                    for d in page["DeleteMarkers"]:
                        print(f"{d['Key']} | DELETE MARKER | VersionId: {d['VersionId']}")
                        versions_list.append(d)

            return versions_list

        except ClientError as e:
            print("Error listing object versions:", e)
            return []
        
    #11.deleting specific object in the bucket
    def delete_object(self, bucket_name, key):
        try:
            self.s3.delete_object(
                Bucket=bucket_name,
                Key=key
            )
            print(f"Deleted object: {key}")

        except ClientError as e:
            print("Error deleting object:", e)

    #12.empty and delete the bucket
    def empty_and_delete_bucket(self, bucket_name):
        try:
            # 1. Delete all object versions (handles versioned buckets too)
            paginator = self.s3.get_paginator("list_object_versions")

            for page in paginator.paginate(Bucket=bucket_name):

                # Delete normal versions
                if "Versions" in page:
                    for obj in page["Versions"]:
                        self.s3.delete_object(
                            Bucket=bucket_name,
                            Key=obj["Key"],
                            VersionId=obj["VersionId"]
                        )
                        print(f"Deleted version: {obj['Key']} ({obj['VersionId']})")

                # Delete delete markers
                if "DeleteMarkers" in page:
                    for obj in page["DeleteMarkers"]:
                        self.s3.delete_object(
                            Bucket=bucket_name,
                            Key=obj["Key"],
                            VersionId=obj["VersionId"]
                        )
                        print(f"Deleted marker: {obj['Key']} ({obj['VersionId']})")

            # 2. Delete remaining non-versioned objects (fallback)
            response = self.s3.list_objects_v2(Bucket=bucket_name)
            if "Contents" in response:
                for obj in response["Contents"]:
                    self.s3.delete_object(
                        Bucket=bucket_name,
                        Key=obj["Key"]
                    )
                    print(f"Deleted object: {obj['Key']}")

            # 3. Delete bucket itself
            self.s3.delete_bucket(Bucket=bucket_name)
            print(f"Bucket deleted: {bucket_name}")

        except ClientError as e:
            print("Error emptying/deleting bucket:", e)    
