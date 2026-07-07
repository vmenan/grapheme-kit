"use client";

import { useEffect, useState } from "react";
import { getGraphemes } from "@/lib/api";
import type { GraphemesResponse } from "@/lib/types";
import { useDebounced } from "@/lib/useDebounced";
import { GraphemeChips } from "@/components/GraphemeChips";

const SAMPLE = "Hello வணக்கம் ආයුබෝවන් مَرْحَبًا שָׁלוֹם";

export default function GraphemizerPage() {
  const [text, setText] = useState(SAMPLE);
  const debounced = useDebounced(text);
  const [result, setResult] = useState<GraphemesResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!debounced.trim()) {
      setResult(null);
      return;
    }
    let cancelled = false;
    setLoading(true);
    setError(null);
    getGraphemes(debounced)
      .then((r) => !cancelled && setResult(r))
      .catch((e) => !cancelled && setError(String(e)))
      .finally(() => !cancelled && setLoading(false));
    return () => {
      cancelled = true;
    };
  }, [debounced]);

  const ratio =
    result && result.count > 0
      ? (result.codepoint_count / result.count).toFixed(2)
      : null;

  return (
    <div className="py-2">
      <h1 className="text-2xl font-bold text-ink">Graphemizer</h1>
      <p className="mt-1 text-sm text-slate-600 dark:text-slate-400">
        How graphemeKit clusters text into visually-perceived characters,
        compared with the raw unicode-point count.
      </p>

      <div className="mt-6 grid grid-cols-1 gap-6 lg:grid-cols-2">
        <div>
          <label className="mb-1 block text-xs font-semibold uppercase tracking-wide text-slate-500 dark:text-slate-400">
            Unicode input
          </label>
          <textarea
            value={text}
            onChange={(e) => setText(e.target.value)}
            rows={5}
            className="indic w-full resize-y rounded-lg border border-slate-300 bg-white p-3 text-xl text-ink focus:border-ink focus:outline-none dark:border-slate-700 dark:bg-slate-900 dark:text-slate-100 dark:placeholder-slate-500"
            placeholder="Type any text…"
          />
          <p className="mt-2 text-xs text-slate-400">
            {loading ? "Computing…" : "Updates as you type."}
          </p>

          {result && (
            <div className="mt-4 grid grid-cols-2 gap-3">
              <CountCard
                title="Graphemes"
                subtitle="graphemeKit"
                value={result.count}
                strong
              />
              <CountCard
                title="Unicode code points"
                subtitle="raw"
                value={result.codepoint_count}
              />
            </div>
          )}
          {ratio && (
            <p className="mt-3 text-sm text-slate-600 dark:text-slate-400">
              On average{" "}
              <span className="font-mono font-semibold text-ink">{ratio}</span>{" "}
              code points per grapheme - that gap is exactly what character-level
              metrics miss.
            </p>
          )}
        </div>

        <div className="space-y-5">
          {error && (
            <div className="rounded-md border border-rose-300 bg-rose-50 px-3 py-2 text-sm text-rose-800 dark:border-rose-800 dark:bg-rose-950 dark:text-rose-200">
              {error}
              <div className="mt-1 text-xs text-rose-500 dark:text-rose-400">
                Is the backend running at the configured API URL?
              </div>
            </div>
          )}

          {result && (
            <>
              <Section
                title="Grapheme clusters (graphemeKit)"
                subtitle={`${result.count} graphemes`}
              >
                <GraphemeChips graphemes={result.graphemes} />
              </Section>

              <Section
                title="Unicode code points (raw)"
                subtitle={`${result.codepoint_count} code points`}
              >
                <GraphemeChips graphemes={result.codepoints} />
                <p className="mt-2 text-xs text-slate-400">
                  Each box is one Unicode scalar; combining marks appear on
                  their own here, but the library keeps them inside one
                  grapheme above.
                </p>
              </Section>
            </>
          )}

          {!result && !error && (
            <p className="text-sm text-slate-400">Enter text to see the breakdown.</p>
          )}
        </div>
      </div>
    </div>
  );
}

function CountCard({
  title,
  subtitle,
  value,
  strong = false,
}: {
  title: string;
  subtitle: string;
  value: number;
  strong?: boolean;
}) {
  return (
    <div
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
        {value}
      </div>
      <div className="text-xs text-slate-400">{subtitle}</div>
    </div>
  );
}

function Section({
  title,
  subtitle,
  children,
}: {
  title: string;
  subtitle?: string;
  children: React.ReactNode;
}) {
  return (
    <div className="rounded-lg border border-slate-200 p-4 dark:border-slate-700">
      <div className="mb-2 flex items-center justify-between">
        <h2 className="text-sm font-semibold uppercase tracking-wide text-slate-500 dark:text-slate-400">
          {title}
        </h2>
        {subtitle && <span className="text-xs text-slate-400">{subtitle}</span>}
      </div>
      {children}
    </div>
  );
}
