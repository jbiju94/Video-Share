import boto3
import botocore
import datetime


class awsClient:
    BUCKET_NAME = "bitsassignment"
    ACCESS_KEY = "*******"
    SECRET_KEY = "********"
    REGION = "us-east-1"
    CDN_URL = "https://d1vmo6aju6p6pp.cloudfront.net/"

    def __init__(self, resource_name):
        self.client = boto3.client(
            resource_name,
            region_name=awsClient.REGION,
            aws_access_key_id=awsClient.ACCESS_KEY,
            aws_secret_access_key=awsClient.SECRET_KEY
        )

    def upload_file(self, file_object, acl="public-read"):
        self.client.upload_fileobj(file_object, awsClient.BUCKET_NAME, file_object.filename, ExtraArgs={
                "ACL": acl,
                "ContentType": file_object.content_type
            })

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
            file_object['Name'] = file_object['Key'].split('.')[0]
            file_list.update({file_object['Key']: file_object})
        return file_list

    def get_file_details(self, file_key):
        file_details = dict()
        response = dict()
        file_object = self.client.get_object(Bucket=awsClient.BUCKET_NAME, Key=file_key)
        file_details['Key'] = file_key
        file_details['URL'] = awsClient.CDN_URL + file_key
        file_details['Name'] = file_key.split('.')[0]
        file_details['ContentType'] = file_object['ContentType']
        file_details['UploadedOn'] = file_object['LastModified'].strftime("%B %d, %Y")
        response.update({0: file_details})
        return response

    def delete_file(self, file_key):
        resp = self.client.delete_object(Bucket=awsClient.BUCKET_NAME, Key=file_key)
        return resp['ResponseMetadata']['HTTPStatusCode']

"""if __name__ == "__main__":
    aws = awsClient('s3')
    files = aws.list_files()"""
