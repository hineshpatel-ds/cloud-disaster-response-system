import json
from decimal import Decimal
from unittest.mock import MagicMock

import get_incidents


def test_returns_items_from_scan(monkeypatch):
    mock_table = MagicMock()
    mock_table.scan.return_value = {
        "Items": [
            {"incidentId": "1", "type": "Flood", "status": "OPEN"},
            {"incidentId": "2", "type": "Fire", "status": "RESOLVED"},
        ]
    }
    monkeypatch.setattr(get_incidents, "table", mock_table)

    response = get_incidents.lambda_handler({}, None)

    assert response["statusCode"] == 200
    items = json.loads(response["body"])
    assert len(items) == 2
    assert items[0]["type"] == "Flood"


def test_encodes_decimal_values(monkeypatch):
    mock_table = MagicMock()
    mock_table.scan.return_value = {"Items": [{"incidentId": "1", "score": Decimal("4.5")}]}
    monkeypatch.setattr(get_incidents, "table", mock_table)

    response = get_incidents.lambda_handler({}, None)

    items = json.loads(response["body"])
    assert items[0]["score"] == 4.5


def test_returns_empty_list_when_no_items(monkeypatch):
    mock_table = MagicMock()
    mock_table.scan.return_value = {}
    monkeypatch.setattr(get_incidents, "table", mock_table)

    response = get_incidents.lambda_handler({}, None)

    assert response["statusCode"] == 200
    assert json.loads(response["body"]) == []


def test_returns_500_on_failure(monkeypatch):
    mock_table = MagicMock()
    mock_table.scan.side_effect = RuntimeError("scan failed")
    monkeypatch.setattr(get_incidents, "table", mock_table)

    response = get_incidents.lambda_handler({}, None)

    assert response["statusCode"] == 500
    assert "scan failed" in response["body"]
