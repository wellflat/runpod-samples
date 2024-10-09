#!/usr/bin/env python

from typing import Any

import runpod
import time


def process_input(input_data: dict[str, str]) -> dict[str, str]:
    name = input_data["name"]
    greeting = f"hello, {name}"
    return { "greeting": greeting }

### RunPod Handler
def handler(event: dict[str, dict[str, Any]]) -> dict[str, str]:
    print(event)
    return process_input(event["input"])

if __name__ == "__main__":
    print("pseudo initialzing serverless")
    time.sleep(10)
    runpod.serverless.start({"handler": handler})
