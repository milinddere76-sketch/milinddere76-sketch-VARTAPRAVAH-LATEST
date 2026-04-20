"""
VartaPravah Services - News fetching, processing, and content generation
"""

from .news_fetcher import (
    get_marathi_news,
    fetch_from_api,
    fetch_from_rss,
    generate_ticker,
    NewsArticle
)

__all__ = [
    "get_marathi_news",
    "fetch_from_api",
    "fetch_from_rss",
    "generate_ticker",
    "NewsArticle"
]
