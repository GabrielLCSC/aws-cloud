import boto3
import os
import sys

dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('STORAGE_USERS_NAME', 'users')
table = dynamodb.Table(table_name)

def handler(event, context):
    print(table_name)
    print("Python version:", sys.version)
    try:
        print("[PostConfirmation] event received:", event)

        user_id = event.get('user_id')
        sub = event.get('sub')
        email = event.get('email')
        first_name = event.get('first_name')
        last_name = event.get('last_name')
        
        
        print(email)
        print(user_id)
        print(first_name)
        print(last_name)

        existing = table.get_item(Key={'id': user_id})
        if 'Item' in existing:
            print(f"[PostConfirmation] User {user_id} already exists in DB")
            return event

        table.put_item(Item={
            'id': sub,
            'email': email,
            'user_id': user_id,
            'firstName': first_name,
            'lastName': last_name,
            'birthDate': None,
            'gender': None,
            'politicalSide': None,
            'size': None
        })

        print(f"[PostConfirmation] User {email} created in DynamoDB")
        print(event)
        return event

    except Exception as e:
        print("[PostConfirmation ERROR]", str(e))
        raise e
