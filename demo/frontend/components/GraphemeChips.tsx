"use client";

// Tiktokenizer-style coloured chips, one per grapheme cluster.
const PALETTE = [
  "bg-rose-100 text-rose-900 dark:bg-rose-950 dark:text-rose-200",
  "bg-amber-100 text-amber-900 dark:bg-amber-950 dark:text-amber-200",
  "bg-emerald-100 text-emerald-900 dark:bg-emerald-950 dark:text-emerald-200",
  "bg-sky-100 text-sky-900 dark:bg-sky-950 dark:text-sky-200",
  "bg-violet-100 text-violet-900 dark:bg-violet-950 dark:text-violet-200",
  "bg-teal-100 text-teal-900 dark:bg-teal-950 dark:text-teal-200",
];

export function GraphemeChips({
  graphemes,
  emptyHint = "Output appears here.",
}: {
  graphemes: string[];
  emptyHint?: string;
}) {
  if (!graphemes.length) {
    return <p className="text-sm text-slate-400">{emptyHint}</p>;
  }
  return (
    <div className="flex flex-wrap gap-1.5 indic">
      {graphemes.map((g, i) => (
        <span
          key={i}
          className={
            "rounded px-2 py-0.5 text-lg " + PALETTE[i % PALETTE.length]
          }
          title={`#${i + 1}`}
        >
          {g === " " ? "␣" : g === "" ? "∅" : g}
        </span>
      ))}
    </div>
  );
}
