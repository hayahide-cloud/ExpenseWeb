"use client";

import { useRouter, useSearchParams } from "next/navigation";
import type { ChangeEvent } from "react";

export default function MonthFilter() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const month = searchParams.get("month") ?? "";

  function handleChange(e: ChangeEvent<HTMLInputElement>) {
    const value = e.target.value;
    router.push(value ? `/receipts?month=${value}` : "/receipts");
  }

  return (
    <label>
      対象月
      <input type="month" value={month} onChange={handleChange} />
    </label>
  );
}
