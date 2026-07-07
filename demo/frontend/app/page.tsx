import Link from "next/link";

const cards = [
  {
    href: "/graphemizer",
    title: "Graphemizer",
    blurb:
      "Segment text into visually-perceived grapheme clusters and see how the count differs from the raw unicode-point count - the gap character-level metrics miss.",
    cta: "Open graphemizer →",
  },
  {
    href: "/metrics",
    title: "Evaluation Metrics",
    blurb:
      "Compare a reference and a prediction with grapheme-level chrF / chrF++, CER and Levenshtein, each next to its standard unicode-point baseline. Paste text or upload two files.",
    cta: "Open metrics →",
  },
  {
    href: "/canonicalization",
    title: "Canonicalization",
    blurb:
      "Decompose complex scripts into their phonetic units, and compose those units back into a full grapheme - the two inverse operations behind grapheme normalization.",
    cta: "Open canonicalization →",
  },
];

export default function Home() {
  return (
    <div className="py-6">
      <h1 className="font-mono text-4xl font-bold tracking-tight text-ink">
        grapheme<span className="text-slate-400">Kit</span>
      </h1>
      <p className="mt-3 max-w-2xl text-lg text-slate-600 dark:text-slate-400">
        A grapheme-aware toolkit for segmenting, comparing, and evaluating text.
        One visually-perceived character is often several Unicode code points -
        these tools measure at the{" "}
        <span className="font-medium text-ink">grapheme</span> level,
        complementing character-based metrics like chrF.
      </p>

      <div className="mt-10 grid grid-cols-1 gap-5 md:grid-cols-3">
        {cards.map((c) => (
          <Link
            key={c.href}
            href={c.href}
            className="group rounded-xl border border-slate-200 p-6 transition hover:border-ink hover:shadow-sm dark:border-slate-800"
          >
            <h2 className="text-xl font-semibold text-ink">{c.title}</h2>
            <p className="mt-2 text-sm leading-relaxed text-slate-600 dark:text-slate-400">
              {c.blurb}
            </p>
            <span className="mt-4 inline-block text-sm font-medium text-ink group-hover:underline">
              {c.cta}
            </span>
          </Link>
        ))}
      </div>
    </div>
  );
}
