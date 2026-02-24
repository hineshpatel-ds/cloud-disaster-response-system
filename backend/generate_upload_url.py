import json
import boto3
import os
import uuid

s3 = boto3.client("s3")

BUCKET_NAME = os.environ.get("IMAGE_BUCKET_NAME")

def lambda_handler(event, context):
    try:
        file_id = str(uuid.uuid4()) + ".jpg"

        upload_url = s3.generate_presigned_url(
            ClientMethod="put_object",
            Params={
                "Bucket": BUCKET_NAME,
                "Key": file_id,
                "ContentType": "image/jpeg"
            },
            ExpiresIn=300
        )

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "uploadUrl": upload_url,
                "fileKey": file_id
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }