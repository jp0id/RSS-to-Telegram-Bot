#!/usr/bin/env python3

import asyncio
import os
import sys

import aiohttp

port = os.environ.get('PORT')
if not port:
    # This script is only used for the health check in the Docker container,
    # skip it if PORT is not set.
    print('Skipping health check as PORT is not set')
    sys.exit(0)


async def check_health():
    async with aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=3.0, connect=1.5),
            raise_for_status=False
    ) as session:
        try:
            async with session.get(f'http://127.0.0.1:{port}', allow_redirects=False) as response:
                status = response.status
        except aiohttp.ClientError as e:
            print(f'Health check failed: Connection error: {e}')
            sys.exit(1)
        if status < 400:
            # RSStT only returns 302 currently, but it should be OK to loosen the requirement in health check.
            print(f'Health check passed with status {status}')
            sys.exit(0)
        else:
            print(f'Health check failed with status {status}')
            sys.exit(1)


if __name__ == '__main__':
    asyncio.run(check_health())