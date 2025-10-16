# ===== Build stage (Debian) =====
FROM python:3.13-slim AS build
RUN apt-get update && apt-get install -y --no-install-recommends gcc build-essential && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN python -m pip install --upgrade pip uv && \
    python -m uv export --frozen --no-dev --format requirements-txt > /tmp/requirements.txt
# Pre-build wheels (optional but nice for speed)
RUN python -m pip wheel --wheel-dir /tmp/wheels -r /tmp/requirements.txt

# ===== Runtime stage (Debian) =====
FROM python:3.13-slim AS runtime
# Lambda Web Adapter as extension
COPY --from=public.ecr.aws/awsguru/aws-lambda-adapter:0.9.1 /lambda-adapter /opt/extensions/lambda-adapter
WORKDIR /var/task

# Install deps from wheels (no venv needed; or create one here if you prefer)
COPY --from=build /tmp/requirements.txt /tmp/requirements.txt
COPY --from=build /tmp/wheels /tmp/wheels
RUN python -m pip install --no-cache-dir --no-index --find-links=/tmp/wheels -r /tmp/requirements.txt

# App code
COPY server ./server
COPY prompts ./prompts

# Env
ENV PYTHONUNBUFFERED=1
ENV PORT=8000
ENV AWS_LWA_PORT=8000
ENV AWS_LWA_READINESS_CHECK_PATH=/health
ENV AWS_LWA_LOG_LEVEL=debug

# Start server (bind to 0.0.0.0; shell form so $PORT expands)
CMD uvicorn server.server:asgi_app --host 0.0.0.0 --port $PORT --log-level info
