// サーバーサイド(Server Component)専用。バックエンドに環境変数経由で直接アクセスする。
// この呼び出しはmiddleware.tsを経由しないため、Basic認証ヘッダーはここで明示的に組み立てる。
const API_BASE = process.env.API_BASE_URL ?? "http://localhost:8000/api/v1";
const USERNAME = process.env.ADMIN_USERNAME ?? "";
const PASSWORD = process.env.ADMIN_PASSWORD ?? "";

function authHeader(): string {
  return "Basic " + Buffer.from(`${USERNAME}:${PASSWORD}`).toString("base64");
}

export async function apiFetch<T>(path: string): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    cache: "no-store",
    headers: { Authorization: authHeader() },
  });
  if (!res.ok) {
    throw new Error(`API error: ${res.status}`);
  }
  return res.json();
}
