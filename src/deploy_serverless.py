#!/usr/bin/env python

import argparse
import asyncio
import json
import os
import sys

from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport
from gql.transport.exceptions import TransportQueryError, TransportServerError

RunpodResponse = dict[str, dict[str, str]]

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Deploy container to RunPod Serverless")
    parser.add_argument("--api_key", type=str, default=None, help="RunPod API key")
    parser.add_argument("--image_name", required=True, type=str, help="Target container image name")
    return parser.parse_args()

async def request_save_template(args: argparse.Namespace) -> RunpodResponse:
    api_key = args.api_key if args.api_key else os.getenv("RUNPOD_API_KEY")
    image_name = args.image_name
    query = """
        mutation saveTemplate($input: SaveTemplateInput) {
            saveTemplate(input: $input) {
                id
                imageName
                name
            }
        }"""
    transport = AIOHTTPTransport(
        url=f"https://api.runpod.io/graphql?api_key={api_key}",
    )
    async with Client(transport=transport) as session:
        variables = {
            "input": {
                "advancedStart": False,
                "containerDiskInGb": 5,
                "containerRegistryAuthId": "clutj6gj60001l7062275rxfi",
                "dockerArgs": "",
                "env": [{"key": "test-key2", "value": "test-value2"}],
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
                #"config": {
                #    "templateId": "48l430fsrb",
                #    "category": "GPU",
                #},
            },
        }
        return await session.execute(gql(query), variable_values=variables)

async def main() -> None:
    try:
        args = parse_args()
        response = await request_save_template(args)
        sys.stdout.write(json.dumps(response, indent=2))
    except TransportQueryError as e:
        sys.stderr.write(str(e))
    except TransportServerError as e:
        sys.stderr.write(str(e))

asyncio.run(main())
