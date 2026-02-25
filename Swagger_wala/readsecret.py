import boto3
import json
import os

def lambda_handler(event, context):
    secret_name = "uat/lambda/power-bi-automation"  
    aws_region = os.environ.get("AWS_REGION", "ap-south-1")  
    # Create a Secrets Manager client Make connection 
    client = boto3.client('secretsmanager', region_name=aws_region)
    try:
        response = client.get_secret_value(SecretId=secret_name)
        
        if 'SecretString' in response:
            secret = json.loads(response['SecretString'])

        # Access the specific secrets
        client_id = secret.get("client_id")
        client_secret = secret.get("client_secret")
        tenant_id = secret.get("tenant_id")

        # Log or return the secrets as necessary
        print("Client ID:", client_id)
        print("Client Secret:", client_secret)
        print("Tenant ID:", tenant_id)

        # Return success message
        return {
            'statusCode': 200,
            'body': json.dumps({
                'client_id': client_id,
                'client_secret': client_secret,
                'tenant_id': tenant_id
            })
        }

    except Exception as e:
        print(f"Error retrieving secret: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': f"Error retrieving secret: {str(e)}"
            })
        }