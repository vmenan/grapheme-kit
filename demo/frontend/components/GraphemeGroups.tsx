"use client";

import type { GraphemeGroup } from "@/lib/types";

// Same palette as GraphemeChips, applied per phonetic unit.
const PALETTE = [
  "bg-rose-100 text-rose-900 dark:bg-rose-950 dark:text-rose-200",
  "bg-amber-100 text-amber-900 dark:bg-amber-950 dark:text-amber-200",
  "bg-emerald-100 text-emerald-900 dark:bg-emerald-950 dark:text-emerald-200",
  "bg-sky-100 text-sky-900 dark:bg-sky-950 dark:text-sky-200",
  "bg-violet-100 text-violet-900 dark:bg-violet-950 dark:text-violet-200",
  "bg-teal-100 text-teal-900 dark:bg-teal-950 dark:text-teal-200",
];

function render(u: string): string {
  return u === " " ? "␣" : u === "" ? "∅" : u;
}

/**
 * Shows units grouped by the grapheme they belong to: the units that came from
 * (or compose into) one grapheme (e.g. வ் + அ) are boxed together. Single-unit
 * graphemes (pure consonants / vowels / spaces) are shown as a plain chip.
 */
export function GraphemeGroups({
  groups,
  emptyHint = "Output appears here.",
}: {
  groups: GraphemeGroup[];
  emptyHint?: string;
}) {
  if (!groups.length) {
    return <p className="text-sm text-slate-400">{emptyHint}</p>;
  }

  let unit = 0;
  return (
    <div className="flex flex-wrap items-center gap-2 indic">
      {groups.map((grp, gi) => {
        const multi = grp.units.length > 1;
        const chips = grp.units.map((u, ui) => (
          <span
            key={ui}
            className={"rounded px-2 py-0.5 text-lg " + PALETTE[unit++ % PALETTE.length]}
          >
            {render(u)}
          </span>
        ));
        return multi ? (
          <span
            key={gi}
            title={`from ${grp.source}`}
            className="flex items-center gap-1 rounded-lg border-2 border-slate-300 bg-slate-50 px-1.5 py-1 dark:border-slate-600 dark:bg-slate-800"
          >
            {chips}
          </span>
        ) : (
          <span key={gi} title={`from ${grp.source}`} className="flex">
            {chips}
          </span>
        );
      })}
    </div>
  );
}
