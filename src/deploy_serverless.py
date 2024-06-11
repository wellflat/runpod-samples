#!/usr/bin/env python

import argparse
import asyncio
import json
import os
import sys

from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport
from gql.transport.exceptions import TransportError

RunpodResponse = dict[str, dict[str, str]]

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Deploy container to RunPod Serverless")
    parser.add_argument("--api_key", type=str, help="RunPod API key")
    parser.add_argument("--registry_auth_id", required=True, type=str, help="RunPod registory authentication ID")
    parser.add_argument("--image_name", type=str, required=True, help="Target container image name")
    parser.add_argument("--template_id", type=str, required=True, help="RunPod template ID")
    parser.add_argument("--template_name", type=str, required=True, help="RunPod template name")
    parser.add_argument("--env", type=str, required=True, help="RunPod template environment")
    return parser.parse_args()


async def request_save_template(args: argparse.Namespace) -> RunpodResponse:
    api_key = args.api_key if args.api_key else os.getenv("RUNPOD_API_KEY")
    registry_auth_id = args.registry_auth_id
    image_name = args.image_name
    template_id = args.template_id
    template_name = args.template_name
    test_env = args.env
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
        env = [
            {"key": "AWS_S3_BUCKET", "value": test_env}
        ]
        variables = {
            "input": {
                "advancedStart": False,
                "containerDiskInGb": 5,
                "containerRegistryAuthId": registry_auth_id,
                "dockerArgs": "",
                "env": env,
                "id": template_id,
                "imageName": image_name,
                "isPublic": False,
                "isServerless": True,
                "name": template_name,
                "ports": "",
                "readme": "",
                "startJupyter": False,
                "startScript": "",
                "startSsh": False,
                "volumeInGb": 0,
                "volumeMountPath": "/workspace",
                "config": {
                    "templateId": template_id,
                    "category": "GPU",
                },
            },
        }
        return await session.execute(gql(query), variable_values=variables)

async def main() -> None:
    try:
        args = parse_args()
        response = await request_save_template(args)
        sys.stdout.write(json.dumps(response, indent=2))
        sys.exit(0)
    except TransportError as e:
        sys.stderr.write(str(e))
        sys.exit(-1)


asyncio.run(main())
