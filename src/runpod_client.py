#!/usr/bin/env python

import argparse
import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Any

from gql import Client
from gql import gql
from gql.transport.aiohttp import AIOHTTPTransport
from gql.transport.exceptions import TransportQueryError
from gql.transport.exceptions import TransportServerError


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Deploy container to RunPod Serverless")
    parser.add_argument("--api_key", type=str, default=None, help="RunPod API Key")
    parser.add_argument("--image_name", required=True, type=str, help="Target container image name")
    return parser.parse_args()

async def request_save_template(gql_path: Path, args: argparse.Namespace) -> dict[str, Any]:
    api_key = args.api_key if args.api_key else os.getenv("RUNPOD_API_KEY")
    image_name = args.image_name
    with Path.open(gql_path) as f:
        lines = f.read()

    params = {
        "input": {
            "advancedStart": False,
            "containerDiskInGb": 5,
            "containerRegistryAuthId": "clutj6gj60001l7062275rxfi",
            "dockerArgs": "",
            "env": [],
            "id": "48l430fsrb",
            "imageName": image_name,
            "isPublic": False,
            "isServerless": True,
            "name": "from_ghcr",
            "ports": "",
            "readme": "",
            "startJupyter": False,
            "startScript": "",
            "startSsh": False,
            "volumeInGb": 0,
            "volumeMountPath": "/workspace",
            "config": {
                "templateId": "48l430fsrb",
                "category": "GPU",
            },
        },
    }

    transport = AIOHTTPTransport(
        url=f"https://api.runpod.io/graphql?api_key={api_key}",
    )
    async with Client(transport=transport) as session:
        query = gql(lines)
        return await session.execute(query, variable_values=params, parse_result=True)

async def main() -> None:
    try:
        args = parse_args()
        gql_path = Path(__file__).parent / "runpod_save_template2.gql"
        result = await request_save_template(gql_path, args)
        sys.stdout.write(json.dumps(result, indent=2))
    except TransportQueryError as e:
        ## TODO logging
        sys.stderr.write(str(e))
    except TransportServerError as e:
        sys.stderr.write(str(e))

asyncio.run(main())
