from typing import List
from dataclasses import dataclass, field
from datetime import datetime
from contextlib import contextmanager
import html

from torss.utils import utcnow

_LEVEL = 0


@contextmanager
def _indent():
    global _LEVEL
    _LEVEL += 1
    indent = "  " * _LEVEL
    yield indent
    _LEVEL -= 1


class Element:
    def __init__(self, tag, text=None, **kw):
        self.tag = tag
        self.text = text
        self.attrs = [(key, val) for key, val in kw.items()]

    def __format__(self, spec):
        if not self.text:
            return ""

        with _indent() as ind:
            if self.attrs:
                attrs = " " + " ".join(
                    '{}="{}"'.format(key, val) for key, val in self.attrs
                )
            else:
                attrs = ""

            text = html.escape(self.text)
            return f"{ind}<{self.tag}{attrs}>{text}</{self.tag}>\n"


@dataclass
class Item:
    title: str
    content: str
    link: str
    guid: str = ""
    pub: str = utcnow()

    def __post_init__(self):
        if not self.guid:
            self.guid = self.link

    def __format__(self, spec):
        if not self.title and not self.content:
            return ""

        guid_attrs = {}
        if not self.guid.startswith("http"):
            guid_attrs["isPermaLink"] = "false"

        with _indent() as ind:
            return (
                f"{ind}<item>\n"
                + format(Element("title", self.title))
                + format(Element("description", self.content))
                + format(Element("link", self.link))
                + format(Element("pubDate", self.pub))
                + format(Element("guid", self.guid, **guid_attrs))
                + f"{ind}</item>\n"
            )


@dataclass
class Channel:
    title: str
    link: str
    descr: str = ""
    pub: datetime = utcnow()
    items: List[Item] = field(default_factory=list)

    def __post_init__(self):
        if not self.descr:
            self.descr = f"RSS feed scrapped by torss from {self.link}"

    def __format__(self, spec):
        E = Element
        with _indent() as ind:
            return (
                f"{ind}<channel>\n"
                + format(Element("title", self.title))
                + format(Element("description", self.descr))
                + format(Element("link", self.link))
                + format(Element("pubDate", self.pub))
                + "\n".join(format(item) for item in self.items)
                + f"{ind}</channel>\n"
            )


@dataclass
class Feed:
    channel: Channel
    file: str = "feed.xml"
