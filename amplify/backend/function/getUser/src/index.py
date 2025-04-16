import boto3
import os
import json

dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('STORAGE_USERS_NAME', 'users')
table = dynamodb.Table(table_name)
addresses_table_name = os.environ.get('STORAGE_ADRESSES_NAME', 'adresses')
addresses_table = dynamodb.Table(addresses_table_name)

def response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
        },
        "body": json.dumps(body)
    }

def handler(event, context):
    try:
        print("[getUser] Event received:", event)

        user_id = event['requestContext']['identity']['cognitoAuthenticationProvider'].split(':CognitoSignIn:')[1].split('/')[0]
        print(f"[getUser] user_id: {user_id}")

        result = table.get_item(Key={'id': user_id})
        print("[getUser] DynamoDB result:", result)

        if 'Item' not in result:
            return response(404, {"message": "Utilisateur non trouvé."})
        
        addresses_result = addresses_table.query(
            IndexName=None,
            KeyConditionExpression=boto3.dynamodb.conditions.Key('user_id').eq(user_id)
        )

        addresses = addresses_result.get('Items', [])
        print("[getUser] DynamoDB addresses result:", addresses)

        result['addresses'] = addresses

        return response(200, result['Item'])

    except Exception as e:
        print("[getUser ERROR]", str(e))
        return response(500, {"message": "Erreur serveur"})
