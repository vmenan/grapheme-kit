// Typed client for the graphemes++ demo API.
// Base URL is configured at build time via NEXT_PUBLIC_API_BASE_URL.

import type {
  ComposeResponse,
  CorpusResponse,
  DecomposeResponse,
  DistanceResponse,
  GraphemesResponse,
  HealthResponse,
  MetricsResponse,
} from "./types";

export const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL?.replace(/\/$/, "") ||
  "http://localhost:7860";

async function postJSON<T>(path: string, body: unknown): Promise<T> {
  const res = await fetch(`${API_BASE_URL}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    throw new Error(`API ${path} failed: ${res.status} ${res.statusText}`);
  }
  return res.json() as Promise<T>;
}

export function getHealth(): Promise<HealthResponse> {
  return fetch(`${API_BASE_URL}/api/health`).then((r) => {
    if (!r.ok) throw new Error(`health failed: ${r.status}`);
    return r.json();
  });
}

export function getMetrics(
  reference: string,
  hypothesis: string
): Promise<MetricsResponse> {
  return postJSON("/api/metrics", { reference, hypothesis });
}

export function getDecompose(text: string): Promise<DecomposeResponse> {
  return postJSON("/api/decompose", { text });
}

export function getCompose(text: string): Promise<ComposeResponse> {
  return postJSON("/api/compose", { text });
}

export function getGraphemes(text: string): Promise<GraphemesResponse> {
  return postJSON("/api/graphemes", { text });
}

export function getDistance(s1: string, s2: string): Promise<DistanceResponse> {
  return postJSON("/api/distance", { s1, s2 });
}

export async function postCorpus(
  referenceFile: File,
  predictionFile: File
): Promise<CorpusResponse> {
  const form = new FormData();
  form.append("reference_file", referenceFile);
  form.append("prediction_file", predictionFile);
  const res = await fetch(`${API_BASE_URL}/api/metrics/corpus`, {
    method: "POST",
    body: form,
  });
  if (!res.ok) {
    throw new Error(`corpus metrics failed: ${res.status} ${res.statusText}`);
  }
  return res.json();
}
