#!/usr/bin/env python

import time
from typing import Any

import runpod


def process_input(input_data: dict[str, str]) -> dict[str, str]:
    name = input_data["name"]
    greeting = f"hello, {name}"
    return { "greeting": greeting }

### RunPod Handler
def handler(event: dict[str, dict[str, Any]]) -> dict[str, str]:
    print(event)
    return process_input(event["input"])

if __name__ == "__main__":
    print("pseudo initialzing serverless (sleep 5s)")
    time.sleep(5)
    runpod.serverless.start({"handler": handler})
