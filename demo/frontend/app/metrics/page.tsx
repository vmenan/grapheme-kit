"use client";

import { useEffect, useMemo, useState } from "react";
import { getMetrics, postCorpus } from "@/lib/api";
import type { CorpusResponse, MetricsResponse } from "@/lib/types";
import { useDebounced } from "@/lib/useDebounced";
import { MetricTable } from "@/components/MetricTable";
import { MetricFocusSelect } from "@/components/MetricFocusSelect";
import { ScoreHighlight } from "@/components/ScoreHighlight";
import { GraphemeChips } from "@/components/GraphemeChips";
import { FileDrop } from "@/components/FileDrop";

const SAMPLE_REF = "ஸ்ரீலங்கா ஒரு அழகான தீவு நாடு.";
const SAMPLE_HYP = "ஶ்ரீலங்கா ஒரு அழகான தீவு நாடு.";

type Mode = "text" | "files";

export default function MetricsPage() {
  const [mode, setMode] = useState<Mode>("text");

  // --- Text mode ---
  const [reference, setReference] = useState(SAMPLE_REF);
  const [hypothesis, setHypothesis] = useState(SAMPLE_HYP);
  const dRef = useDebounced(reference);
  const dHyp = useDebounced(hypothesis);
  const [result, setResult] = useState<MetricsResponse | null>(null);
  const [focus, setFocus] = useState("all");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (mode !== "text") return;
    if (!dRef.trim() && !dHyp.trim()) {
      setResult(null);
      return;
    }
    let cancelled = false;
    setLoading(true);
    setError(null);
    getMetrics(dRef, dHyp)
      .then((r) => !cancelled && setResult(r))
      .catch((e) => !cancelled && setError(String(e)))
      .finally(() => !cancelled && setLoading(false));
    return () => {
      cancelled = true;
    };
  }, [dRef, dHyp, mode]);

  const families = useMemo(
    () => (result ? Array.from(new Set(result.metrics.map((m) => m.family))) : []),
    [result]
  );

  // --- File mode ---
  const [refFile, setRefFile] = useState<File | null>(null);
  const [predFile, setPredFile] = useState<File | null>(null);
  const [corpus, setCorpus] = useState<CorpusResponse | null>(null);
  const [corpusErr, setCorpusErr] = useState<string | null>(null);
  const [corpusLoading, setCorpusLoading] = useState(false);

  async function runCorpus() {
    if (!refFile || !predFile) return;
    setCorpusLoading(true);
    setCorpusErr(null);
    try {
      setCorpus(await postCorpus(refFile, predFile));
    } catch (e) {
      setCorpusErr(String(e));
    } finally {
      setCorpusLoading(false);
    }
  }

  return (
    <div className="py-2">
      <div className="flex flex-wrap items-end justify-between gap-3">
        <div>
          <h1 className="text-2xl font-bold text-ink">Evaluation Metrics</h1>
          <p className="mt-1 text-sm text-slate-600">
            Grapheme-level scores next to their unicode-point baselines.
          </p>
        </div>
        <div className="flex items-center gap-2">
          {result && mode === "text" && (
            <MetricFocusSelect
              families={families}
              value={focus}
              onChange={setFocus}
            />
          )}
          <div className="inline-flex rounded-md border border-slate-300 p-0.5 text-sm">
            {(["text", "files"] as Mode[]).map((m) => (
              <button
                key={m}
                onClick={() => setMode(m)}
                className={
                  "rounded px-3 py-1 capitalize transition " +
                  (mode === m ? "bg-ink text-white" : "text-slate-600")
                }
              >
                {m}
              </button>
            ))}
          </div>
        </div>
      </div>

      {mode === "text" ? (
        <div className="mt-6 grid grid-cols-1 gap-6 lg:grid-cols-2">
          <div className="space-y-4">
            <Field label="Reference (gold)">
              <textarea
                value={reference}
                onChange={(e) => setReference(e.target.value)}
                rows={4}
                className="indic w-full resize-y rounded-lg border border-slate-300 p-3 text-lg focus:border-ink focus:outline-none"
                placeholder="Reference text…"
              />
            </Field>
            <Field label="Prediction (hypothesis)">
              <textarea
                value={hypothesis}
                onChange={(e) => setHypothesis(e.target.value)}
                rows={4}
                className="indic w-full resize-y rounded-lg border border-slate-300 p-3 text-lg focus:border-ink focus:outline-none"
                placeholder="Predicted text…"
              />
            </Field>
            {result && (
              <div className="space-y-3 rounded-lg border border-slate-200 p-4">
                <Breakdown
                  title="Reference graphemes"
                  graphemes={result.reference_graphemes}
                />
                <Breakdown
                  title="Prediction graphemes"
                  graphemes={result.hypothesis_graphemes}
                />
              </div>
            )}
          </div>

          <div className="space-y-4">
            {error && <ErrorBox message={error} />}
            {!result && !error && (
              <p className="text-sm text-slate-400">
                {loading ? "Computing…" : "Enter text to see metrics."}
              </p>
            )}
            {result && (
              <>
                <ScoreHighlight rows={result.metrics} />
                <MetricTable rows={result.metrics} focus={focus} />
                <p className="text-xs text-slate-400">
                  All values come straight from the graphemes++ library and
                  sacrebleu.
                </p>
              </>
            )}
          </div>
        </div>
      ) : (
        <div className="mt-6 space-y-5">
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <FileDrop label="Reference file" file={refFile} onPick={setRefFile} />
            <FileDrop
              label="Prediction file"
              file={predFile}
              onPick={setPredFile}
            />
          </div>
          <p className="text-xs text-slate-500">
            One sentence per line, reference and prediction line-aligned.
          </p>
          <button
            onClick={runCorpus}
            disabled={!refFile || !predFile || corpusLoading}
            className="rounded-md bg-ink px-4 py-2 text-sm font-medium text-white disabled:opacity-40"
          >
            {corpusLoading ? "Computing…" : "Compute corpus metrics"}
          </button>

          {corpusErr && <ErrorBox message={corpusErr} />}
          {corpus && (
            <div className="space-y-4">
              {!corpus.aligned && (
                <div className="rounded-md border border-amber-300 bg-amber-50 px-3 py-2 text-sm text-amber-800">
                  Files differ in length ({corpus.reference_lines} vs{" "}
                  {corpus.prediction_lines} lines). Compared the first{" "}
                  {corpus.line_count}.
                </div>
              )}
              <ScoreHighlight rows={corpus.corpus} />
              <MetricTable rows={corpus.corpus} />
              <CorpusRows corpus={corpus} />
            </div>
          )}
        </div>
      )}
    </div>
  );
}

