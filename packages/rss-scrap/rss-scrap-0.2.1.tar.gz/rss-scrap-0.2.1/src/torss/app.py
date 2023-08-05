import os
import sys
import asyncio
import pkgutil
import logging
import subprocess

from typing import List, Iterable

import aiohttp

from torss.args import ArgumentParser
from torss.feed import Channel

log = logging.getLogger(__name__)

cli = ArgumentParser()
cli.parser.add_argument(
    "-f",
    "--feed",
    action="append",
    default=[],
    dest="feeds",
    help=(
        "name of the feed to fetch. Each feed occupies a single -f option and "
        "can be optionally followed by feed-specific comma-separated options, "
        "e.g. -f economist -f wiki_current_events,date=2022-02-28"
    ),
)
cli.parser.add_argument(
    "-o",
    "--output-dir",
    default="_torss",
    help="path to the directory where torss will store feeds",
)


def load_fetcher(names: Iterable[str]) -> Iterable:
    path = os.path.join(os.path.dirname(__file__), "feeds")
    for finder, name, ispkg in pkgutil.iter_modules([path]):
        if name.startswith("_"):
            continue

        if name not in names:
            continue

        found = finder.find_module(name)

        if not found:
            log.error(f"No such feed fetcher: {name}")
            continue

        return found.load_module()
    return None


def save_feed(ch: Channel, outf: str):
    print("""<?xml version="1.0" encoding="utf-8" standalone="yes" ?>""", file=outf)
    print("""<rss version="2.0">""", file=outf)

    print(format(ch), file=outf)

    print("""</rss>""", file=outf)


def parse_opt(kv):
    key, _, val = kv.partition("=")
    key = key.strip().lower()
    val = val.strip()
    return key, val


def parse_fetcher_options(feeds):
    fetchers = {}
    for feed in feeds:
        fetcher, _, opt_line = feed.partition(",")
        fetcher = fetcher.strip().lower()
        opts = {}

        for kv in opt_line.split(","):
            key, val = parse_opt(kv)
            if key and val:
                opts[key] = val

        fetchers[fetcher] = opts

    return fetchers


async def fetch_rss(args):
    async with aiohttp.ClientSession(trust_env=True) as session:
        fetchers_map = parse_fetcher_options(args.feeds)

        tasks = []
        used_fetchers = []

        for name, opts in fetchers_map.items():
            f = load_fetcher(name)
            if f:
                used_fetchers.append(name)
                tasks.append(f.run(session, **opts))

        return used_fetchers, await asyncio.gather(*tasks)


def write_results(output_dir, names, results):
    for i, feeds in enumerate(results):
        if not isinstance(feeds, (list, tuple)):
            feeds = [feeds]

        feed_dir = os.path.join(output_dir, names[i])
        os.makedirs(feed_dir, exist_ok=True)
        for feed in feeds:
            with open(os.path.join(feed_dir, feed.file), "w") as of:
                save_feed(feed.channel, of)


async def main_():
    args = cli.parse_args()

    if not args.feeds:
        return 0

    names, results = await fetch_rss(args)
    write_results(args.output_dir, names, results)


def main():
    loop = asyncio.get_event_loop()
    sys.exit(loop.run_until_complete(main_()))
