import boto3
import os

dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('STORAGE_USERS_NAME', 'users')
table = dynamodb.Table(table_name)

def handler(event, context):
    try:
        print("[PostConfirmation] event received:", event)

        attributes = event['request']['userAttributes']
        email = attributes.get('email')
        first_name = attributes.get('name')
        last_name = attributes.get('family_name')

        existing = table.get_item(Key={'email': email})
        if 'Item' in existing:
            print(f"[PostConfirmation] User {email} already exists in DB")
            return event

        table.put_item(Item={
            'email': email,
            'firstName': first_name,
            'lastName': last_name,
            'birthDate': None,
            'gender': None,
            'politicalSide': None,
            'size': None
        })

        print(f"[PostConfirmation] User {email} created in DynamoDB")
        return event

    except Exception as e:
        print("[PostConfirmation ERROR]", str(e))
        raise e
