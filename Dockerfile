FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# System deps for uvicorn[standard] (includes uvloop/httptools) may need gcc on some platforms.
# We keep it minimal; if you hit build issues, uncomment build deps.
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
  && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml README.md /app/
COPY src /app/src

RUN pip install --no-cache-dir -U pip \
    && pip install --no-cache-dir .

EXPOSE 8000

CMD ["python", "-m", "theo_server"]
