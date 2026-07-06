// ブラウザから /api/v1 に送る。Next.js rewritesでバックエンドに転送される。
// 認証ヘッダーはmiddleware.tsのBasic認証チャレンジで既にブラウザにキャッシュされている
// ものがそのまま自動的に付与されるため、ここで明示的に組み立てる必要はない。
const API_BASE = "/api/v1";

export async function apiFetch<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, init);
  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(`API error ${res.status}: ${text}`);
  }
  if (res.status === 204) {
    return undefined as T;
  }
  return res.json();
}
