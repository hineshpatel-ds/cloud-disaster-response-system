import json
from unittest.mock import MagicMock

import create_incident


def _event(body):
    return {"body": json.dumps(body)}


def test_creates_incident_without_image(monkeypatch):
    mock_table = MagicMock()
    mock_sns = MagicMock()
    monkeypatch.setattr(create_incident, "table", mock_table)
    monkeypatch.setattr(create_incident, "sns", mock_sns)

    response = create_incident.lambda_handler(
        _event({"type": "Flood", "description": "Rising water", "location": "Halifax"}),
        None,
    )

    assert response["statusCode"] == 201
    body = json.loads(response["body"])
    assert "incidentId" in body

    put_item_kwargs = mock_table.put_item.call_args.kwargs
    item = put_item_kwargs["Item"]
    assert item["type"] == "Flood"
    assert item["status"] == "OPEN"
    assert item["imageUrl"] is None
    mock_sns.publish.assert_called_once()


def test_creates_incident_with_image_builds_url(monkeypatch):
    mock_table = MagicMock()
    mock_sns = MagicMock()
    monkeypatch.setattr(create_incident, "table", mock_table)
    monkeypatch.setattr(create_incident, "sns", mock_sns)
    monkeypatch.setattr(create_incident, "IMAGE_BUCKET_NAME", "my-bucket")

    response = create_incident.lambda_handler(
        _event({"type": "Fire", "description": "Smoke", "location": "Downtown", "fileKey": "abc.jpg"}),
        None,
    )

    assert response["statusCode"] == 201
    item = mock_table.put_item.call_args.kwargs["Item"]
    assert item["imageUrl"] == "https://my-bucket.s3.ca-central-1.amazonaws.com/abc.jpg"


def test_returns_500_on_failure(monkeypatch):
    mock_table = MagicMock()
    mock_table.put_item.side_effect = RuntimeError("dynamo down")
    monkeypatch.setattr(create_incident, "table", mock_table)
    monkeypatch.setattr(create_incident, "sns", MagicMock())

    response = create_incident.lambda_handler(
        _event({"type": "Flood", "description": "x", "location": "y"}),
        None,
    )

    assert response["statusCode"] == 500
    assert "dynamo down" in response["body"]
