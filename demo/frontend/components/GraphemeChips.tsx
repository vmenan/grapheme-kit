"use client";

// Tiktokenizer-style coloured chips, one per grapheme cluster.
const PALETTE = [
  "bg-rose-100 text-rose-900",
  "bg-amber-100 text-amber-900",
  "bg-emerald-100 text-emerald-900",
  "bg-sky-100 text-sky-900",
  "bg-violet-100 text-violet-900",
  "bg-teal-100 text-teal-900",
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
