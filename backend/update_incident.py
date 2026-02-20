import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Incidents')

def lambda_handler(event, context):
    try:
        incident_id = event["pathParameters"]["id"]
        body = json.loads(event["body"])

        new_status = body.get("status")
        volunteer_id = body.get("volunteerId")

        table.update_item(
            Key={"incidentId": incident_id},
            UpdateExpression="SET #s = :status, volunteerId = :volunteer",
            ExpressionAttributeNames={"#s": "status"},
            ExpressionAttributeValues={
                ":status": new_status,
                ":volunteer": volunteer_id
            }
        )

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "message": "Incident updated successfully"
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }