import boto3
import botocore


class awsClient:
    BUCKET_NAME = "bitsassignment"
    ACCESS_KEY = "AKIAIL3LLGV7C4BUGL6A1234"
    SECRET_KEY = "q5dHkyOx6GRV4MbcD1QVWnrTf8nDO8+cikdHz5iq1234"
    REGION = "us-east-1"
    CDN_URL = "https://d1vmo6aju6p6pp.cloudfront.net/"

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
        file_list = dict()
        file_objects = self.client.list_objects_v2(Bucket=awsClient.BUCKET_NAME)
        for file_object in file_objects["Contents"]:
            # Check for URL format : Object Key Trimming.
            file_object['URL'] = awsClient.CDN_URL + file_object['Key']
            file_list.update({file_object['Key']: file_object})
        return file_list

"""if __name__ == "__main__":
    aws = awsClient('s3')
    files = aws.list_files()"""
