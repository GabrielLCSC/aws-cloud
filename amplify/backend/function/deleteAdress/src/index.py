import boto3
import os
import json

dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('STORAGE_ADRESSES_NAME')
table = dynamodb.Table(table_name)

def response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Methods": "OPTIONS,DELETE,POST"
        },
        "body": json.dumps(body)
    }

def handler(event, context):
    try:
        print("[deleteAddress] Event received:", event)

        user_id = (
            event['requestContext']['identity']
            ['cognitoAuthenticationProvider']
            .split(":CognitoSignIn:")[1]
            .split("/")[0]
        )

        if not user_id:
            return response(401, {"message": "Utilisateur non authentifié."})

        body = json.loads(event.get("body", "{}"))
        address_id = body.get("id")

        if not address_id:
            return response(400, {"message": "L'identifiant de l'adresse est requis."})

        result = table.get_item(Key={"id": address_id})
        item = result.get("Item")

        if not item:
            return response(404, {"message": "Adresse non trouvée."})

        if item["user_id"] != user_id:
            return response(403, {"message": "Action non autorisée pour cette adresse."})

        table.delete_item(Key={"id": address_id})

        return response(200, {"message": "Adresse supprimée avec succès."})

    except Exception as e:
        print("[deleteAddress ERROR]", str(e))
        return response(500, {"message": "Erreur serveur."})
