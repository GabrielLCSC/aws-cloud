import json
import boto3
import bcrypt
import os

dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('USER_TABLE', 'Users')
table = dynamodb.Table(table_name)

def handler(event, context):
    try:
        body = json.loads(event.get('body', '{}'))

        email = body.get('email')
        first_name = body.get('firstName')
        last_name = body.get('lastName')
        password = body.get('password')

        if not email or not first_name or not last_name or not password:
            return response(400, 'Champs manquants.')

        existing = table.get_item(Key={'email': email})
        if 'Item' in existing:
            return response(409, 'Un utilisateur avec cet email existe déjà.')

        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        hashed = hashed.decode('utf-8') 

        table.put_item(Item={
            'email': email,
            'firstName': first_name,
            'lastName': last_name,
            'passwordHash': hashed
        })

        return response(201, 'Utilisateur créé avec succès.')

    except Exception as e:
        print('[ERROR]', str(e))
        return response(500, 'Erreur serveur.')

def response(status_code, message):
    return {
        'statusCode': status_code,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Credentials': True,
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET',
            'Access-Control-Allow-Headers': 'Content-Type'
        },
        'body': json.dumps({'message': message})
    }
