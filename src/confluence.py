#!/usr/bin/env python

import argparse
import json
import os

from atlassian import Confluence


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Upload API document to Confluence")
    parser.add_argument("--url", type=str, help="Confluence Base URL")
    parser.add_argument("--user", type=str, required=True, help="Confluence username")
    parser.add_argument("--token", type=str, required=True, help="Confluence API token")
    return parser.parse_args()

def upload_document(url: str, user: str, token: str) -> None:
    confluence = Confluence(
        url=url,
        username=user,
        password=token,
        api_root="/wiki/api/v2/",
    )
    filename = "api.html"
    page_id = 3054567551
    ret = confluence.attach_file(
        filename,
        name="API外部仕様書.html",
        content_type="text/html",
        page_id=page_id,
        comment="ex) 2024/08/07 version 0.0.1"
    )
    print(json.dumps(ret, indent=2))

if __name__ == "__main__":
    CONFLUENCE_URL = os.getenv("CONFLUENCE_URL")
    CONFLUENCE_USER = os.getenv("CONFLUENCE_USER")
    CONFLUENCE_TOKEN = os.getenv("CONFLUENCE_TOKEN")

    args = parse_args()
    upload_document(args.url, args.user, args.token)


