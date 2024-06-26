#!/usr/bin/env python


import os

import runpod

if __name__ == "__main__":
    try:
        runpod.api_key = os.getenv("RUNPOD_API_KEY")
        endpoint = runpod.Endpoint("6ldqxy8osj4uuq")
        payload = {"input": {"name":"wellflat"}}
        print("request runpod endpoint")
        run = endpoint.run_sync(payload, timeout=60)
        print(run)
    except TimeoutError as e:
        print(e)
