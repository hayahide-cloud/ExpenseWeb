# ExpenseWeb

`ExpenseVBA`（Excel VBA版・経費精算システム）のモバイル用コンパニオンWebアプリ。

スマホでレシートを撮影 → OpenAI Vision APIでOCR取込 → 明細として記録する。
ExpenseVBAを置き換えるものではなく**併用**する。月次集計・仕訳出力は引き続きExcel側（ExpenseVBA）で行う。

## 位置づけ

| | ExpenseVBA | ExpenseWeb |
|---|---|---|
| 環境 | 会社PC（Excel VBA） | スマホ（Webブラウザ） |
| 役割 | 月次集計・仕訳出力 | レシート撮影・OCR取込 |
| データ連携 | — | CSVエクスポート→Excelへ手動取込 |

## 技術スタック

Next.js（frontend） + FastAPI（backend） + PostgreSQL、Railwayでホスティング。
`hayahide-cloud/M.T.Works-hub`の`docs/RAILWAY_STACK_GUIDE.md`（紫電パレットで確立したパターン）に準拠。

## 構成

```
ExpenseWeb/
├── frontend/    Next.js App Router（撮影・一覧・CSVエクスポート画面）
├── backend/     FastAPI（OCR解析・DB・CSV出力API）
└── CLAUDE.md
```

## ローカル開発

### backend

```bash
docker run -d -e POSTGRES_PASSWORD=dev -p 5432:5432 postgres:16

cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

DATABASE_URL=postgresql://postgres:dev@localhost/expenseweb alembic upgrade head
DATABASE_URL=postgresql://postgres:dev@localhost/expenseweb \
  ADMIN_USERNAME=admin ADMIN_PASSWORD=devpass \
  OPENAI_API_KEY=sk-xxxx OPENAI_MODEL=gpt-5.4 \
  uvicorn app.main:app --reload
```

テスト（OpenAI呼び出しはモック、実課金なし）:

```bash
cd backend
pytest
```

### frontend

```bash
cd frontend
npm install
API_BASE_URL=http://localhost:8000/api/v1 \
  ADMIN_USERNAME=admin ADMIN_PASSWORD=devpass \
  npm run dev
```

ブラウザで `http://localhost:3000` を開き、Basic認証（admin / devpass）でログインする。

## Railwayへのデプロイ手順

`docs/RAILWAY_STACK_GUIDE.md`のRailwayセットアップ手順（3サービス構成）に準拠。

1. [railway.app](https://railway.app) で新規プロジェクト作成 → GitHubリポジトリ（`hayahide-cloud/ExpenseWeb`）を接続
2. サービスを3つ追加
   - **PostgreSQL**（Railwayテンプレート、自動作成）
   - **backend**（Root Directory: `backend`）
     - Build Command: `pip install -r requirements.txt && alembic upgrade head`
     - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
     - 環境変数: `DATABASE_URL=${{Postgres.DATABASE_URL}}`, `ADMIN_USERNAME`, `ADMIN_PASSWORD`, `OPENAI_API_KEY`, `OPENAI_MODEL=gpt-5.4`
   - **frontend**（Root Directory: `frontend`）
     - Build Command: `npm ci && npm run build`
     - Start Command: `npm start`
     - 環境変数: `API_BASE_URL=http://${{backend.RAILWAY_PRIVATE_DOMAIN}}/api/v1`, `ADMIN_USERNAME`（backendと同じ）, `ADMIN_PASSWORD`（backendと同じ）
3. frontendサービス → Settings → Networking → 「Generate Domain」で公開URLを発行
4. 発行されたURLにスマホのSafariでアクセスし、Basic認証でログイン後、「ホーム画面に追加」でアプリのように起動できる

## 使い方

1. `/capture` でレシート写真を撮影 →「解析する」→ 抽出結果を確認・修正 →「保存」
2. `/receipts` で一覧確認・月フィルタ・CSVエクスポート
3. エクスポートしたCSVを、ExpenseVBAの明細シートへコピー＆ペーストで取り込む（自動連携は未対応、手動ブリッジ）

## セキュリティ

- 単一オーナー専用の非公開ツール。全ページ・全APIをBasic認証で保護
- レシート画像はサーバーに保存しない（解析後は破棄。ストレージコスト増加を避けるため）
