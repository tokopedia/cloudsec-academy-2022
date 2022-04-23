import json
import boto3
import os

def lambda_handler(event, context):
    # Check config
    if os.environ.get('is_active', 'true').lower() == 'false':
        return {
            'statusCode': 200,
            'body': 'EC2 overly permissive auto-remediation is triggered, but it set to not active'
        }
    
    # Get Security Group ID
    securityGroupID = event['detail']['requestParameters']['groupId']
    
    client = boto3.client('ec2')
    
    # Revoke overly permissive on port 22 SSH
    responsePort22 = client.revoke_security_group_ingress(
        CidrIp='0.0.0.0/0',
        FromPort=22,
        GroupId=securityGroupID,
        IpProtocol='TCP',
        ToPort=22
    )
    
    # Revoke overly permissive on port 3389 RDP
    responsePort3389 = client.revoke_security_group_ingress(
        CidrIp='0.0.0.0/0',
        FromPort=3389,
        GroupId=securityGroupID,
        IpProtocol='TCP',
        ToPort=3389
    )

    return {
        'statusCode': 200,
        'port22Response': responsePort22,
        'port3389Response': responsePort3389
    }
