from fastapi import FastAPI

from app.api.v1.routers.receipts import router as receipts_router

app = FastAPI(title="ExpenseWeb API")

app.include_router(receipts_router, prefix="/api/v1")


@app.get("/health")
def health():
    return {"status": "ok"}
