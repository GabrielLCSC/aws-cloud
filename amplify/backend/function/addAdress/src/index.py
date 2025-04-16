import boto3
import os
import json
import uuid
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource("dynamodb")
table_name = os.environ.get("STORAGE_ADRESSES_NAME")
table = dynamodb.Table(table_name)

def response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST"
        },
        "body": json.dumps(body)
    }

def handler(event, context):
    try:
        print("[addAddress] Event received:", event)

        user_id = (
            event['requestContext']['identity']
            ['cognitoAuthenticationProvider']
            .split(":CognitoSignIn:")[1]
            .split("/")[0]
        )

        if not user_id:
            return response(401, {"message": "Utilisateur non authentifié."})

        body = json.loads(event.get("body", "{}"))

        allowed_fields = ["street", "city", "zipCode", "country"]
        address_data = {k: v for k, v in body.items() if k in allowed_fields}

        if not address_data:
            return response(400, {"message": "Données d'adresse manquantes ou invalides."})

        existing_addresses = table.query(
            IndexName="user_id-index",
            KeyConditionExpression=Key("user_id").eq(user_id)
        )

        for addr in existing_addresses.get("Items", []):
            if all(addr.get(field) == address_data.get(field) for field in allowed_fields):
                return response(409, {"message": "Cette adresse existe déjà."})

        address_id = str(uuid.uuid4())

        item = {
            "id": address_id,
            "user_id": user_id,
            **address_data
        }

        table.put_item(Item=item)

        return response(200, {
            "message": "Adresse ajoutée avec succès.",
            "address": item
        })

    except Exception as e:
        print("[addAddress ERROR]", str(e))
        return response(500, {"message": "Erreur serveur."})
