import boto3
import os
import json

dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('STORAGE_USERS_NAME', 'users')
table = dynamodb.Table(table_name)

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

        claims = event['requestContext']['authorizer']['jwt']['claims']
        user_id = claims['sub']
        print("[getUser] user_id:", user_id)

        result = table.get_item(Key={'id': user_id})
        print("result", result)
        if 'Item' not in result:
            return response(404, {"message": "Utilisateur non trouvé."})

        return response(200, result['Item'])

    except Exception as e:
        print("[getUser ERROR]", str(e))
        return response(500, {"message": "Erreur serveur"})
