"use client";

import { useState } from "react";
import CameraCapture from "@/components/CameraCapture";
import ReceiptForm from "@/components/ReceiptForm";
import { apiFetch } from "@/lib/client-api";
import type { ReceiptAnalyzeResponse, ReceiptCreate } from "@/types/api";

export default function CapturePage() {
  const [analyzed, setAnalyzed] = useState<ReceiptAnalyzeResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [savedMessage, setSavedMessage] = useState<string | null>(null);
  const [resetKey, setResetKey] = useState(0);

  async function handleSave(data: ReceiptCreate) {
    await apiFetch("/receipts", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
    setSavedMessage("保存しました。次のレシートを撮影できます。");
    setAnalyzed(null);
    setError(null);
    setResetKey((k) => k + 1);
  }

  return (
    <main style={{ maxWidth: 480, margin: "0 auto", padding: 16 }}>
      <h1>レシート取込</h1>
      {savedMessage && <p style={{ color: "green" }}>{savedMessage}</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}
      {!analyzed && (
        <CameraCapture
          key={resetKey}
          onAnalyzed={(result) => {
            setAnalyzed(result);
            setSavedMessage(null);
          }}
          onError={(message) => setError(message)}
        />
      )}
      {analyzed && (
        <ReceiptForm
          initial={{
            date: analyzed.date,
            vendor: analyzed.vendor,
            amount: analyzed.amount,
            category: analyzed.category,
            memo: analyzed.memo,
          }}
          needsReviewInitial={analyzed.needs_review}
          onSave={handleSave}
        />
      )}
    </main>
  );
}
