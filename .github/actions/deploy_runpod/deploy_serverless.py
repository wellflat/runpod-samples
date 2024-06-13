#!/usr/bin/env python

import argparse
import asyncio
import json
import sys
from typing import Any

from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport
from gql.transport.exceptions import TransportError

RunpodResponse = dict[str, dict[str, str]]

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Deploy container to RunPod Serverless")
    parser.add_argument("--api_key", type=str, help="RunPod API key")
    parser.add_argument("--image_name", type=str, required=True, help="Target container image name")
    parser.add_argument("--template_id", type=str, required=True, help="RunPod template ID")
    return parser.parse_args()

async def request_get_templates(transport: AIOHTTPTransport) -> dict[str, Any]:
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

async def request_save_template(transport: AIOHTTPTransport, image_name: str, params: dict[str, Any]) -> RunpodResponse:
    query = """
        mutation saveTemplate($input: SaveTemplateInput) {
            saveTemplate(input: $input) {
                id
                imageName
                name
            }
        }"""
    async with Client(transport=transport) as session:
        variables = {
            "input": {
                "advancedStart": False,
                "containerDiskInGb": params["containerDiskInGb"],
                "containerRegistryAuthId": params["containerRegistryAuthId"],
                "dockerArgs": "",
                "env": params["env"],
                "id": params["id"],
                "imageName": image_name,
                "isPublic": False,
                "isServerless": True,
                "name": params["name"],
                "ports": "",
                "readme": "",
                "startJupyter": False,
                "startScript": params["startScript"],
                "startSsh": False,
                "volumeInGb": 0,
                "volumeMountPath": params["volumeMountPath"],
                "config": {
                    "templateId": params["id"],
                    "category": "GPU",
                },
            },
        }
        return await session.execute(gql(query), variable_values=variables)

async def main() -> None:
    try:
        args = parse_args()
        transport = AIOHTTPTransport(url=f"https://api.runpod.io/graphql?api_key={args.api_key}")
        templates = await request_get_templates(transport)
        target_template = list(filter(lambda i : i["id"] == args.template_id, templates["myself"]["podTemplates"]))
        save_response = await request_save_template(transport, args.image_name, target_template[0])
        sys.stdout.write(json.dumps(save_response, indent=2))
        sys.exit(0)
    except TransportError as e:
        sys.stderr.write(str(e))
        sys.exit(-1)
    except IndexError as e:
        sys.stderr.write(str(e))
        sys.exit(-1)


asyncio.run(main())
