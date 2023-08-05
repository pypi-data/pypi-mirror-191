#!/usr/bin/env python3

import sys
import argparse
import datetime

dt = datetime.datetime
tz = datetime.timezone


from bs4 import Comment

from torss.feed import Channel, Feed, Item
from torss.utils import fetch_bs, pub_date_fmt


def today():
    t = datetime.date.today()
    return t.strftime("%Y-%m-%d")


def string_filter(string):
    return isinstance(string, Comment)


def tag_filter(tag):
    fs = [
        ("class", lambda c: c and "editlink" in c),
        ("role", lambda r: r == "navigation"),
        ("style", lambda s: s and "display:none" in s),
    ]

    return any(fn(tag.attrs.get(name)) for name, fn in fs)


def tag_strip(tag):
    fs = [
        lambda: tag.name == "div",
        lambda: tag.name == "span",
    ]

    return any(fn() for fn in fs)


async def run(session, date=today(), **kw):
    date_dt = datetime.date.fromisoformat(date)
    date_human = datetime.date.today().strftime("%Y %B %d")
    urlbase = "https://en.wikipedia.org/wiki/Portal:Current_events"
    urlremainder = date_dt.strftime("%Y_%B_%-d")
    url = "{}/{}".format(urlbase, urlremainder)

    ch = Channel(
        "Wikipedia: Portal: Current events", urlbase, "Current events on Wikipedia"
    )

    soup = await fetch_bs(session, url)
    content = soup.find(class_="mw-parser-output")
    if content:
        to_remove = content.find_all(string=string_filter)
        to_remove.extend(content.find_all(tag_filter))
        for elem in to_remove:
            elem.extract()

        to_strip = content.find_all(tag_strip)
        for elem in to_strip:
            elem.unwrap()

        pub = dt.combine(date_dt, dt.min.time(), tzinfo=tz.utc)
        ch.items.append(
            Item(
                title="Current events: {}".format(date_human),
                link=url,
                content=str(content),
                pub=pub_date_fmt(pub)
            )
        )

    return Feed(ch)
