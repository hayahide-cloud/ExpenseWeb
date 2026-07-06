export type Category = "交通費" | "会議費" | "消耗品費" | "交際費" | "通信費" | "雑費" | "";

export const CATEGORIES: Category[] = ["交通費", "会議費", "消耗品費", "交際費", "通信費", "雑費"];

export interface ReceiptAnalyzeResponse {
  date: string;
  vendor: string;
  amount: number;
  category: Category;
  memo: string;
  needs_review: string;
}

export interface ReceiptCreate {
  date: string;
  vendor: string;
  amount: number;
  category: Category;
  memo: string;
}

export interface Receipt {
  id: number;
  receipt_date: string;
  vendor: string;
  amount: number;
  category: string;
  memo: string;
  needs_review: string;
  source: string;
  created_at: string;
}
