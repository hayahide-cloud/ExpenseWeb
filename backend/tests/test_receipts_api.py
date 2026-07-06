from unittest.mock import patch


def test_create_and_list_receipt(client):
    response = client.post(
        "/api/v1/receipts",
        json={
            "date": "2026-07-06",
            "vendor": "テスト商店",
            "amount": 1000,
            "category": "交通費",
            "memo": "テスト",
        },
    )
    assert response.status_code == 201
    body = response.json()
    assert body["needs_review"] == ""

    list_response = client.get("/api/v1/receipts")
    assert list_response.status_code == 200
    assert len(list_response.json()) == 1


def test_create_receipt_with_missing_fields_flags_review(client):
    response = client.post(
        "/api/v1/receipts",
        json={"date": "", "vendor": "テスト商店", "amount": 0, "category": "交通費", "memo": ""},
    )
    assert response.status_code == 201
    body = response.json()
    assert "日付" in body["needs_review"]
    assert "金額" in body["needs_review"]


def test_needs_review_is_recomputed_server_side(client):
    response = client.post(
        "/api/v1/receipts",
        json={
            "date": "2026-07-06",
            "vendor": "テスト商店",
            "amount": 1000,
            "category": "交通費",
            "memo": "",
        },
    )
    assert response.json()["needs_review"] == ""


def test_month_filter(client):
    client.post(
        "/api/v1/receipts",
        json={"date": "2026-07-01", "vendor": "A", "amount": 100, "category": "雑費", "memo": ""},
    )
    client.post(
        "/api/v1/receipts",
        json={"date": "2026-06-01", "vendor": "B", "amount": 200, "category": "雑費", "memo": ""},
    )
    response = client.get("/api/v1/receipts", params={"month": "2026-07"})
    assert response.status_code == 200
    results = response.json()
    assert len(results) == 1
    assert results[0]["vendor"] == "A"


def test_delete_receipt(client):
    create_response = client.post(
        "/api/v1/receipts",
        json={
            "date": "2026-07-06",
            "vendor": "テスト商店",
            "amount": 1000,
            "category": "交通費",
            "memo": "",
        },
    )
    receipt_id = create_response.json()["id"]
    delete_response = client.delete(f"/api/v1/receipts/{receipt_id}")
    assert delete_response.status_code == 204
    list_response = client.get("/api/v1/receipts")
    assert list_response.json() == []


def test_delete_missing_receipt_returns_404(client):
    response = client.delete("/api/v1/receipts/999")
    assert response.status_code == 404


def test_analyze_endpoint_with_mocked_vision(client):
    fake_result = {
        "date": "2026-07-06",
        "vendor": "テスト商店",
        "amount": 500,
        "category": "雑費",
        "memo": "テスト",
    }
    with patch(
        "app.api.v1.routers.receipts.vision_service.analyze_receipt",
        return_value=fake_result,
    ):
        response = client.post(
            "/api/v1/receipts/analyze",
            files={"image": ("receipt.jpg", b"fake-image-bytes", "image/jpeg")},
        )
    assert response.status_code == 200
    body = response.json()
    assert body["vendor"] == "テスト商店"
    assert body["needs_review"] == ""


def test_export_csv(client):
    client.post(
        "/api/v1/receipts",
        json={
            "date": "2026-07-06",
            "vendor": "テスト商店",
            "amount": 1000,
            "category": "交通費",
            "memo": "",
        },
    )
    response = client.get("/api/v1/receipts/export.csv")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/csv")
    text = response.content.decode("utf-8-sig")
    assert "取込日時" in text
