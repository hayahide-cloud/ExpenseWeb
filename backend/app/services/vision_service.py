"""OpenAI Vision APIでレシート画像から構造化データを抽出する。

プロンプトはExpenseVBA(src/modReceiptOCR.bas の BuildRequestBody)と同一文言を使い、
Excel側とWeb側で抽出品質を揃える。モデルは実機検証済みのgpt-5.4を既定値とする
(gpt-4o-miniは手書き数字の誤読が多く、gpt-5.5はmodel_not_foundで使用不可と判明済み)。
"""

import base64
import json
import re

import httpx

from app.config import get_settings

_PROMPT = (
    "あなたは経理担当者向けの経費精算アシスタントです。添付画像は日本の店舗レシートまたは領収書です。\n"
    "画像内の文字を1文字ずつ正確に読み取ってください。手書き文字・印影・かすれた文字は、推測でそれらしい値を作らず、\n"
    "確信が持てない場合は空文字にしてください。\n"
    "次の項目をJSONオブジェクト1つだけで出力してください。前後に説明文やコードブロック記号は付けないでください。\n"
    "date: 領収書に印字された日付（YYYY-MM-DD形式）\n"
    "vendor: 発行元の店舗名・会社名（手書きの宛名「様」宛先ではなく、レシート発行元を優先する）\n"
    "amount: 「合計」「ご請求金額」等と明記された税込合計金額（数値のみ、カンマ・円記号なし）。小計や内訳の金額と混同しない\n"
    "category: 次のいずれか1つ（交通費、会議費、消耗品費、交際費、通信費、雑費）。摘要から最も近いものを選ぶ\n"
    "memo: 購入品目・利用目的の要約（20文字以内）\n"
    "読み取れない項目は date と vendor と category は空文字、amount は 0 にしてください。"
)


class VisionAnalysisError(Exception):
    pass


def analyze_receipt(image_bytes: bytes, mime_type: str) -> dict:
    settings = get_settings()
    b64_image = base64.b64encode(image_bytes).decode("ascii")

    body = {
        "model": settings.openai_model,
        "temperature": 0,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": _PROMPT},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{mime_type};base64,{b64_image}",
                            "detail": "high",
                        },
                    },
                ],
            }
        ],
    }

    try:
        response = httpx.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {settings.openai_api_key}",
            },
            json=body,
            timeout=60.0,
        )
        response.raise_for_status()
    except httpx.HTTPError as exc:
        raise VisionAnalysisError(f"OpenAI API呼び出しに失敗しました: {exc}") from exc

    payload = response.json()
    try:
        content = payload["choices"][0]["message"]["content"]
    except (KeyError, IndexError) as exc:
        raise VisionAnalysisError(f"APIレスポンスの形式が不正です: {payload}") from exc

    match = re.search(r"\{.*\}", content, re.DOTALL)
    if not match:
        raise VisionAnalysisError(f"レスポンスにJSONが見つかりません: {content}")

    try:
        extracted = json.loads(match.group(0))
    except json.JSONDecodeError as exc:
        raise VisionAnalysisError(f"JSON解析に失敗しました: {content}") from exc

    return {
        "date": str(extracted.get("date", "") or ""),
        "vendor": str(extracted.get("vendor", "") or ""),
        "amount": int(extracted.get("amount", 0) or 0),
        "category": str(extracted.get("category", "") or ""),
        "memo": str(extracted.get("memo", "") or ""),
    }
