import os

os.environ.setdefault("AWS_DEFAULT_REGION", "ca-central-1")
os.environ.setdefault("SNS_TOPIC_ARN", "arn:aws:sns:ca-central-1:123456789012:test-topic")
os.environ.setdefault("IMAGE_BUCKET_NAME", "test-image-bucket")
