"use client";

import type { MetricRow } from "@/lib/types";

function fmt(v: number): string {
  return Number.isInteger(v) ? String(v) : v.toFixed(4);
}

const LEVEL_BADGE: Record<string, string> = {
  grapheme: "bg-emerald-100 text-emerald-800",
  codepoint: "bg-slate-100 text-slate-600",
};

/**
 * Groups metric rows by family (chrF, chrF++, CER, Levenshtein) so the
 * grapheme-level value sits next to its code-point baseline - the paper's
 * "grapheme metric complements chrF" comparison, made visual.
 */
export function MetricTable({
  rows,
  focus = "all",
}: {
  rows: MetricRow[];
  focus?: string;
}) {
  const families = Array.from(new Set(rows.map((r) => r.family)));
  const visible = focus === "all" ? families : families.filter((f) => f === focus);

  return (
    <div className="overflow-hidden rounded-lg border border-slate-200">
      <table className="w-full text-sm">
        <thead className="bg-slate-50 text-left text-xs uppercase tracking-wide text-slate-500">
          <tr>
            <th className="px-4 py-2 font-medium">Metric</th>
            <th className="px-4 py-2 font-medium">Level</th>
            <th className="px-4 py-2 text-right font-medium">Value</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-100">
          {visible.map((family) =>
            rows
              .filter((r) => r.family === family)
              .map((r) => (
                <tr key={r.key} className="hover:bg-slate-50">
                  <td className="px-4 py-2 font-medium text-ink">{r.label}</td>
                  <td className="px-4 py-2">
                    <span
                      className={
                        "rounded px-2 py-0.5 text-xs font-medium " +
                        (LEVEL_BADGE[r.level] ?? "bg-slate-100 text-slate-600")
                      }
                    >
                      {r.level === "grapheme" ? "grapheme" : "unicode-point"}
                    </span>
                  </td>
                  <td className="px-4 py-2 text-right font-mono tabular-nums text-ink">
                    {fmt(r.value)}
                  </td>
                </tr>
              ))
          )}
        </tbody>
      </table>
    </div>
  );
}
