import json
import uuid
import boto3
from datetime import datetime
import os

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Incidents')
sns = boto3.client('sns')

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

        topic_arn = os.environ.get("SNS_TOPIC_ARN")

        sns.publish(
            TopicArn=topic_arn,
            Message=json.dumps({
                "incidentId": incident_id,
                "type": body.get("type"),
                "location": body.get("location"),
                "status": "OPEN"
            }),
            Subject="New Disaster Incident Reported"
        )

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