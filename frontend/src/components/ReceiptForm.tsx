"use client";

import { useState, type FormEvent } from "react";
import { CATEGORIES, type Category, type ReceiptCreate } from "@/types/api";

interface Props {
  initial: ReceiptCreate;
  needsReviewInitial: string;
  onSave: (data: ReceiptCreate) => Promise<void>;
}

export default function ReceiptForm({ initial, needsReviewInitial, onSave }: Props) {
  const [date, setDate] = useState(initial.date);
  const [vendor, setVendor] = useState(initial.vendor);
  const [amount, setAmount] = useState(initial.amount);
  const [category, setCategory] = useState<Category>(initial.category);
  const [memo, setMemo] = useState(initial.memo);
  const [saving, setSaving] = useState(false);

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setSaving(true);
    try {
      await onSave({ date, vendor, amount, category, memo });
    } finally {
      setSaving(false);
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      {needsReviewInitial && (
        <p style={{ background: "#fff2cc", padding: 8, borderRadius: 4 }}>{needsReviewInitial}</p>
      )}
      <label>
        日付
        <input type="date" value={date} onChange={(e) => setDate(e.target.value)} />
      </label>
      <label>
        支払先
        <input type="text" value={vendor} onChange={(e) => setVendor(e.target.value)} />
      </label>
      <label>
        金額
        <input
          type="number"
          value={amount}
          onChange={(e) => setAmount(Number(e.target.value))}
        />
      </label>
      <label>
        勘定科目
        <select value={category} onChange={(e) => setCategory(e.target.value as Category)}>
          <option value="">未選択</option>
          {CATEGORIES.map((c) => (
            <option key={c} value={c}>
              {c}
            </option>
          ))}
        </select>
      </label>
      <label>
        摘要（20文字以内）
        <input type="text" maxLength={20} value={memo} onChange={(e) => setMemo(e.target.value)} />
      </label>
      <button type="submit" disabled={saving}>
        {saving ? "保存中..." : "保存"}
      </button>
    </form>
  );
}
