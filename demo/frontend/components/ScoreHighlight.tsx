"use client";

import type { MetricRow } from "@/lib/types";

function fmt(v: number): string {
  return Number.isInteger(v) ? String(v) : v.toFixed(2);
}

/**
 * Tiktokenizer "Token count" style summary: puts the headline grapheme-chrF
 * next to standard chrF so the contrast is immediate.
 */
export function ScoreHighlight({ rows }: { rows: MetricRow[] }) {
  const pick = (key: string) => rows.find((r) => r.key === key);
  const cards = [
    { row: pick("grapheme_chrf"), title: "chrF (grapheme)", strong: true },
    { row: pick("std_chrf"), title: "chrF (unicode-point)", strong: false },
    { row: pick("cer"), title: "CER (grapheme)", strong: false },
  ].filter((c) => c.row);

  return (
    <div className="grid grid-cols-1 gap-3 sm:grid-cols-3">
      {cards.map(({ row, title, strong }) => (
        <div
          key={title}
          className={
            "rounded-lg border p-4 " +
            (strong
              ? "border-emerald-300 bg-emerald-50 dark:border-emerald-800 dark:bg-emerald-950"
              : "border-slate-200 bg-white dark:border-slate-700 dark:bg-slate-900")
          }
        >
          <div className="text-xs uppercase tracking-wide text-slate-500 dark:text-slate-400">
            {title}
          </div>
          <div className="mt-1 font-mono text-3xl font-semibold tabular-nums text-ink">
            {fmt(row!.value)}
          </div>
        </div>
      ))}
    </div>
  );
}
