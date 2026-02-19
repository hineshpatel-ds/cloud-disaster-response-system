import json
import uuid
import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Incidents')

def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])

        incident_id = str(uuid.uuid4())
        
        item = {
            "incidentId": incident_id,
            "type": body.get("type"),
            "description": body.get("description"),
            "location": body.get("location"),
            "status": "OPEN",
            "volunteerId": None,
            "imageUrl": body.get("imageUrl"),
            "createdAt": datetime.utcnow().isoformat()
        }

        table.put_item(Item=item)

        return {
            "statusCode": 201,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "message": "Incident created successfully",
                "incidentId": incident_id
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": str(e)
            })
        }