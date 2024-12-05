#!/usr/bin/env python

import hashlib
import os
import time
from typing import Any

import runpod
import sentry_sdk
from sentry_sdk.integrations.loguru import LoguruIntegration
from sentry_sdk.integrations.serverless import serverless_function
from loguru import logger
import sentry_sdk.profiler

def process_input(input_data: dict[str, str]) -> dict[str, str]:
    transaction = sentry_sdk.start_transaction(op="process_input", name="process_input(transaction)")
    span = transaction.start_child(op="greeting", name="greeting")
    name = input_data["name"]
    greeting = f"hello, {name}"
    span.finish()
    number = int(input_data["number"])
    span = transaction.start_child(op="calculate_fibonacci", name=f"calculate_fibonacci({number})")
    fibonacci_result = calculate_fibonacci(number)
    span.finish()
    span = transaction.start_child(op="hash", name=f"hashsha256({number})")
    digest = hashlib.sha256(f"{greeting}-{fibonacci_result}".encode()).hexdigest()
    span.finish()
    transaction.finish()
    return { "greeting": greeting, "fibonacci": str(fibonacci_result), "digest": digest }


def calculate_fibonacci(n: int) -> int:
    if n <= 1:
        return n
    return calculate_fibonacci(n - 1) + calculate_fibonacci(n - 2)


### RunPod Handler
@serverless_function
def handler(event: dict[str, dict[str, Any]]) -> dict[str, str]:
    logger.info(event)
    return process_input(event["input"])


if __name__ == "__main__":
    print("pseudo initialzing serverless (sleep 5s)")
    time.sleep(5)
    sentry_sdk.init(
        dsn=os.getenv("SENTRY_DSN"),
        integrations=[LoguruIntegration()],
        # Set traces_sample_rate to 1.0 to capture 100% of transactions for tracing.
        traces_sample_rate=1.0,
        # Set profiles_sample_rate to 1.0 to profile 100% of sampled transactions.
        # We recommend adjusting this value in production.
        #profiles_sample_rate=1.0,
    )
    sentry_sdk.profiler.start_profiler()
    runpod.serverless.start({"handler": handler})
    sentry_sdk.profiler.stop_profiler()
    
    

