"use client";

import type { MetricRow } from "@/lib/types";

function fmt(v: number): string {
  return Number.isInteger(v) ? String(v) : v.toFixed(4);
}

const LEVEL_BADGE: Record<string, string> = {
  grapheme: "bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300",
  codepoint: "bg-slate-100 text-slate-600 dark:bg-slate-800 dark:text-slate-400",
};

/**
 * "All metrics" shows one row per family (the grapheme-level value only, to
 * keep the overview compact). Focusing one family expands to show its
 * grapheme value next to the standard code-point baseline - the "grapheme
 * metric complements chrF" comparison, made visual.
 */
export function MetricTable({
  rows,
  focus = "all",
}: {
  rows: MetricRow[];
  focus?: string;
}) {
  const visible =
    focus === "all" ? rows.filter((r) => r.level === "grapheme") : rows.filter((r) => r.family === focus);

  return (
    <div className="overflow-hidden rounded-lg border border-slate-200 dark:border-slate-700">
      <table className="w-full text-sm">
        <thead className="bg-slate-50 text-left text-xs uppercase tracking-wide text-slate-500 dark:bg-slate-800 dark:text-slate-400">
          <tr>
            <th className="px-4 py-2 font-medium">Metric</th>
            <th className="px-4 py-2 font-medium">Level</th>
            <th className="px-4 py-2 text-right font-medium">Value</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-100 dark:divide-slate-800">
          {visible.map((r) => (
            <tr key={r.key} className="hover:bg-slate-50 dark:hover:bg-slate-800/60">
              <td className="px-4 py-2 font-medium text-ink">{r.label}</td>
              <td className="px-4 py-2">
                <span
                  className={
                    "rounded px-2 py-0.5 text-xs font-medium " +
                    (LEVEL_BADGE[r.level] ?? "bg-slate-100 text-slate-600 dark:bg-slate-800 dark:text-slate-400")
                  }
                >
                  {r.level === "grapheme" ? "grapheme" : "unicode-point"}
                </span>
              </td>
              <td className="px-4 py-2 text-right font-mono tabular-nums text-ink">
                {fmt(r.value)}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
