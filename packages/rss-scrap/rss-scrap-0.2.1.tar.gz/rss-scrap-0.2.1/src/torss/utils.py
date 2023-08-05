import sys
import asyncio
from datetime import timezone, datetime

import aiohttp


def eprint(*a, **kw):
    kw["file"] = sys.stderr
    print(*a, **kw)


def die(msg, code=1):
    eprint(msg, file=sys.stderr)
    sys.exit(code)


def expect(expr, msg, code=1):
    if not expr:
        die(msg, code)


async def fetch_bs(session, url, retries_on_timeout=5):
    from bs4 import BeautifulSoup

    timeouts = [5]
    for _ in range(retries_on_timeout):
        timeouts.append(timeouts[-1] * 2)
    timeouts = [aiohttp.ClientTimeout(total=t) for t in timeouts]

    for i, t in enumerate(timeouts):
        try:
            async with session.get(url, timeout=t) as resp:
                return BeautifulSoup(await resp.text(), "html.parser")
        except asyncio.TimeoutError:
            if i + 1 < len(timeouts):
                eprint(f"Timeout: {url}. Retrying with timeout={timeouts[i+1].total}")

    raise asyncio.TimeoutError(url)


def pub_date_fmt(dt: datetime):
    return dt.strftime("%a, %d %b %Y %H:%M:%S %z")


def utcnow():
    tm = datetime.now(timezone.utc)
    return pub_date_fmt(tm)
