# -*- coding: utf-8 -*-
"""Library to simplify working with S3."""
import boto3
from botocore.config import Config
import os

# noinspection PyPackageRequirements
from aws_lambda_powertools import Logger
from botocore.exceptions import ClientError

LOGGER = Logger(sampling_rate=float(os.environ["LOG_SAMPLING_RATE"]), level=os.environ["LOG_LEVEL"])


class S3Service:
    """Simplify S3 actions."""

    def __init__(self, region_name="eu-west-1"):
        """Initialize default AWS region name.

        :param region_name: default eu-west-1
        """
        self.__s3 = boto3.client(
            "s3", region_name=region_name, config=Config(retries={"max_attempts": 10, "mode": "adaptive"})
        )

    def upload(self, bucket, local_path, remote_path, extra_args=None):
        """Upload files from local path to target path on S3 bucket."""
        if extra_args is None:
            extra_args = {}
        try:
            self.__s3.upload_file(local_path, bucket, remote_path, ExtraArgs=extra_args)
            LOGGER.info(f"Uploaded file {local_path} into s3://{bucket}/{remote_path}")
        except ClientError:
            LOGGER.error(f"Failed to upload file {local_path} into s3://{bucket}/{remote_path}")
            raise

    def download(self, bucket, local_path, remote_path):
        """Download files from path in S3 bucket to local path."""
        try:
            self.__s3.download_file(bucket, remote_path, local_path)
            LOGGER.info(f"Downloaded file s3://{bucket}/{remote_path} into {local_path}")
        except ClientError:
            LOGGER.error("Failed to download file s3://{bucket}/{remote_path} into {local_path}")
            raise

    def list_files(self, bucket, prefix, page_size=1000):
        """List files using prefix path in S3 bucket."""
        try:
            token = None
            files = []
            while True:
                if token is None:
                    response = self.__s3.list_objects_v2(Bucket=bucket, Prefix=prefix, MaxKeys=page_size)
                else:
                    response = self.__s3.list_objects_v2(
                        Bucket=bucket,
                        Prefix=prefix,
                        MaxKeys=page_size,
                        ContinuationToken=token,
                    )
                if "Contents" in response.keys():
                    files.extend(file["Key"] for file in response["Contents"])
                if response["IsTruncated"]:
                    token = response["NextContinuationToken"]
                else:
                    break
            LOGGER.info(f"Found {len(files)} search results with prefix {prefix}")
            return files
        except ClientError:
            LOGGER.error(f"Failed to list files in bucket {bucket} with prefix {prefix}")
            raise

    def list_prefixes(self, bucket, delimiter, path_prefix="", page_size=1000):
        """List prefixes that are in path prefix in S3 bucket."""
        try:
            token = None
            prefixes = []
            while True:
                if token is None:
                    response = self.__s3.list_objects_v2(
                        Bucket=bucket,
                        Prefix=path_prefix,
                        Delimiter=delimiter,
                        MaxKeys=page_size,
                    )
                else:
                    response = self.__s3.list_objects_v2(
                        Bucket=bucket,
                        Prefix=path_prefix,
                        Delimiter=delimiter,
                        MaxKeys=page_size,
                        ContinuationToken=token,
                    )
                if "CommonPrefixes" in response.keys():
                    prefixes.extend(
                        prefix["Prefix"].replace(path_prefix, "").replace(delimiter, "")
                        for prefix in response["CommonPrefixes"]
                    )

                if response["IsTruncated"]:
                    token = response["NextContinuationToken"]
                else:
                    break
            LOGGER.info(f"Found {len(prefixes)} prefixes with delimiter {delimiter}")
            return prefixes
        except ClientError:
            LOGGER.error(f"Failed to list prefixes in bucket {bucket} with delimiter {delimiter}")
            raise

    def delete_object(self, bucket, key):
        """Delete file from S3 bucket."""
        try:
            self.__s3.delete_object(Bucket=bucket, Key=key)
            LOGGER.info(f"Deleted file s3://{bucket}/{key}")
        except ClientError as client_error:
            if client_error.response["Error"]["Code"] == "404":
                LOGGER.exception(f"Object not found: {bucket}, {key}")
            LOGGER.error(f"Failed to delete file s3://{bucket}/{key}")
            raise

    def delete_objects(self, bucket, keys):
        """Delete files from S3 bucket."""
        try:
            for idx in range(0, len(keys), 1000):
                objects = [{"Key": key} for key in keys[idx : idx + 1000]]
                self.__s3.delete_objects(Bucket=bucket, Delete={"Objects": objects})
            LOGGER.info(f"Deleted {len(keys)} objects from bucket {bucket}")
        except ClientError:
            LOGGER.error(f"Failed to delete objects from bucket {bucket}")
            raise

    def delete_prefix(self, bucket, prefix):
        """Delete all files from S3 bucket that have the same prefix."""
        LOGGER.info(f"Deleting prefix {prefix} from bucket {bucket}")
        keys = self.list_files(bucket, prefix)
        self.delete_objects(bucket, keys)
        LOGGER.info(f"Deleted prefix {prefix} from bucket {bucket}")

    def copy(self, source_bucket, source_key, target_bucket, target_key):
        # sourcery skip: raise-specific-error
        """Copy file from S3 bucket to another S3 location."""
        try:
            copy_source = {"Bucket": source_bucket, "Key": source_key}
            self.__s3.copy(copy_source, target_bucket, target_key)
        except ClientError as error:
            if error.response["Error"]["Code"] == "404":
                LOGGER.error(
                    f"Failed to copy objects s3://{source_bucket}/{source_key} -> s3://{target_bucket}/{target_key}"
                )

        except Exception as error:
            LOGGER.critical(f"Unexpected error in download_object function of s3 helper: {error}")
            raise Exception(f"Unexpected error in download_object function of s3 helper: {error}") from error

    def move_object(self, source_bucket, source_key, target_bucket, target_key):
        """Move file from S3 bucket to another S3 location."""
        try:
            self.copy(source_bucket, source_key, target_bucket, target_key)
            self.delete_object(source_bucket, source_key)
            LOGGER.info(f"Object moved s3://{source_bucket}/{source_key} -> s3://{target_bucket}/{target_key}")
        except ClientError:
            LOGGER.error(
                f"Failed to move object s3://{source_bucket}/{source_key} -> s3://{target_bucket}/{target_key}"
            )
            raise

    def move_objects(self, source_bucket, source_prefix, target_bucket, target_prefix):
        """Move files from S3 bucket to another S3 location."""
        try:
            LOGGER.info(
                f"Starting moving objects s3://{source_bucket}/{source_prefix} -> s3://{target_bucket}/{target_prefix}",
            )
            token = None
            while True:
                if token is None:
                    response = self.__s3.list_objects_v2(Bucket=source_bucket, Prefix=source_prefix, MaxKeys=1000)
                else:
                    response = self.__s3.list_objects_v2(
                        Bucket=source_bucket,
                        Prefix=source_prefix,
                        MaxKeys=1000,
                        ContinuationToken=token,
                    )
                if "Contents" in response.keys():
                    for file in response["Contents"]:
                        if file["Key"] == source_prefix:
                            continue
                        target_key = f"{file['Key'].replace(source_prefix, target_prefix)}"
                        self.move_object(source_bucket, file["Key"], target_bucket, target_key)
                if response["IsTruncated"]:
                    token = response["NextContinuationToken"]
                else:
                    break
            LOGGER.info(
                f"Finished moving objects s3://{source_bucket}/{source_prefix} -> s3://{target_bucket}/{target_prefix}",
            )
        except ClientError:
            LOGGER.error(
                "Failed to move objects s3://{source_bucket}/{source_prefix} -> s3://{target_bucket}/{target_prefix}"
            )
            raise
