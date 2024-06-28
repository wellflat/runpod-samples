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
    parser = argparse.ArgumentParser(description="Request GitHub GraphQL API")
    parser.add_argument("--token", type=str, default=None, help="GitHub Access Token (or GH_TOKEN env)")
    return parser.parse_args()

async def request(gql_path: Path, args: argparse.Namespace) -> dict[str, Any]:
    token = args.token if args.token else os.getenv("GH_TOKEN")
    with Path.open(gql_path) as f:
        lines = f.read()

    headers = {"Authorization": f"bearer {token}"}
    transport = AIOHTTPTransport(url="https://api.github.com/graphql", headers=headers)
    async with Client(transport=transport) as session:
        query = gql(lines)
        variables = {
            "number_of_repos": 3,
        }
        return await session.execute(query, parse_result=True)

async def main() -> None:
    try:
        args = parse_args()
        gql_path = Path(__file__).parent / "sample.gql"
        result = await request(gql_path, args)
        sys.stdout.write(json.dumps(result, indent=2))
    except TransportQueryError as e:
        sys.stderr.write(str(e))
    except TransportServerError as e:
        sys.stderr.write(str(e))

asyncio.run(main())
