#!/usr/bin/env python

import os

import pynvml
import sentry_sdk

if __name__ == "__main__":
    sentry_sdk.init(
        dsn=os.getenv("SENTRY_DSN"),
        sample_rate=1.0,
        profiles_sample_rate=1.0,
    )
    pynvml.nvmlInit()
    print(f"Driver Version: {pynvml.nvmlSystemGetDriverVersion()}")
    handle = pynvml.nvmlDeviceGetHandleByIndex(0)
    info = pynvml.nvmlDeviceGetMemoryInfo(handle)
    print(f"Total memory: {info.total}")
    print(f"Free memory:, {info.free}")
    print(f"Used memory: {info.used}")
    send_str = f"Total memory: {info.total}, Free memory: {info.free}, Used memory: {info.used}"
    pynvml.nvmlShutdown()

    sentry_sdk.capture_event({"message": send_str, "level": "info"})
