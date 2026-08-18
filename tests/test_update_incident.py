import json
from unittest.mock import MagicMock

import update_incident


def _event(incident_id, body):
    return {"pathParameters": {"id": incident_id}, "body": json.dumps(body)}


def test_updates_status_and_volunteer(monkeypatch):
    mock_table = MagicMock()
    monkeypatch.setattr(update_incident, "table", mock_table)

    response = update_incident.lambda_handler(
        _event("abc-123", {"status": "IN_PROGRESS", "volunteerId": "vol-1"}), None
    )

    assert response["statusCode"] == 200
    call = mock_table.update_item.call_args.kwargs
    assert call["Key"] == {"incidentId": "abc-123"}
    assert call["ExpressionAttributeValues"][":status"] == "IN_PROGRESS"
    assert call["ExpressionAttributeValues"][":volunteer"] == "vol-1"


def test_returns_500_on_failure(monkeypatch):
    mock_table = MagicMock()
    mock_table.update_item.side_effect = RuntimeError("update failed")
    monkeypatch.setattr(update_incident, "table", mock_table)

    response = update_incident.lambda_handler(
        _event("abc-123", {"status": "RESOLVED", "volunteerId": None}), None
    )

    assert response["statusCode"] == 500
    assert "update failed" in response["body"]


def test_returns_500_when_id_missing(monkeypatch):
    monkeypatch.setattr(update_incident, "table", MagicMock())

    response = update_incident.lambda_handler({"pathParameters": {}, "body": "{}"}, None)

    assert response["statusCode"] == 500
