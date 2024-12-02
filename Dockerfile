# Multi-stage build, build phase
FROM python:3.12 AS builder

RUN apt-get update && \
    apt-get install -y git && \
    rm -rf /var/lib/apt/lists/*
## install uv
RUN pip install --upgrade pip && pip install uv
WORKDIR /build
COPY pyproject.toml uv.lock .
RUN uv pip compile pyproject.toml -o requirements.txt

# Multi-stage build, package phase
FROM python:3.12-slim
ENV PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    TZ=Asia/Tokyo
RUN apt-get update && \
    apt-get install -y git git-lfs && \
    rm -rf /var/lib/apt/lists/*
WORKDIR /runner
COPY --from=builder /build/requirements.txt .
RUN pip install -r requirements.txt
COPY ./src/rp_handler.py ./src/test_input.json ./src/entrypoint.sh ./src/send_metrics.py .

# Set OCI Labels
LABEL org.opencontainers.image.source=https://github.com/wellflat/runpod-samples
LABEL org.opencontainers.image.description="RunPod Serverless samples"
LABEL org.opencontainers.image.licenses=MIT

# Start the container
CMD ["bash", "entrypoint.sh"]