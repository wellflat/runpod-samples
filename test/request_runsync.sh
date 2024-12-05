#!/bin/sh

ENDPOINT_ID=hv6vxmb8var5us
INTERVAL=5


request_runsync() {
     curl --request POST \
          --url https://api.runpod.ai/v2/${ENDPOINT_ID}/runsync \
          --header "accept: application/json" \
          --header "authorization: ${RUNPOD_API_KEY}" \
          --header "content-type: application/json" \
          --data @test_input.json
}
echo "RUNPOD_API_KEY: ${RUNPOD_API_KEY}"

while true; do
     echo "Requesting runsync..."
     request_runsync
     echo "Waiting for ${INTERVAL} seconds..."
     sleep ${INTERVAL}
done
