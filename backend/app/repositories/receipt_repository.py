from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.receipt import Receipt


def create(db: Session, **fields) -> Receipt:
    receipt = Receipt(**fields)
    db.add(receipt)
    db.commit()
    db.refresh(receipt)
    return receipt


def list_receipts(db: Session, month: Optional[str] = None) -> list[Receipt]:
    stmt = select(Receipt).order_by(Receipt.created_at.desc())
    if month:
        stmt = stmt.where(Receipt.receipt_date.like(f"{month}-%"))
    return list(db.scalars(stmt))


def get(db: Session, receipt_id: int) -> Optional[Receipt]:
    return db.get(Receipt, receipt_id)


def delete(db: Session, receipt: Receipt) -> None:
    db.delete(receipt)
    db.commit()
