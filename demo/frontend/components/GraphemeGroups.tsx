"use client";

import type { GraphemeGroup } from "@/lib/types";

// Same palette as GraphemeChips, applied per phonetic unit.
const PALETTE = [
  "bg-rose-100 text-rose-900",
  "bg-amber-100 text-amber-900",
  "bg-emerald-100 text-emerald-900",
  "bg-sky-100 text-sky-900",
  "bg-violet-100 text-violet-900",
  "bg-teal-100 text-teal-900",
];

function render(u: string): string {
  return u === " " ? "␣" : u === "" ? "∅" : u;
}

/**
 * Shows the decomposition grouped by source grapheme: the units that came from
 * one grapheme (e.g. வ → வ் + அ) are boxed together. Single-unit graphemes
 * (pure consonants / vowels / spaces) are shown as a plain chip.
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
            className="flex items-center gap-1 rounded-lg border-2 border-slate-300 bg-slate-50 px-1.5 py-1"
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
