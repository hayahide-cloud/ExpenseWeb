"""明細CSVの生成。ExpenseVBAの明細シートと同じ8列・同じ順序にし、
Excelで日本語ヘッダーが文字化けしないようUTF-8 BOM付きで出力する
(WinHttpのUTF-8文字化け教訓と同種の注意点。docs/LESSONS_LEARNED.md参照)。
"""

import csv
import io

from app.models.receipt import Receipt

_HEADERS = ["取込日時", "領収書日付", "支払先", "金額", "勘定科目", "摘要", "元ファイル名", "要確認"]
_SOURCE_MARKER = "(Web取込)"


def build_csv(receipts: list[Receipt]) -> bytes:
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(_HEADERS)
    for r in receipts:
        writer.writerow(
            [
                r.created_at.strftime("%Y-%m-%d %H:%M:%S") if r.created_at else "",
                r.receipt_date,
                r.vendor,
                r.amount,
                r.category,
                r.memo,
                _SOURCE_MARKER,
                r.needs_review,
            ]
        )
    return ("\ufeff" + buffer.getvalue()).encode("utf-8")
