#!/usr/bin/env python

import os
import time
from typing import Any

import runpod
import sentry_sdk
from sentry_sdk.integrations.loguru import LoguruIntegration


def process_input(input_data: dict[str, str]) -> dict[str, str]:
    name = input_data["name"]
    greeting = f"hello, {name}"
    time.sleep(1)
    return { "greeting": greeting }

### RunPod Handler
def handler(event: dict[str, dict[str, Any]]) -> dict[str, str]:
    print(event)
    return process_input(event["input"])

if __name__ == "__main__":
    print("pseudo initialzing serverless (sleep 5s)")
    time.sleep(5)
    runpod.serverless.start({"handler": handler})
    sentry_sdk.init(
        dsn=os.getenv("SENTRY_DSN"),
        integrations=[LoguruIntegration()],
    )
