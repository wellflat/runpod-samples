#!/bin/sh

ENDPOINT_ID=4b7i63j9w7witl

curl --request POST \
     --url https://api.runpod.ai/v2/${ENDPOINT_ID}/runsync \
     --header "accept: application/json" \
     --header "authorization: ${RUNPOD_API_KEY}" \
     --header "content-type: application/json" \
     --data @test_input.json