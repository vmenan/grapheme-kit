"""FastAPI app exposing the graphemes++ library for the demo website.

Run locally:
    uvicorn app.main:app --reload --port 7860

The frontend (Cloudflare Pages) calls these JSON endpoints. CORS origins are
configurable via the GRAPHEMES_CORS_ORIGINS env var (comma-separated); defaults
to "*" for easy local development.
"""

from __future__ import annotations

import os
import sys

# NOTE: graphemes_plusplus/graphemizer.py currently has an unguarded module-level
# `print(...)` (debug leftover, lines 35-36) that runs on import. On a Windows
# cp1252 stdout this crashes when emitting Sinhala text. Force UTF-8 on the
# streams *before* importing the library so the demo is robust on every host.
# (The library should drop those stray prints — flagged separately.)
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8")  # type: ignore[union-attr]
    except Exception:  # pragma: no cover - best effort
        pass

from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from app import services
from app.schemas import (
    ComposeResponse,
    CorpusResponse,
    DecomposeResponse,
    DistanceResponse,
    GraphemesResponse,
    HealthResponse,
    MetricsRequest,
    MetricsResponse,
    PairRequest,
    TextRequest,
)

app = FastAPI(
    title="graphemes++ demo API",
    version="0.1.0",
    description="Grapheme segmentation, decomposition and evaluation metrics "
    "for Tamil and Sinhala, powered by the graphemes_plusplus library.",
)

_origins_env = os.getenv("GRAPHEMES_CORS_ORIGINS", "*")
_origins = [o.strip() for o in _origins_env.split(",") if o.strip()] or ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=_origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok", library_version=services.library_version())


@app.post("/api/graphemes", response_model=GraphemesResponse)
def graphemes(req: TextRequest) -> GraphemesResponse:
    return GraphemesResponse(**services.get_graphemes(req.text))


@app.post("/api/decompose", response_model=DecomposeResponse)
def decompose(req: TextRequest) -> DecomposeResponse:
    return DecomposeResponse(**services.get_decompose(req.text))


@app.post("/api/compose", response_model=ComposeResponse)
def compose(req: TextRequest) -> ComposeResponse:
    return ComposeResponse(**services.get_compose(req.text))


@app.post("/api/distance", response_model=DistanceResponse)
def distance(req: PairRequest) -> DistanceResponse:
    return DistanceResponse(**services.get_distance(req.s1, req.s2))


@app.post("/api/metrics", response_model=MetricsResponse)
def metrics(req: MetricsRequest) -> MetricsResponse:
    return MetricsResponse(**services.get_metrics(req.reference, req.hypothesis))


@app.post("/api/metrics/corpus", response_model=CorpusResponse)
async def metrics_corpus(
    reference_file: UploadFile = File(...),
    prediction_file: UploadFile = File(...),
) -> CorpusResponse:
    reference_text = (await reference_file.read()).decode("utf-8", errors="replace")
    prediction_text = (await prediction_file.read()).decode("utf-8", errors="replace")
    return CorpusResponse(**services.get_corpus_metrics(reference_text, prediction_text))


if __name__ == "__main__":  # pragma: no cover
    import uvicorn

    port = int(os.getenv("PORT", "7860"))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port)
