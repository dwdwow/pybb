"""
A module for watching and handling news articles.

This module provides functionality to continuously monitor news articles from various sources
and handle new articles as they arrive. It includes functions for fetching, printing and 
watching for new articles.

Functions:
    printer: Prints article titles and timestamps in a formatted way
    watcher: Continuously monitors for new articles and handles them
"""

import datetime
import time
from typing import Callable, Dict, List
from apis import D, fetch_articles


def printer(news: List[D]):
    for n in news:
        ti = datetime.datetime.fromtimestamp(int(n["create_time"]), tz=datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        print(f"{n['title']} - {ti}")


def watcher(fetcher: Callable[[int, int, str], List[D]], handler: Callable[[List[D]], None]=printer):
    links: Dict[str, str] = {}
    while True:
        time.sleep(10)
        try:
            results = fetcher()
        except Exception as e:
            print(f"Error fetching {fetcher.__name__}: {e}")
            continue
        new_results: List[D] = []
        for n in results:
            link = n["link"]
            if link not in links:
                links[link] = n["create_time"]
                new_results.insert(0, n)
        if new_results:
            handler(new_results)


if __name__ == "__main__":
    # fetcher = fetch_flash_news
    fetcher = fetch_articles
    watcher(fetcher)