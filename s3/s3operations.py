import logging
import boto3
import json
from botocore.exceptions import ClientError
from boto3.s3.transfer import TransferConfig

def create_bucket(bucket_name, region=None):
    """Create an S3 bucket in a specified region

    If a region is not specified, the bucket is created in the S3 default
    region (us-east-1).

    :param bucket_name: Bucket to create
    :param region: String region to create bucket in, e.g., 'us-west-2'
    :return: True if bucket created, else False
    """

    # Create bucket
    try:
        if region is None:
            s3_client = boto3.client('s3')
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client = boto3.client('s3', region_name=region)
            location = {'LocationConstraint': region}
            s3_client.create_bucket(Bucket=bucket_name,
                                    CreateBucketConfiguration=location)
    except ClientError as e:
        logging.error(e)
        return False
    return True

def setBucketPolicy(bucket_name):
    #Instantiate bucketname
    bucketname = bucket_name

    #Define Bucket Policy
    bucket_policy = {
        'Version': '2012-10-17',
        'Statement': [{
            'Sid': 'AddPerm',
            'Effect': 'Allow',
            'Principal': '*',
            'Action': ['s3:GetObject'],
            'Resource': 'arn:aws:s3:::' + bucketname + '/*'
        }]
    }

    # Convert the policy from JSON dict to string
    bucket_policy = json.dumps(bucket_policy)

    # Set the new policy
    try:
        s3 = boto3.client('s3')
        s3.put_bucket_policy(Bucket=bucket_name, Policy=bucket_policy)
    except ClientError as e:
        logging.error(e)
        return False
    return True

def get_bucket_acl(bucket_name):
    """Retrieve the access control list of an Amazon S3 bucket

    :param bucket_name: string
    :return: Dictionary defining the bucket's access control list consisting
     of owner and grants. If error, return None.
    """

    # Retrieve the bucket ACL
    s3 = boto3.client('s3')
    try:
        response = s3.get_bucket_acl(Bucket=bucket_name)
    except ClientError as e:
        # AllAccessDisabled error == bucket not found
        logging.error(e)
        return None

    # Return both the Owner and Grants keys
    # The Owner and Grants settings together form the Access Control Policy.
    # The Grants alone form the Access Control List.
    return {'Owner': response['Owner'], 'Grants': response['Grants']}

def putBucketACL(bucket_name):
    s3 = boto3.resource('s3')
    bucket_acl = s3.BucketAcl(bucket_name)

    #Grant ACL to the Bucket
    try:
        response = bucket_acl.put(
        ACL='public-read')
        #AccessControlPolicy={},
        #GrantFullControl='string',
        #GrantRead='string',
        #GrantReadACP='string',
        #GrantWrite='string',
        #GrantWriteACP='string'
    except ClientError as e:
        logging.error(e)
        return False
    return True

def list_bucket():
    """List all the existing buckets for the AWS account."""

    # Retrieve the list of existing buckets
    s3 = boto3.client('s3')
    try:
        response = s3.list_buckets()
        # Output the bucket names
        print('Existing buckets:')
        for bucket in response['Buckets']:
            print({bucket["Name"]})
    except ClientError as e:
        logging.error(e)
        return False
    return True

def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3 = boto3.client('s3')
    try:
        response = s3.upload_file(file_name, bucket, object_name)
        #s3_client.upload_file(
        #    file_name, bucket, object_name,
        #    Callback=ProgressPercentage(file_name))"""
    except ClientError as e:
        logging.error(e)
        return False
    return True

def download_file(bucket, object_name, file_name):
    """Download a file to from S3 bucket

    :param bucket: Bucket to download from
    :param object_name: S3 object name.
    :param file_name: File to save the file
    """
    s3 = boto3.client('s3')
    try:
        s3.download_file(bucket, object_name, file_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

def upload_file_multipart_transfer(file_name, bucket, object_name=None):
    # Set the desired multipart threshold value (5GB)
    GB = 1024 ** 3
    config = TransferConfig(multipart_threshold=5*GB, max_concurrency=5)

    # Perform the transfer
    s3 = boto3.client('s3')
    try:
        s3.upload_file(file_name, bucket, object_name, Config=config)
    except ClientError as e:
        logging.error(e)
        return False
    return True

def list_files(bucket_name):
    """List files in S3 bucket

    :param bucket: Bucket to list the Files
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)
    for obj in bucket.objects.all():
        print(obj.key)