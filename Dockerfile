# Multi-stage build, build phase
FROM python:3.10 as builder

RUN apt-get update && \
    apt-get install -y git && \
    rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip && pip install poetry
WORKDIR /build
COPY pyproject.toml poetry.lock .
RUN poetry config virtualenvs.create false && \
    poetry config warnings.export false && \
    poetry export --without-hashes -f requirements.txt > requirements.txt
ARG BRANCH
RUN --mount=type=secret,id=github_token \
    GH_TOKEN=$(cat /run/secrets/github_token) && \
    git clone -b ${BRANCH} https://wellflat:${GH_TOKEN}@github.com/wellflat/runpod-samples && \
    cd runpod-samples && \
    git submodule | cut -c 2- | cut -d' ' -f1,2 --output-delimiter="," > /build/submodule_list.csv

# Multi-stage build, package phase
FROM python:3.10-slim
ENV PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    TZ=Asia/Tokyo
RUN apt-get update && \
    apt-get install -y git git-lfs && \
    rm -rf /var/lib/apt/lists/*
WORKDIR /runner
COPY --from=builder /build/requirements.txt /build/submodule_list.csv .
RUN pip install -r requirements.txt
COPY ./src/rp_handler.py ./src/test_input.json ./src/entrypoint.sh .

# Set OCI Labels
LABEL org.opencontainers.image.source=https://github.com/wellflat/runpod-samples
LABEL org.opencontainers.image.description="RunPod Serverless samples"
LABEL org.opencontainers.image.licenses=MIT

# Start the container
CMD ["bash", "entrypoint.sh"]