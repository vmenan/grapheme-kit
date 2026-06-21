"use client";

import { useEffect, useState } from "react";
import { getDecompose } from "@/lib/api";
import type { DecomposeResponse } from "@/lib/types";
import { useDebounced } from "@/lib/useDebounced";
import { GraphemeChips } from "@/components/GraphemeChips";
import { GraphemeGroups } from "@/components/GraphemeGroups";

const SAMPLE = "வணக்கம் உலகம்";

export default function DecomposePage() {
  const [text, setText] = useState(SAMPLE);
  const debounced = useDebounced(text);
  const [result, setResult] = useState<DecomposeResponse | null>(null);
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
    getDecompose(debounced)
      .then((r) => !cancelled && setResult(r))
      .catch((e) => !cancelled && setError(String(e)))
      .finally(() => !cancelled && setLoading(false));
    return () => {
      cancelled = true;
    };
  }, [debounced]);

  return (
    <div className="py-2">
      <h1 className="text-2xl font-bold text-ink">Tamil / Sinhala Decomposition</h1>
      <p className="mt-1 text-sm text-slate-600">
        Segment into grapheme clusters, then decompose complex scripts into their
        phonetic units and recompose to verify the round-trip.
      </p>

      <div className="mt-6 grid grid-cols-1 gap-6 lg:grid-cols-2">
        <div>
          <label className="mb-1 block text-xs font-semibold uppercase tracking-wide text-slate-500">
            Unicode input
          </label>
          <textarea
            value={text}
            onChange={(e) => setText(e.target.value)}
            rows={5}
            className="indic w-full resize-y rounded-lg border border-slate-300 p-3 text-xl focus:border-ink focus:outline-none"
            placeholder="Type Tamil or Sinhala text…"
          />
          <p className="mt-2 text-xs text-slate-400">
            {loading ? "Computing…" : "Updates as you type."}
          </p>
        </div>

        <div className="space-y-5">
          {error && (
            <div className="rounded-md border border-rose-300 bg-rose-50 px-3 py-2 text-sm text-rose-800">
              {error}
              <div className="mt-1 text-xs text-rose-500">
                Is the backend running at the configured API URL?
              </div>
            </div>
          )}

          {result && (
            <>
              <Section
                title="Grapheme clusters"
                subtitle={`${result.graphemes.length} graphemes`}
              >
                <GraphemeChips graphemes={result.graphemes} />
              </Section>

              <Section
                title="Decomposed (phonetic units)"
                subtitle="boxed = units from one grapheme"
              >
                <p className="indic break-words rounded-lg bg-slate-50 p-3 text-xl">
                  {result.decomposed}
                </p>
                <div className="mt-3">
                  <GraphemeGroups groups={result.groups} />
                </div>
              </Section>

              <Section title="Recomposed (round-trip)">
                <div className="flex items-center gap-3">
                  <p className="indic break-words text-xl">{result.recomposed}</p>
                  <span
                    className={
                      "rounded px-2 py-0.5 text-xs font-medium " +
                      (result.round_trip_ok
                        ? "bg-emerald-100 text-emerald-800"
                        : "bg-rose-100 text-rose-800")
                    }
                  >
                    {result.round_trip_ok ? "✓ matches input" : "✗ differs from input"}
                  </span>
                </div>
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
    <div className="rounded-lg border border-slate-200 p-4">
      <div className="mb-2 flex items-center justify-between">
        <h2 className="text-sm font-semibold uppercase tracking-wide text-slate-500">
          {title}
        </h2>
        {subtitle && <span className="text-xs text-slate-400">{subtitle}</span>}
      </div>
      {children}
    </div>
  );
}
