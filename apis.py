"""
BlockBeats API client for accessing news and articles.

This module provides a simple interface to the BlockBeats RESTful API for retrieving flash news 
and articles in multiple languages.

Example:
    >>> from apis import flash_news, articles
    >>> news = flash_news(size=5)  # Get 5 latest flash news items
    >>> arts = articles(lang="zh")  # Get Chinese language articles

Types:
    FlashNews: TypedDict containing flash news item fields
        - id: Unique identifier
        - title: News headline
        - content: News content
        - pic: Image URL
        - link: Source link
        - url: BlockBeats URL
        - create_time: Creation timestamp

    Article: TypedDict containing article fields
        - title: Article title
        - description: Short description
        - content: Article content
        - link: Source link
        - pic: Image URL
        - column: Category/column
        - create_time: Creation timestamp
        - is_original: Whether article is original content
"""

from typing import List, TypeVar, TypedDict
import requests

# https://github.com/BlockBeatsOfficial/RESTful-API
base_url = "https://api.theblockbeats.news/v1/open-api"

Data = TypedDict("Data", {"link": str, "create_time": int, "title": str, "content": str, "pic": str})

D = TypeVar("D", bound=Data)

Page = TypedDict("Page", {"page": int, "data": List[D]})

RespData = TypedDict("RespData", {"status": int, "message": str, "data": Page[D]})

FlashNews = TypedDict("FlashNews", {
    "id": int,
    "title": str, 
    "content": str,
    "pic": str,
    "link": str,
    "url": str,
    "create_time": str
})

Article = TypedDict("Article", {
    "title": str,
    "description": str, 
    "content": str,
    "link": str,
    "pic": str,
    "column": str,
    "create_time": str,
    "is_original": bool
})

def fetch(path: str, size=10, page=1, lang="en") -> List[D]:
    url = f"{base_url}/{path.lstrip('/')}?size={size}&page={page}&lang={lang}"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch {path}: {response.status_code} {response.text}")
    d = response.json()
    if d["status"] != 0:
        raise Exception(f"Failed to fetch {path}: {d['message']}")
    return d["data"]["data"]


def fetch_flash_news(size=10, page=1, lang="en") -> List[FlashNews]:
    return fetch("open-flash", size, page, lang)


def fetch_articles(size=10, page=1, lang="en") -> List[Article]:
    return fetch("open-information", size, page, lang)


if __name__ == "__main__":
    print(fetch_flash_news())
    # print(fetch_articles())
