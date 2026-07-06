from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

Category = Literal["交通費", "会議費", "消耗品費", "交際費", "通信費", "雑費", ""]


class ReceiptAnalyzeResponse(BaseModel):
    date: str
    vendor: str
    amount: int
    category: Category
    memo: str = Field(max_length=20)
    needs_review: str


class ReceiptCreate(BaseModel):
    date: str = ""
    vendor: str = ""
    amount: int = 0
    category: Category = ""
    memo: str = Field(default="", max_length=20)


class ReceiptRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    receipt_date: str
    vendor: str
    amount: int
    category: str
    memo: str
    needs_review: str
    source: str
    created_at: datetime
