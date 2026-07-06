import { apiFetch } from "@/lib/api";
import type { Receipt } from "@/types/api";
import MonthFilter from "@/components/MonthFilter";
import ReceiptTable from "@/components/ReceiptTable";

interface Props {
  searchParams: { month?: string };
}

export default async function ReceiptsPage({ searchParams }: Props) {
  const month = searchParams.month;
  const query = month ? `?month=${month}` : "";
  const receipts = await apiFetch<Receipt[]>(`/receipts${query}`);
  const exportHref = `/api/v1/receipts/export.csv${query}`;

  return (
    <main style={{ maxWidth: 800, margin: "0 auto", padding: 16 }}>
      <h1>明細一覧</h1>
      <MonthFilter />
      <p>
        <a href={exportHref}>CSVエクスポート</a>
      </p>
      <ReceiptTable receipts={receipts} />
    </main>
  );
}
