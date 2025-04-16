import boto3
import os
import json
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('STORAGE_NASAAPOD_NAME')
table = dynamodb.Table(table_name)

def response(status_code, body):
    return {
        'statusCode': status_code,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,GET',
        },
        'body': json.dumps(body)
    }

def handler(event, context):
    try:
        print("[getApodData] Event received:", event)

        user_id = event['requestContext']['identity']['cognitoAuthenticationProvider'].split(':CognitoSignIn:')[1].split('/')[0]
        print(f"[getApodData] Authenticated user_id: {user_id}")
        data = table.scan()
        items = data.get('Items', [])

        items.sort(key=lambda x: x.get('date', ''), reverse=True)

        return response(200, items)

    except Exception as e:
        print("[getApodData ERROR]", str(e))
        return response(500, { "message": "Erreur serveur." })
