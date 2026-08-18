import json
from unittest.mock import MagicMock

import generate_upload_url


def test_generates_url_with_default_content_type(monkeypatch):
    mock_s3 = MagicMock()
    mock_s3.generate_presigned_url.return_value = "https://example.com/upload"
    monkeypatch.setattr(generate_upload_url, "s3", mock_s3)
    monkeypatch.setattr(generate_upload_url, "BUCKET_NAME", "my-bucket")

    response = generate_upload_url.lambda_handler({}, None)

    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    assert body["uploadUrl"] == "https://example.com/upload"
    assert body["fileKey"].endswith(".jpeg")

    params = mock_s3.generate_presigned_url.call_args.kwargs["Params"]
    assert params["Bucket"] == "my-bucket"
    assert params["ContentType"] == "image/jpeg"


def test_generates_url_with_custom_content_type(monkeypatch):
    mock_s3 = MagicMock()
    mock_s3.generate_presigned_url.return_value = "https://example.com/upload"
    monkeypatch.setattr(generate_upload_url, "s3", mock_s3)
    monkeypatch.setattr(generate_upload_url, "BUCKET_NAME", "my-bucket")

    response = generate_upload_url.lambda_handler(
        {"queryStringParameters": {"contentType": "image/png"}}, None
    )

    body = json.loads(response["body"])
    assert body["fileKey"].endswith(".png")


def test_returns_500_on_failure(monkeypatch):
    mock_s3 = MagicMock()
    mock_s3.generate_presigned_url.side_effect = RuntimeError("s3 error")
    monkeypatch.setattr(generate_upload_url, "s3", mock_s3)

    response = generate_upload_url.lambda_handler({}, None)

    assert response["statusCode"] == 500
    assert "s3 error" in response["body"]
