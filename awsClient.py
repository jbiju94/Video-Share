import boto3
import botocore


class awsClient:
    BUCKET_NAME = "VIDEO SHARE"
    ACCESS_KEY = "AKIAIO5FODNN7EXAMPLE"
    SECRET_KEY = "ABCDEF+c2L7yXeGvUyrPgYsDnWRRC1AYEXAMPLE"
    REGION = "us-east-1"

    def __init__(self, resource_name):
        self.client = boto3.client(
            resource_name,
            region_name=awsClient.REGION,
            aws_access_key_id=awsClient.ACCESS_KEY,
            aws_secret_access_key=awsClient.SECRET_KEY
        )

    def upload_file(self, file_name, file_title):
        self.client.upload_file(file_name, awsClient.BUCKET_NAME, file_title)

    def download_files(self, file_key, file_name):
        try:
            self.client.Bucket(awsClient.BUCKET_NAME).download_file(file_key, file_name)
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                return None
            else:
                raise

    def list_files(self):
        file_objects = self.client.list_objects_v2(Bucket=awsClient.BUCKET_NAME)
        for file_object in file_objects["Contents"]:
            print(file_object["Key"])
