import json
import boto3
import os
import urllib.request
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('STORAGE_NASAAPOD_NAME')
table = dynamodb.Table(table_name)

def response(status_code, body):
    return {
        "statusCode": status_code,
        "body": json.dumps(body)
    }

def delete_all_items():
    scan = table.scan()
    with table.batch_writer() as batch:
        for item in scan.get('Items', []):
            batch.delete_item(Key={'date': item['date']})

def handler(event, context):
    try:
        print("[updateApodData] Suppression des anciennes données")
        delete_all_items()

        print("[updateApodData] Récupération des données depuis l'API NASA")
        with urllib.request.urlopen('https://api.nasa.gov/planetary/apod?api_key=JmRKWvgaqZrhhPKGXSkZTr5szS1nRcLzORfQZhgZ') as res:
            raw_data = res.read()
            apod = json.loads(raw_data)

        item = {
            'date': apod.get('date', datetime.today().strftime('%Y-%m-%d')),
            'title': apod.get('title', ''),
            'description': apod.get('explanation', ''),
            'imageUrl': apod.get('hdurl') or apod.get('url', ''),
            'mediaType': apod.get('media_type', ''),
            'thumbnailUrl': apod.get('thumbnail_url', ''),
            'copyright': apod.get('copyright', 'NASA')
        }

        print(f"[updateApodData] Ajout du nouvel objet : {item}")
        table.put_item(Item=item)

        return response(200, {"message": "✅ Donnée APOD mise à jour avec succès.", "data": item})

    except Exception as e:
        print("[updateApodData ERROR]", str(e))
        return response(500, {"message": "❌ Erreur lors de la mise à jour des données APOD."})
