"use client";

// Tiktokenizer "model selector" style dropdown, repurposed to focus one metric.
export function MetricFocusSelect({
  families,
  value,
  onChange,
}: {
  families: string[];
  value: string;
  onChange: (v: string) => void;
}) {
  return (
    <select
      value={value}
      onChange={(e) => onChange(e.target.value)}
      className="rounded-md border border-slate-300 bg-white px-3 py-1.5 text-sm text-ink shadow-sm focus:border-ink focus:outline-none dark:border-slate-700 dark:bg-slate-900 dark:text-slate-100"
    >
      <option value="all">All metrics</option>
      {families.map((f) => (
        <option key={f} value={f}>
          {f}
        </option>
      ))}
    </select>
  );
}
