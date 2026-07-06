"""要確認フラグの計算。
ExpenseVBA(modReceiptOCR.bas)のAppendMissingFieldと同じ判定順序・文言に揃える
（日付→支払先→金額→勘定科目の順、「要確認: X・Yが未検出」形式）。
"""

_FIELD_ORDER = (
    ("date", "日付"),
    ("vendor", "支払先"),
    ("amount", "金額"),
    ("category", "勘定科目"),
)


def compute_needs_review(date: str, vendor: str, amount: int, category: str) -> str:
    values = {"date": date, "vendor": vendor, "amount": amount, "category": category}
    missing = [
        label
        for key, label in _FIELD_ORDER
        if (values[key] == 0 if key == "amount" else values[key] == "")
    ]
    if not missing:
        return ""
    return "要確認: " + "・".join(missing) + "が未検出"
