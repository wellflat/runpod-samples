#!/usr/bin/env python

import argparse
import json
import os

from atlassian import Confluence


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Upload API document to Confluence")
    parser.add_argument("--url", type=str, required=True, help="Confluence Base URL")
    parser.add_argument("--user", type=str, required=True, help="Confluence username")
    parser.add_argument("--token", type=str, required=True, help="Confluence API token")
    parser.add_argument("--page", type=int, required=True, help="Confluence page ID")
    parser.add_argument("--name", type=str, default="openapi.html", help="API document filename")
    parser.add_argument("--comment", type=str, help="Comment for attachment")
    return parser.parse_args()

def upload_document(filename: str, page_id: int, url: str, user: str, token: str, comment: str) -> None:
    confluence = Confluence(
        url=url,
        username=user,
        password=token,
        api_root="/wiki/api/v2/",
    )
    ret = confluence.attach_file(
        filename,
        name=filename,
        content_type="text/html",
        page_id=page_id,
        comment=comment,
    )
    print(json.dumps(ret, indent=2))

if __name__ == "__main__":
    CONFLUENCE_URL = os.getenv("CONFLUENCE_URL")
    CONFLUENCE_USER = os.getenv("CONFLUENCE_USER")
    CONFLUENCE_TOKEN = os.getenv("CONFLUENCE_TOKEN")

    args = parse_args()
    upload_document(args.name, args.page, args.url, args.user, args.token, args.comment)

