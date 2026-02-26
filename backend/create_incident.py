import json
import uuid
import boto3
import os
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Incidents')

sns = boto3.client('sns')

SNS_TOPIC_ARN = os.environ.get("SNS_TOPIC_ARN")
IMAGE_BUCKET_NAME = os.environ.get("IMAGE_BUCKET_NAME")

def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])

        incident_id = str(uuid.uuid4())

        # Extract optional fileKey
        file_key = body.get("fileKey")

        image_url = None
        if file_key:
            image_url = f"https://{IMAGE_BUCKET_NAME}.s3.ca-central-1.amazonaws.com/{file_key}"

        item = {
            "incidentId": incident_id,
            "type": body.get("type"),
            "description": body.get("description"),
            "location": body.get("location"),
            "status": "OPEN",
            "volunteerId": None,
            "imageUrl": image_url,
            "createdAt": datetime.utcnow().isoformat()
        }

        table.put_item(Item=item)

        # Publish SNS notification
        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
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