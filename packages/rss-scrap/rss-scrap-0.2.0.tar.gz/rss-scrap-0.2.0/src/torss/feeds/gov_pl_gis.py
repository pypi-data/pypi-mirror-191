import asyncio
from urllib.parse import urljoin
from datetime import datetime, timezone

from torss.feed import Channel, Feed, Item
from torss.utils import fetch_bs, pub_date_fmt

BASE_URL = "https://www.gov.pl/web/gis/ostrzezenia"


async def get_article(session, li):
    relurl = li.a["href"]
    url = relurl if relurl.startswith("http") else urljoin(BASE_URL, relurl)
    soup = await fetch_bs(session, url)
    article = soup.find("article", id="main-content")

    title = article.h2.text
    date = datetime.strptime(
        article.find(class_="event-date").text, "%d.%m.%Y"
    ).replace(tzinfo=timezone.utc)
    content = article.find(class_="editor-content")

    return Item(title, str(content), link=url, pub=pub_date_fmt(date))


async def run(session):
    metadata = {
        "feed_title": "Główny Inspektorat Sanitarny - Ostrzeżenia",
        "feed_link": BASE_URL,
        "feed_descr": "Ostrzeżenia GIS",
        "title": "Ostrzeżenia GIS",
        "link": BASE_URL,
        "guid": BASE_URL,
    }

    soup = await fetch_bs(session, BASE_URL)
    content = soup.find(class_="article-area")
    if not content:
        return

    ch = Channel("Główny Inspektorat Sanitarny - Ostrzeżenia", BASE_URL)

    article_list = content.article.ul
    tasks = [get_article(session, li) for li in article_list.find_all("li")]
    ch.items = await asyncio.gather(*tasks)

    return Feed(ch, "gis_warnings.xml")
