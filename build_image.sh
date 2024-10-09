#!/bin/sh

docker build -t runpod-samples:latest \
    --secret id=github_token,env=GH_TOKEN \
    --build-arg BRANCH=develop .

# docker run -it --rm runpod-samples /bin/bash