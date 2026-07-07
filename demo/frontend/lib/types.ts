// Mirrors the backend pydantic schemas (demo/backend/app/schemas.py).

export type MetricLevel = "grapheme" | "codepoint";

export interface MetricRow {
  key: string;
  label: string;
  family: string;
  level: MetricLevel;
  value: number;
  higher_better: boolean;
}

export interface GraphemesResponse {
  graphemes: string[];
  count: number;
  codepoints: string[];
  codepoint_count: number;
}

export interface GraphemeGroup {
  source: string;
  units: string[];
}

export interface DecomposeResponse {
  input: string;
  graphemes: string[];
  decomposed: string;
  decomposed_graphemes: string[];
  groups: GraphemeGroup[];
  recomposed: string;
  round_trip_ok: boolean;
}

export interface ComposeResponse {
  input: string;
  composed: string;
  composed_graphemes: string[];
  groups: GraphemeGroup[];
}

export interface DistanceResponse {
  grapheme_levenshtein: number;
  codepoint_levenshtein: number;
  grapheme_hamming: number | null;
  grapheme_count_s1: number;
  grapheme_count_s2: number;
  equal_grapheme_length: boolean;
}

export interface MetricsResponse {
  reference_graphemes: string[];
  hypothesis_graphemes: string[];
  metrics: MetricRow[];
}

export interface CorpusRow {
  index: number;
  reference: string;
  prediction: string;
  grapheme_chrf: number;
  std_chrf: number;
  cer: number;
  grapheme_levenshtein: number;
  codepoint_levenshtein: number;
}

export interface CorpusResponse {
  line_count: number;
  reference_lines: number;
  prediction_lines: number;
  aligned: boolean;
  truncated_rows: boolean;
  corpus: MetricRow[];
  rows: CorpusRow[];
}

export interface HealthResponse {
  status: string;
  library_version: string;
}
