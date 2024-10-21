#!/bin/sh

IMAGE=runpod-samples:latest
docker build -t ${IMAGE} \
    --secret id=github_token,env=GH_TOKEN \
    --build-arg BRANCH=develop --no-cache .

# docker run -it --rm runpod-samples /bin/bash
