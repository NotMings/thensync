import os
import boto3
from botocore.exceptions import NoCredentialsError


def upload_to_s3(file_path, s3_config):
    access_key_id = s3_config['access_key_id']
    secret_access_key = s3_config['secret_access_key']
    bucket = s3_config['bucket']
    endpoint = s3_config['endpoint']
    folder = s3_config['folder']
    default_region=s3_config['default_region']

    try:
        s3 = boto3.client(
            's3',
            region_name=default_region,
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key,
            endpoint_url=endpoint
        )
        key = f'{folder} / {os.path.basename(file_path)}'
        s3.upload_file(file_path, bucket, key)

        print(f'File uploaded successfully to {bucket}')
    except NoCredentialsError:
        print('Credentials not available')

def delete_from_s3(file_path, s3_config):
    access_key_id = s3_config['access_key_id']
    secret_access_key = s3_config['secret_access_key']
    bucket = s3_config['bucket']
    endpoint = s3_config['endpoint']
    folder = s3_config['folder']
    default_region=s3_config['default_region']

    try:
        s3 = boto3.client(
            's3',
            region_name=default_region,
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key,
            endpoint_url=endpoint
        )
        key = f'{folder} / {os.path.basename(file_path)}'
        s3.delete_object(Bucket=bucket, Key=key)

        print(f'File deleted successfully from {bucket}')
    except NoCredentialsError:
        print('Credentials not available')
