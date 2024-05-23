#!/usr/bin/env python

import argparse
import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Any

from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport
from gql.transport.exceptions import TransportQueryError, TransportServerError


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create RunPod instance")
    parser.add_argument("--api_key", type=str, default=None, help="RunPod API Key")
    return parser.parse_args()

async def request_deploy_ondemand_pod(gql_path: Path, args: argparse.Namespace) -> dict[str, Any]:
    api_key = args.api_key if args.api_key else os.getenv("RUNPOD_API_KEY")
    with Path.open(gql_path) as f:
        lines = f.read()

    transport = AIOHTTPTransport(
        url=f"https://api.runpod.io/graphql?api_key={api_key}",
    )
    async with Client(transport=transport) as session:
        query = gql(lines)
        return await session.execute(query, parse_result=True)

async def main() -> None:
    try:
        args = parse_args()
        gql_path = Path(__file__).parent / "runpod_deploy_pod.gql"
        result = await request_deploy_ondemand_pod(gql_path, args)
        sys.stdout.write(json.dumps(result, indent=2))
    except TransportQueryError as e:
        sys.stderr.write(str(e))
    except TransportServerError as e:
        sys.stderr.write(str(e))

asyncio.run(main())