function Field({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <label className="block">
      <span className="mb-1 block text-xs font-semibold uppercase tracking-wide text-slate-500">
        {label}
      </span>
      {children}
    </label>
  );
}

function Breakdown({ title, graphemes }: { title: string; graphemes: string[] }) {
  return (
    <div>
      <div className="mb-1 flex items-center justify-between">
        <span className="text-xs font-semibold uppercase tracking-wide text-slate-500">
          {title}
        </span>
        <span className="text-xs text-slate-400">{graphemes.length} graphemes</span>
      </div>
      <GraphemeChips graphemes={graphemes} />
    </div>
  );
}

function ErrorBox({ message }: { message: string }) {
  return (
    <div className="rounded-md border border-rose-300 bg-rose-50 px-3 py-2 text-sm text-rose-800">
      {message}
      <div className="mt-1 text-xs text-rose-500">
        Is the backend running at the configured API URL?
      </div>
    </div>
  );
}

function CorpusRows({ corpus }: { corpus: CorpusResponse }) {
  if (!corpus.rows.length) return null;
  return (
    <div className="overflow-x-auto rounded-lg border border-slate-200">
      <table className="w-full text-sm">
        <thead className="bg-slate-50 text-left text-xs uppercase tracking-wide text-slate-500">
          <tr>
            <th className="px-3 py-2">#</th>
            <th className="px-3 py-2">Reference</th>
            <th className="px-3 py-2">Prediction</th>
            <th className="px-3 py-2 text-right">chrF (g)</th>
            <th className="px-3 py-2 text-right">chrF (cp)</th>
            <th className="px-3 py-2 text-right">CER</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-100">
          {corpus.rows.map((r) => (
            <tr key={r.index} className="hover:bg-slate-50">
              <td className="px-3 py-2 text-slate-400">{r.index + 1}</td>
              <td className="indic max-w-xs truncate px-3 py-2">{r.reference}</td>
              <td className="indic max-w-xs truncate px-3 py-2">{r.prediction}</td>
              <td className="px-3 py-2 text-right font-mono tabular-nums">
                {r.grapheme_chrf.toFixed(2)}
              </td>
              <td className="px-3 py-2 text-right font-mono tabular-nums text-slate-500">
                {r.std_chrf.toFixed(2)}
              </td>
              <td className="px-3 py-2 text-right font-mono tabular-nums">
                {r.cer.toFixed(3)}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      {corpus.truncated_rows && (
        <p className="px-3 py-2 text-xs text-slate-400">
          Showing the first {corpus.rows.length} of {corpus.line_count} lines.
        </p>
      )}
    </div>
  );
}
