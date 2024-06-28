#!/usr/bin/env python

import argparse
import asyncio
import os

from aiohttp import ClientSession

VERSIONS = list[tuple[int, str, str]]

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Manage GitHub Packages")
    parser.add_argument("--token", type=str, default=None, help="GitHub Access Token (or GH_TOKEN env)")
    parser.add_argument("--name", type=str, required=True, help="Target package name")
    return parser.parse_args()

async def get_package_versions(session: ClientSession, name: str, headers: dict) -> list[dict]:
    page = 1  # 真面目にページング処理するなら page / per_page パラメータを指定して走査する
    per_page = 100
    url = f"https://api.github.com/user/packages/container/{name}/versions?page={page}&per_page={per_page}"
    async with session.get(url, headers=headers) as response:
        return await response.json()

async def delete_package_versions(session: ClientSession, name: str, versions: VERSIONS, headers: dict) -> None:
    base_url = f"https://api.github.com/user/packages/container/{name}/versions"
    for version in versions:
        if "sha256:" in version[1]:
            url = f"{base_url}/{version[0]}"
            print(f"version name: {version[1]}")
            async with session.delete(url, headers=headers) as response:
                print(f"status: {response.status}")
                await asyncio.sleep(1)
        else:
            # tagではなくversionなのでsha256:~以外のパターンは無い?
            print(version[1])

async def main() -> None:
    args = parse_args()
    token = args.token if args.token else os.getenv("GH_TOKEN")
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "Authorization": f"Bearer {token}",
    }
    package_name = args.name
    async with ClientSession() as session:
        result = await get_package_versions(session, package_name, headers)
        versions = [(i["id"], i["name"], i["created_at"]) for i in result]
        print(f"{len(versions)} versions exists.")
        await delete_package_versions(session, package_name, versions, headers)

asyncio.run(main())
