from typing import Optional

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.api.v1.auth import require_admin
from app.api.v1.schemas.receipt import ReceiptAnalyzeResponse, ReceiptCreate, ReceiptRead
from app.db.session import get_db
from app.repositories import receipt_repository
from app.services import csv_service, review_service, vision_service

router = APIRouter(prefix="/receipts", tags=["receipts"], dependencies=[Depends(require_admin)])


@router.post("/analyze", response_model=ReceiptAnalyzeResponse)
async def analyze(image: UploadFile = File(...)):
    image_bytes = await image.read()
    mime_type = image.content_type or "image/jpeg"
    try:
        extracted = vision_service.analyze_receipt(image_bytes, mime_type)
    except vision_service.VisionAnalysisError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    needs_review = review_service.compute_needs_review(
        extracted["date"], extracted["vendor"], extracted["amount"], extracted["category"]
    )
    return ReceiptAnalyzeResponse(**extracted, needs_review=needs_review)


@router.post("", response_model=ReceiptRead, status_code=201)
def create_receipt(payload: ReceiptCreate, db: Session = Depends(get_db)):
    # needs_reviewはクライアントの申告を信用せず、保存直前の値からサーバー側で再計算する
    needs_review = review_service.compute_needs_review(
        payload.date, payload.vendor, payload.amount, payload.category
    )
    receipt = receipt_repository.create(
        db,
        receipt_date=payload.date,
        vendor=payload.vendor,
        amount=payload.amount,
        category=payload.category,
        memo=payload.memo,
        needs_review=needs_review,
    )
    return receipt


@router.get("", response_model=list[ReceiptRead])
def list_receipts(month: Optional[str] = Query(default=None), db: Session = Depends(get_db)):
    return receipt_repository.list_receipts(db, month=month)


@router.delete("/{receipt_id}", status_code=204)
def delete_receipt(receipt_id: int, db: Session = Depends(get_db)):
    receipt = receipt_repository.get(db, receipt_id)
    if receipt is None:
        raise HTTPException(status_code=404, detail="見つかりません")
    receipt_repository.delete(db, receipt)


@router.get("/export.csv")
def export_csv(month: Optional[str] = Query(default=None), db: Session = Depends(get_db)):
    receipts = receipt_repository.list_receipts(db, month=month)
    csv_bytes = csv_service.build_csv(receipts)
    filename = f"receipts_{month or 'all'}.csv"
    return Response(
        content=csv_bytes,
        media_type="text/csv; charset=utf-8",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
