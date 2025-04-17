import boto3
import os
import json

dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('STORAGE_USERS_NAME')
table = dynamodb.Table(table_name)

def response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,PUT"
        },
        "body": json.dumps(body)
    }

def handler(event, context):
    print("[updateUser] Event received:", event)
    try:
        print("[updateUser] Event received:", event)

        body = json.loads(event.get('body', '{}'))

        user_id = event['requestContext']['identity']['cognitoAuthenticationProvider'].split(':CognitoSignIn:')[1].split('/')[0]

        if not user_id:
            return response(401, {"message": "Utilisateur non authentifié."})

        allowed_fields = ['firstName', 'lastName', 'birthDate', 'gender', 'politicalSide', 'size', 'avatar']
        update_fields = {k: v for k, v in body.items() if k in allowed_fields}

        if not update_fields:
            return response(400, {"message": "Aucune donnée valide à mettre à jour."})

        update_expr = "SET " + ", ".join(f"{k}=:{k}" for k in update_fields)
        expr_values = {f":{k}": v for k, v in update_fields.items()}

        table.update_item(
            Key={'id': user_id},
            UpdateExpression=update_expr,
            ExpressionAttributeValues=expr_values
        )

        return response(200, {"message": "Utilisateur mis à jour avec succès."})

    except Exception as e:
        print("[updateUser ERROR]", str(e))
        return response(500, {"message": "Erreur serveur"})
