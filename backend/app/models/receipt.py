from datetime import datetime

from sqlalchemy import DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Receipt(Base):
    """ExpenseVBAの明細シートと同じ意味論のフィールドを持つ。
    未検出の値は空文字（0はamountのみ）で表し、NULLは使わない。
    """

    __tablename__ = "receipts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    receipt_date: Mapped[str] = mapped_column(String(10), nullable=False, default="")
    vendor: Mapped[str] = mapped_column(String(255), nullable=False, default="")
    amount: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    category: Mapped[str] = mapped_column(String(20), nullable=False, default="")
    memo: Mapped[str] = mapped_column(String(20), nullable=False, default="")
    needs_review: Mapped[str] = mapped_column(String(255), nullable=False, default="")
    source: Mapped[str] = mapped_column(String(50), nullable=False, default="web")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
