from datetime import datetime, timezone

from app.models.receipt import Receipt
from app.services.csv_service import build_csv


def _make_receipt(**overrides) -> Receipt:
    defaults = dict(
        id=1,
        receipt_date="2026-07-06",
        vendor="テスト商店",
        amount=1000,
        category="交通費",
        memo="テスト",
        needs_review="",
        source="web",
        created_at=datetime(2026, 7, 6, 12, 0, 0, tzinfo=timezone.utc),
    )
    defaults.update(overrides)
    return Receipt(**defaults)


def test_csv_headers_and_order():
    csv_bytes = build_csv([_make_receipt()])
    text = csv_bytes.decode("utf-8-sig")
    lines = text.strip().splitlines()
    assert lines[0] == "取込日時,領収書日付,支払先,金額,勘定科目,摘要,元ファイル名,要確認"
    assert "(Web取込)" in lines[1]


def test_csv_has_utf8_bom():
    csv_bytes = build_csv([])
    assert csv_bytes.startswith("\ufeff".encode("utf-8"))
