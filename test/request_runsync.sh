#!/bin/sh

ENDPOINT_ID=yra3ok1uioei67

curl --request POST \
     --url https://api.runpod.ai/v2/${ENDPOINT_ID}/runsync \
     --header "accept: application/json" \
     --header "authorization: ${RUNPOD_API_KEY}" \
     --header "content-type: application/json" \
     --data @test_input.json
