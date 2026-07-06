"use client";

import { useRouter } from "next/navigation";
import { apiFetch } from "@/lib/client-api";
import type { Receipt } from "@/types/api";

interface Props {
  receipts: Receipt[];
}

export default function ReceiptTable({ receipts }: Props) {
  const router = useRouter();

  async function handleDelete(id: number) {
    if (!confirm("削除しますか？")) return;
    await apiFetch(`/receipts/${id}`, { method: "DELETE" });
    router.refresh();
  }

  return (
    <table>
      <thead>
        <tr>
          <th>日付</th>
          <th>支払先</th>
          <th>金額</th>
          <th>勘定科目</th>
          <th>摘要</th>
          <th>要確認</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        {receipts.map((r) => (
          <tr key={r.id}>
            <td>{r.receipt_date}</td>
            <td>{r.vendor}</td>
            <td>{r.amount.toLocaleString()}</td>
            <td>{r.category}</td>
            <td>{r.memo}</td>
            <td style={{ color: r.needs_review ? "#b8860b" : undefined }}>{r.needs_review}</td>
            <td>
              <button type="button" onClick={() => handleDelete(r.id)}>
                削除
              </button>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
