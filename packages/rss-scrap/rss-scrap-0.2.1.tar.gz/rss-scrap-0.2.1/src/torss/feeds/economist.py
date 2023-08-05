import re
import urllib.parse
import asyncio

from torss.feed import Channel, Feed, Item
from torss.utils import fetch_bs, expect


async def fetch_urls(session):
    url = "https://www.economist.com/weeklyedition"

    soup = await fetch_bs(session, url)

    world_this_week = soup.find(re.compile(r"h\d"), string="The world this week")
    expect(world_this_week, "Couldn't get 'The world this week section'")
    section = world_this_week.find_parent("section")

    politics = section.find("a", string=re.compile(r"Politics.*"))
    business = section.find("a", string=re.compile(r"Business.*"))

    # KAL's uses a real typographic apostrophe (KAL’s cartoon) so to be safe,
    # let's skip it entirely with regular expression
    kal = section.find("a", string=re.compile(r"KAL.*cartoon"))

    urljoin = urllib.parse.urljoin

    ret = {}
    if politics:
        ret["politics"] = urljoin(url, politics["href"])
    if business:
        ret["business"] = urljoin(url, business["href"])
    if kal:
        ret["kal"] = urljoin(url, kal["href"])
    return ret


def lead_img_section_filter(tag):
    if tag.name != "section":
        return False

    figures = tag.find_all("figure")
    if len(figures) != 1:
        return False

    paragraphs = tag.find_all("p")
    if len(paragraphs) > 0:
        return False

    fig = figures[0]
    return any(d.name == "img" for d in fig.descendants)


def body_section_filter(tag):
    if tag.name != "section":
        return False

    paragraphs = tag.find_all("p")
    return len(paragraphs) > 0


def body_filter(tag):
    if tag.name == "p":
        return "your browser does" not in tag.text.lower()
    if tag.name in ("h1", "h2", "h3"):
        return tag.text != "Listen on the go"
    if tag.name == "img":
        return True
    return False


async def parse_article(session, url):

    contents = []

    soup = await fetch_bs(session, url)
    main = soup.find("main", id="content")

    lead_section = main.find(lead_img_section_filter)
    if lead_section:
        contents.append(lead_section.find("img"))

    body = main.find(body_section_filter)
    contents.extend(body.find_all(body_filter))

    return "\n".join(str(elem) for elem in contents)


async def politics(session, urls):
    expect("politics" in urls, "URL for Politics this week not found")
    url = urls["politics"]

    ch = Channel("The Economist: Politics this week", "https://www.economist.com")
    ch.items.append(
        Item(
            title="Politics this week",
            link=url,
            content=await parse_article(session, url),
        )
    )
    return Feed(ch, "politics.xml")


async def business(session, urls):
    expect("business" in urls, "URL for Business this week not found")
    url = urls["business"]

    ch = Channel("The Economist: Business this week", "https://www.economist.com")
    ch.items.append(
        Item(
            title="Business this week",
            link=url,
            content=await parse_article(session, url),
        )
    )
    return Feed(ch, "business.xml")


async def kal(session, urls):
    expect("kal" in urls, "URL for KAL's cartoon not found")
    url = urls["kal"]

    ch = Channel("The Economist: KAL's cartoon", "https://www.economist.com")
    ch.items.append(
        Item(
            title="KAL's cartoon",
            link=url,
            content=await parse_article(session, url),
        )
    )
    return Feed(ch, "kal.xml")


async def run(session, **kw):
    urls = await fetch_urls(session)
    feeds = await asyncio.gather(
        politics(session, urls), business(session, urls), kal(session, urls)
    )
    return feeds
