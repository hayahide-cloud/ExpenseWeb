from app.services.review_service import compute_needs_review


def test_no_missing_fields():
    assert compute_needs_review("2026-07-06", "テスト商店", 1000, "交通費") == ""


def test_missing_date_only():
    assert compute_needs_review("", "テスト商店", 1000, "交通費") == "要確認: 日付が未検出"


def test_missing_multiple_fields_in_fixed_order():
    assert compute_needs_review("", "", 0, "交通費") == "要確認: 日付・支払先・金額が未検出"


def test_missing_category():
    assert compute_needs_review("2026-07-06", "テスト商店", 1000, "") == "要確認: 勘定科目が未検出"
