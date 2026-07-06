"use client";

import { useState, type ChangeEvent } from "react";
import { apiFetch } from "@/lib/client-api";
import type { ReceiptAnalyzeResponse } from "@/types/api";

interface Props {
  onAnalyzed: (result: ReceiptAnalyzeResponse) => void;
  onError: (message: string) => void;
}

export default function CameraCapture({ onAnalyzed, onError }: Props) {
  const [file, setFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  function handleFileChange(e: ChangeEvent<HTMLInputElement>) {
    const selected = e.target.files?.[0] ?? null;
    setFile(selected);
    setPreviewUrl(selected ? URL.createObjectURL(selected) : null);
  }

  async function handleAnalyze() {
    if (!file) return;
    setLoading(true);
    try {
      const formData = new FormData();
      formData.append("image", file);
      const result = await apiFetch<ReceiptAnalyzeResponse>("/receipts/analyze", {
        method: "POST",
        body: formData,
      });
      onAnalyzed(result);
    } catch (err) {
      onError(err instanceof Error ? err.message : "解析に失敗しました");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div>
      <input type="file" accept="image/*" capture="environment" onChange={handleFileChange} />
      {previewUrl && (
        // eslint-disable-next-line @next/next/no-img-element
        <img
          src={previewUrl}
          alt="レシートプレビュー"
          style={{ maxWidth: "100%", marginTop: 8, borderRadius: 4 }}
        />
      )}
      <button type="button" onClick={handleAnalyze} disabled={!file || loading} style={{ marginTop: 8 }}>
        {loading ? "解析中..." : "解析する"}
      </button>
    </div>
  );
}
