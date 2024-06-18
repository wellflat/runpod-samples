FROM python:3.10-slim

RUN apt-get update && apt-get install -y git

WORKDIR /runner
RUN pip install --no-cache-dir runpod
COPY src/rp_handler.py .
COPY src/test_input.json .
COPY src/entrypoint.sh .

# Setup submodule
RUN git submodule update --init --recursive

# Set OCI Labels
LABEL org.opencontainers.image.source=https://github.com/wellflat/runpod-samples
LABEL org.opencontainers.image.description="RunPod Serverless samples"
LABEL org.opencontainers.image.licenses=MIT

# Start the container
CMD ["bash", "entrypoint.sh"]