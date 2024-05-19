#!/usr/bin/env python

import json
import os
from pathlib import Path

from gql import Client
from gql import gql
from gql.transport.aiohttp import AIOHTTPTransport
from gql.transport.exceptions import TransportQueryError

if __name__ == "__main__":
    try:
        api_key = os.getenv("RUNPOD_API_KEY")
        transport = AIOHTTPTransport(
          url=f"https://api.runpod.io/graphql?api_key={api_key}",
        )
        client = Client(transport=transport)

        with Path.open(Path("runpod_save_template.gql")) as f:
            lines = f.read()

        query = gql(lines)
        result = client.execute(query)
        print(json.dumps(result, indent=2))
    except TransportQueryError as e:
        print(e)
