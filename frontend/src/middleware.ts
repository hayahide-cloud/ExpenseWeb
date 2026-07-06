import { NextRequest, NextResponse } from "next/server";

// このアプリは単一オーナー専用の非公開データを扱うため、
// 紫電パレットの「公開閲覧+管理者のみBasic認証」パターンとは異なり、
// 全ページ・全APIをBasic認証で保護する(訪問者の認証情報をそのまま
// バックエンドへ転送するので、ヘッダーの再構築は行わない)。
const REALM = "ExpenseWeb";

function isAuthorized(request: NextRequest): boolean {
  const authHeader = request.headers.get("authorization");
  if (!authHeader?.startsWith("Basic ")) return false;

  const decoded = Buffer.from(authHeader.slice(6), "base64").toString("utf-8");
  const separatorIndex = decoded.indexOf(":");
  if (separatorIndex === -1) return false;

  const username = decoded.slice(0, separatorIndex);
  const password = decoded.slice(separatorIndex + 1);

  return (
    username === process.env.ADMIN_USERNAME &&
    password === process.env.ADMIN_PASSWORD
  );
}

export function middleware(request: NextRequest) {
  if (isAuthorized(request)) {
    return NextResponse.next();
  }

  return new NextResponse("Authentication required", {
    status: 401,
    headers: { "WWW-Authenticate": `Basic realm="${REALM}"` },
  });
}

export const config = {
  matcher: ["/((?!_next/static|_next/image|favicon.ico|manifest.json).*)"],
};
