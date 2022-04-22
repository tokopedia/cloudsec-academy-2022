import json
import boto3
import os

def lambda_handler(event, context):
    # Check config
    if os.environ['is_active'].lower() == 'false':
        return {
            'statusCode': 200,
            'body': 's3 public bucket auto-remediation is triggered, but it set to not active'
        }
    
    # Retrieve bucket name
    bucketName = event['detail']['requestParameters']['bucketName']

    # Check whitelisted bucker
    whitelistedBuckets = os.environ.get('whitelisted','')
    
    for whitelistedBucket in whitelistedBuckets.split(','):
        if whitelistedBucket == bucketName:
            # Return response since bucket whitelisted
            return {
                'statusCode': 200,
                'body': "bucket whitelisted"
            }

    # S3 public bucket remediation
    client = boto3.client('s3')
    response = client.put_public_access_block(
        Bucket=bucketName,
        PublicAccessBlockConfiguration={
            'BlockPublicAcls': True,
            'IgnorePublicAcls': True,
            'BlockPublicPolicy': True,
            'RestrictPublicBuckets': True
        },
    )

    # Return response
    return {
        'statusCode': 200,
        'body': response
    }
