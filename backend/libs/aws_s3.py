import io

import boto3
from boto3.s3.transfer import TransferConfig
from botocore.exceptions import ClientError 


class AwsS3:
    GB = 1024 ** 3

    def __init__(self):
        self.s3_client = None
        self.config = TransferConfig(multipart_threshold=5 * self.GB)

    def connect(self, region_name=None, api_version=None, use_ssl=True, verify=None, endpoint_url=None,
                aws_access_key_id=None, aws_secret_access_key=None, aws_session_token=None, config=None):
        """
        Args:
            region_name: The name of the AWS region. Defaults to None.
            api_version: The version of the AWS API to use. Defaults to None.
            use_ssl: Whether to use SSL encryption when connecting. Defaults to True.
            verify: Set to False to disable SSL certificate verification. Defaults to None.
            endpoint_url: The URL of the AWS endpoint to connect to. Defaults to None.
            aws_access_key_id: The AWS access key ID to use for authentication. Defaults to None.
            aws_secret_access_key: The AWS secret access key to use for authentication. Defaults to None.
            aws_session_token: The AWS session token to use for authentication. Defaults to None.
            config: Additional configuration options. Defaults to None.

        """

        self.s3_client = boto3.client('s3', region_name=region_name, api_version=api_version, use_ssl=use_ssl,
                                        verify=verify, endpoint_url=endpoint_url, aws_access_key_id=aws_access_key_id,
                                        aws_secret_access_key=aws_secret_access_key,
                                        aws_session_token=aws_session_token, config=config)

    def upload_file(self, bucket, file_obj, object_name):
        """
        Uploads a file object to a specified bucket with a specified object name.

        Args:
            bucket (str): The name of the bucket where the file will be uploaded.
            file_obj (file-like object): The file object to be uploaded.
            object_name (str): The name of the object in the bucket.

        """
        try:
            self.s3_client.upload_fileobj(file_obj, bucket, object_name, Config=self.config)
        except ClientError as error:
            raise error

    def download_file(self, bucket, object_name):
        """
        Args:
            bucket: A string representing the name of the S3 bucket where the file is located.
            object_name: A string representing the name of the file to be downloaded from the bucket.

        Returns:
            A BytesIO object containing the downloaded file data. Returns None if there's an error during the download or if the file doesn't exist.
        """

        try:
            file = io.BytesIO()
            self.s3_client.download_fileobj(bucket, object_name, file, Config=self.config)
            file.seek(0)
            return file
        except ClientError as error:
                raise error

