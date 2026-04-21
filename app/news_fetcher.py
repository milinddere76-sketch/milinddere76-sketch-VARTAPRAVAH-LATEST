#!/usr/bin/env python3
"""
VARTAPRAVAH - Auto News Fetcher
Fetches news from multiple sources (India, Maharashtra, World)
Uses NewsAPI and WorldNews API
"""

import requests
import logging
from datetime import datetime
from typing import List, Dict, Optional
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class NewsArticle(BaseModel):
    """News article data model"""
    title: str
    description: Optional[str] = None
    source: str
    category: str  # "India", "Maharashtra", "World"
    url: Optional[str] = None
    image_url: Optional[str] = None
    timestamp: str


class NewsCategory:
    INDIA = "India"
    MAHARASHTRA = "Maharashtra"
    WORLD = "World"


class NewsFetcher:
    """
    Fetches news from multiple APIs
    Supports: NewsAPI, WorldNews API
    """
    
    def __init__(self, newsapi_key: Optional[str] = None, worldnews_key: Optional[str] = None):
        """
        Initialize news fetcher with API keys
        
        Args:
            newsapi_key: NewsAPI key (get from https://newsapi.org/)
            worldnews_key: WorldNews API key (get from https://worldnewsapi.com/)
        """
        import os
        
        self.newsapi_key = newsapi_key or os.getenv("NEWSAPI_KEY", "demo")
        self.worldnews_key = worldnews_key or os.getenv("WORLDNEWS_API_KEY", "demo")
        self.newsapi_url = "https://newsapi.org/v2"
        self.worldnews_url = "https://api.worldnewsapi.com"
        
    def fetch_india_news(self, limit: int = 5) -> List[NewsArticle]:
        """Fetch top India news headlines"""
        try:
            url = f"{self.newsapi_url}/top-headlines"
            params = {
                "country": "in",
                "apiKey": self.newsapi_key,
                "pageSize": limit,
                "sortBy": "publishedAt"
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            articles = []
            for article in data.get("articles", []):
                articles.append(NewsArticle(
                    title=article.get("title", ""),
                    description=article.get("description", ""),
                    source=article.get("source", {}).get("name", "Unknown"),
                    category=NewsCategory.INDIA,
                    url=article.get("url", ""),
                    image_url=article.get("urlToImage", ""),
                    timestamp=datetime.now().strftime("%H:%M")
                ))
            
            logger.info(f"✅ Fetched {len(articles)} India news articles")
            return articles
            
        except Exception as e:
            logger.error(f"❌ Error fetching India news: {str(e)}")
            return []
    
    def fetch_maharashtra_news(self, limit: int = 5) -> List[NewsArticle]:
        """Fetch Maharashtra news"""
        try:
            url = f"{self.newsapi_url}/everything"
            params = {
                "q": "Maharashtra",
                "apiKey": self.newsapi_key,
                "pageSize": limit,
                "sortBy": "publishedAt",
                "language": "en"
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            articles = []
            for article in data.get("articles", []):
                articles.append(NewsArticle(
                    title=article.get("title", ""),
                    description=article.get("description", ""),
                    source=article.get("source", {}).get("name", "Unknown"),
                    category=NewsCategory.MAHARASHTRA,
                    url=article.get("url", ""),
                    image_url=article.get("urlToImage", ""),
                    timestamp=datetime.now().strftime("%H:%M")
                ))
            
            logger.info(f"✅ Fetched {len(articles)} Maharashtra news articles")
            return articles
            
        except Exception as e:
            logger.error(f"❌ Error fetching Maharashtra news: {str(e)}")
            return []
    
    def fetch_world_news(self, limit: int = 5) -> List[NewsArticle]:
        """Fetch world news headlines"""
        try:
            url = f"{self.newsapi_url}/top-headlines"
            params = {
                "category": "general",
                "apiKey": self.newsapi_key,
                "pageSize": limit,
                "sortBy": "publishedAt"
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            articles = []
            for article in data.get("articles", []):
                articles.append(NewsArticle(
                    title=article.get("title", ""),
                    description=article.get("description", ""),
                    source=article.get("source", {}).get("name", "Unknown"),
                    category=NewsCategory.WORLD,
                    url=article.get("url", ""),
                    image_url=article.get("urlToImage", ""),
                    timestamp=datetime.now().strftime("%H:%M")
                ))
            
            logger.info(f"✅ Fetched {len(articles)} World news articles")
            return articles
            
        except Exception as e:
            logger.error(f"❌ Error fetching World news: {str(e)}")
            return []
    
    def fetch_all_news(self, limit: int = 5) -> Dict[str, List[NewsArticle]]:
        """Fetch news from all categories"""
        logger.info("🌐 Starting auto news fetch from all sources...")
        
        return {
            NewsCategory.INDIA: self.fetch_india_news(limit),
            NewsCategory.MAHARASHTRA: self.fetch_maharashtra_news(limit),
            NewsCategory.WORLD: self.fetch_world_news(limit)
        }
    
    def filter_duplicate_titles(self, articles: List[NewsArticle]) -> List[NewsArticle]:
        """Remove duplicate articles based on title"""
        seen_titles = set()
        filtered = []
        
        for article in articles:
            if article.title not in seen_titles:
                seen_titles.add(article.title)
                filtered.append(article)
        
        return filtered


def get_news_fetcher() -> NewsFetcher:
    """Factory function to create NewsFetcher instance"""
    return NewsFetcher()


if __name__ == "__main__":
    # Test the news fetcher
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    fetcher = NewsFetcher()
    all_news = fetcher.fetch_all_news(limit=3)
    
    for category, articles in all_news.items():
        print(f"\n📰 {category} News ({len(articles)} articles)")
        print("=" * 60)
        for i, article in enumerate(articles, 1):
            print(f"{i}. {article.title}")
            print(f"   Source: {article.source}")
            print(f"   Time: {article.timestamp}")
            if article.description:
                print(f"   Summary: {article.description[:100]}...")
            print()
