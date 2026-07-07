# Backend image for the grapheme-kit demo.
#
# Build context MUST be the repository root so the library source is available:
#     docker build -f demo/backend/Dockerfile -t grapheme-kit-demo-api .
#
# Portable across hosts: the server binds to $PORT (default 7860, which is what
# Hugging Face Spaces expects). On Koyeb / your own box, $PORT is injected.
FROM python:3.14-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONUTF8=1 \
    PIP_NO_CACHE_DIR=1 \
    PORT=7860

WORKDIR /app

# 1) Install the library (and its scientific deps) from the repo root.
COPY pyproject.toml README.md ./
COPY src ./src
RUN pip install --upgrade pip && pip install .

# 2) Install the web layer.
COPY demo/backend/requirements.txt ./demo-requirements.txt
RUN pip install -r demo-requirements.txt

# 3) Copy the API code.
COPY demo/backend/app ./app

EXPOSE 7860
# Shell form so ${PORT} is expanded at runtime.
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-7860}
