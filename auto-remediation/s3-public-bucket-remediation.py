import json
import boto3
import os


def lambda_handler(event, context):
    # Check config
    if os.environ.get('is_active', 'true').lower() == 'false':
        return {
            'statusCode': 200,
            'body': 's3 public bucket auto-remediation is triggered, but it set to not active'
        }

    # Retrieve bucket name
    bucketName = event['detail']['requestParameters']['bucketName']

    # Check whitelisted bucket
    whitelistedBuckets = os.environ.get('whitelisted', '')

    for whitelistedBucket in whitelistedBuckets.split(','):
        if whitelistedBucket == bucketName:
            # Return response since bucket whitelisted
            return {
                'statusCode': 200,
                'body': "bucket whitelisted"
            }

    # S3 public bucket remediation
    client = boto3.client('s3')
    response = client.get_public_access_block(
        Bucket=bucketName
    )

    publicAccessConfig = response['PublicAccessBlockConfiguration']
    if publicAccessConfig['BlockPublicAcls'] == False or publicAccessConfig['IgnorePublicAcls'] == False or publicAccessConfig['BlockPublicPolicy'] == False or publicAccessConfig['RestrictPublicBuckets'] == False:
        responseRemediation = client.put_public_access_block(
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
            'body': responseRemediation
        }

    # Return response
    return {
        'statusCode': 200,
        'body': response
    }
