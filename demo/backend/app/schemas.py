"""Pydantic request/response models for the demo API."""

from __future__ import annotations

from pydantic import BaseModel, Field


class TextRequest(BaseModel):
    text: str = Field(default="", description="Input text (Tamil / Sinhala / mixed).")


class PairRequest(BaseModel):
    s1: str = Field(default="", description="First string.")
    s2: str = Field(default="", description="Second string.")


class MetricsRequest(BaseModel):
    reference: str = Field(default="", description="Reference (gold) text.")
    hypothesis: str = Field(default="", description="Hypothesis / prediction text.")


class MetricRow(BaseModel):
    key: str
    label: str
    family: str
    level: str  # "grapheme" | "codepoint"
    value: float
    higher_better: bool


class GraphemesResponse(BaseModel):
    graphemes: list[str]
    count: int
    codepoints: list[str]
    codepoint_count: int


class GraphemeGroup(BaseModel):
    source: str
    units: list[str]


class DecomposeResponse(BaseModel):
    input: str
    graphemes: list[str]
    decomposed: str
    decomposed_graphemes: list[str]
    groups: list[GraphemeGroup]
    recomposed: str
    round_trip_ok: bool


class ComposeResponse(BaseModel):
    input: str
    composed: str


class DistanceResponse(BaseModel):
    grapheme_levenshtein: int
    codepoint_levenshtein: int
    grapheme_hamming: int | None
    grapheme_count_s1: int
    grapheme_count_s2: int
    equal_grapheme_length: bool


class MetricsResponse(BaseModel):
    reference_graphemes: list[str]
    hypothesis_graphemes: list[str]
    metrics: list[MetricRow]


class CorpusRow(BaseModel):
    index: int
    reference: str
    prediction: str
    grapheme_chrf: float
    std_chrf: float
    cer: float
    grapheme_levenshtein: int
    codepoint_levenshtein: int


class CorpusResponse(BaseModel):
    line_count: int
    reference_lines: int
    prediction_lines: int
    aligned: bool
    truncated_rows: bool = False
    corpus: list[MetricRow]
    rows: list[CorpusRow]


class HealthResponse(BaseModel):
    status: str
    library_version: str
