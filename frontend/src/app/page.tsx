import Link from "next/link";

export default function HomePage() {
  return (
    <main style={{ maxWidth: 480, margin: "0 auto", padding: 16 }}>
      <h1>ExpenseWeb</h1>
      <p>ExpenseVBAのモバイル版コンパニオン。レシートを撮影してOCR取込します。</p>
      <p>
        <Link href="/capture">レシートを取り込む</Link>
      </p>
      <p>
        <Link href="/receipts">明細一覧・CSVエクスポート</Link>
      </p>
    </main>
  );
}
