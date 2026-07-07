"use client";

import { useEffect, useState } from "react";
import { getDecompose, getCompose } from "@/lib/api";
import type { DecomposeResponse, ComposeResponse } from "@/lib/types";
import { useDebounced } from "@/lib/useDebounced";
import { GraphemeChips } from "@/components/GraphemeChips";
import { GraphemeGroups } from "@/components/GraphemeGroups";

const SAMPLE = "வணக்கம் ආයුබෝවන්";
const SAMPLE_UNITS = "வ்அண்அக்க்அம் ආය්උබ්ඕව්අන්";

type Mode = "decompose" | "compose";

export default function CanonicalizationPage() {
  const [mode, setMode] = useState<Mode>("decompose");

  // --- Decomposition ---
  const [text, setText] = useState(SAMPLE);
  const debounced = useDebounced(text);
  const [decomposeResult, setDecomposeResult] = useState<DecomposeResponse | null>(
    null
  );
  const [decomposeError, setDecomposeError] = useState<string | null>(null);
  const [decomposeLoading, setDecomposeLoading] = useState(false);

  useEffect(() => {
    if (!debounced.trim()) {
      setDecomposeResult(null);
      return;
    }
    let cancelled = false;
    setDecomposeLoading(true);
    setDecomposeError(null);
    getDecompose(debounced)
      .then((r) => !cancelled && setDecomposeResult(r))
      .catch((e) => !cancelled && setDecomposeError(String(e)))
      .finally(() => !cancelled && setDecomposeLoading(false));
    return () => {
      cancelled = true;
    };
  }, [debounced]);

  // --- Composition ---
  const [unitsText, setUnitsText] = useState(SAMPLE_UNITS);
  const debouncedUnits = useDebounced(unitsText);
  const [composeResult, setComposeResult] = useState<ComposeResponse | null>(null);
  const [composeError, setComposeError] = useState<string | null>(null);
  const [composeLoading, setComposeLoading] = useState(false);
  const [prefilledFromDecompose, setPrefilledFromDecompose] = useState(false);

  // Once the user actually decomposes something, hand that off as the compose default.
  useEffect(() => {
    if (decomposeResult && !prefilledFromDecompose) {
      setUnitsText(decomposeResult.decomposed);
      setPrefilledFromDecompose(true);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [decomposeResult]);

  useEffect(() => {
    if (!debouncedUnits.trim()) {
      setComposeResult(null);
      return;
    }
    let cancelled = false;
    setComposeLoading(true);
    setComposeError(null);
    getCompose(debouncedUnits)
      .then((r) => !cancelled && setComposeResult(r))
      .catch((e) => !cancelled && setComposeError(String(e)))
      .finally(() => !cancelled && setComposeLoading(false));
    return () => {
      cancelled = true;
    };
  }, [debouncedUnits]);

  return (
    <div className="py-2">
      <div className="flex flex-wrap items-end justify-between gap-3">
        <div>
          <h1 className="text-2xl font-bold text-ink">Canonicalization</h1>
          <p className="mt-1 text-sm text-slate-600 dark:text-slate-400">
            Two inverse operations on grapheme clusters: decompose into phonetic
            units, or compose units back into a full grapheme.
          </p>
        </div>
        <div className="inline-flex rounded-md border border-slate-300 p-0.5 text-sm dark:border-slate-700">
          {(["decompose", "compose"] as Mode[]).map((m) => (
            <button
              key={m}
              onClick={() => setMode(m)}
              className={
                "rounded px-3 py-1 capitalize transition " +
                (mode === m ? "bg-ink text-white dark:text-slate-900" : "text-slate-600 dark:text-slate-400")
              }
            >
              {m === "decompose" ? "Decomposition" : "Composition"}
            </button>
          ))}
        </div>
      </div>

      {mode === "decompose" ? (
        <div className="mt-6 grid grid-cols-1 gap-6 lg:grid-cols-2">
          <div>
            <label className="mb-1 block text-xs font-semibold uppercase tracking-wide text-slate-500 dark:text-slate-400">
              Unicode input
            </label>
            <textarea
              value={text}
              onChange={(e) => setText(e.target.value)}
              rows={5}
              className="indic w-full resize-y rounded-lg border border-slate-300 bg-white p-3 text-xl text-ink focus:border-ink focus:outline-none dark:border-slate-700 dark:bg-slate-900 dark:text-slate-100"
              placeholder="Type any text…"
            />
            <p className="mt-2 text-xs text-slate-400">
              {decomposeLoading ? "Computing…" : "Updates as you type."}
            </p>
          </div>

          <div className="space-y-5">
            {decomposeError && <ErrorBox message={decomposeError} />}
            {decomposeResult && (
              <>
                <Section
                  title="Grapheme clusters"
                  subtitle={`${decomposeResult.graphemes.length} graphemes`}
                >
                  <GraphemeChips graphemes={decomposeResult.graphemes} />
                </Section>

                <Section
                  title="Decomposed (phonetic units)"
                  subtitle="boxed = units from one grapheme"
                >
                  <GraphemeGroups groups={decomposeResult.groups} />
                </Section>

                <Section title="Recomposed (round-trip)">
                  <div className="flex items-center gap-3">
                    <p className="indic break-words text-xl">
                      {decomposeResult.recomposed}
                    </p>
                    <span
                      className={
                        "rounded px-2 py-0.5 text-xs font-medium " +
                        (decomposeResult.round_trip_ok
                          ? "bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300"
                          : "bg-rose-100 text-rose-800 dark:bg-rose-950 dark:text-rose-300")
                      }
                    >
                      {decomposeResult.round_trip_ok
                        ? "✓ matches input"
                        : "✗ differs from input"}
                    </span>
                  </div>
                </Section>
              </>
            )}
            {!decomposeResult && !decomposeError && (
              <p className="text-sm text-slate-400">
                Enter text to see the breakdown.
              </p>
            )}
          </div>
        </div>
      ) : (
        <div className="mt-6 grid grid-cols-1 gap-6 lg:grid-cols-2">
          <div>
            <label className="mb-1 block text-xs font-semibold uppercase tracking-wide text-slate-500 dark:text-slate-400">
              Decomposed units
            </label>
            <textarea
              value={unitsText}
              onChange={(e) => setUnitsText(e.target.value)}
              rows={5}
              className="indic w-full resize-y rounded-lg border border-slate-300 bg-white p-3 text-xl text-ink focus:border-ink focus:outline-none dark:border-slate-700 dark:bg-slate-900 dark:text-slate-100"
              placeholder="Paste decomposed phonetic units…"
            />
            <p className="mt-2 text-xs text-slate-400">
              {composeLoading ? "Computing…" : "Updates as you type. Prefilled from the decomposition tab."}
            </p>
          </div>

          <div className="space-y-5">
            {composeError && <ErrorBox message={composeError} />}
            {composeResult && (
              <>
                <Section
                  title="Input units"
                  subtitle="boxed = units from one grapheme"
                >
                  <GraphemeGroups groups={composeResult.groups} />
                </Section>

                <Section
                  title="Composed (grapheme clusters)"
                  subtitle={`${composeResult.composed_graphemes.length} graphemes`}
                >
                  <GraphemeChips graphemes={composeResult.composed_graphemes} />
                </Section>
              </>
            )}
            {!composeResult && !composeError && (
              <p className="text-sm text-slate-400">
                Enter decomposed units to compose them back.
              </p>
            )}
          </div>
        </div>
      )}
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

function ErrorBox({ message }: { message: string }) {
  return (
    <div className="rounded-md border border-rose-300 bg-rose-50 px-3 py-2 text-sm text-rose-800 dark:border-rose-800 dark:bg-rose-950 dark:text-rose-200">
      {message}
      <div className="mt-1 text-xs text-rose-500 dark:text-rose-400">
        Is the backend running at the configured API URL?
      </div>
    </div>
  );
}
