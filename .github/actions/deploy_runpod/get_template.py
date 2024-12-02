#!/usr/bin/env python

import argparse
import asyncio
import json
import sys
from typing import Any

from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport
from gql.transport.exceptions import TransportError

RunPodGetTemplatesResponse = dict[str, Any]

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Deploy container to RunPod Serverless")
    parser.add_argument("--api_key", required=True, type=str, help="RunPod API key")
    return parser.parse_args()

async def request_get_templates(api_key: str) -> dict[str, Any]:
    transport = AIOHTTPTransport(
        url=f"https://api.runpod.io/graphql?api_key={api_key}",
    )
    async with Client(transport=transport) as session:
        query = """
        query getPodTemplates {
          myself {
            id
            podTemplates {
              containerDiskInGb
              containerRegistryAuthId
              env {
                key
                value
              }
              id
              imageName
              name
              startScript
              volumeMountPath
            }
          }
        }"""

        return await session.execute(gql(query))


async def main() -> None:
    try:
        args = parse_args()
        response = await request_get_templates(args.api_key)
        sys.stdout.write(json.dumps(response, indent=2))
        sys.exit(0)
    except TransportError as e:
        sys.stderr.write(str(e))
        sys.exit(-1)

asyncio.run(main())
