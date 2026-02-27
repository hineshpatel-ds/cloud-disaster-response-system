import json
import boto3
import os
import uuid
from botocore.config import Config

s3 = boto3.client(
    "s3",
    region_name="ca-central-1",
    config=Config(signature_version="s3v4")
)

BUCKET_NAME = os.environ.get("IMAGE_BUCKET_NAME")

def lambda_handler(event, context):
    try:
        query = event.get("queryStringParameters") or {}
        content_type = query.get("contentType", "image/jpeg")

        file_extension = content_type.split("/")[-1]
        file_id = f"{uuid.uuid4()}.{file_extension}"

        upload_url = s3.generate_presigned_url(
            ClientMethod="put_object",
            Params={
                "Bucket": BUCKET_NAME,
                "Key": file_id,
                "ContentType": content_type
            },
            ExpiresIn=300
        )

        return {
            "statusCode": 200,
            "headers": { "Content-Type": "application/json" },
            "body": json.dumps({
                "uploadUrl": upload_url,
                "fileKey": file_id
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({ "error": str(e) })
        }