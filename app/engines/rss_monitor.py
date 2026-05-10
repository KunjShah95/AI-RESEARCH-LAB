"""RSS Monitor - arXiv RSS feed monitoring"""

from typing import List, Optional
from datetime import datetime
from dataclasses import dataclass
import feedparser
from enum import Enum


class RSSCategory(str, Enum):
    AI = "cs.AI"
    ML = "cs.LG"
    CV = "cs.CV"
    CL = "cs.CL"
    NE = "stat.ML"


@dataclass
class RSSEntry:
    id: str
    title: str
    summary: str
    published: datetime
    authors: List[str]
    pdf_url: Optional[str]


class RSSMonitor:
    """Monitor arXiv RSS feeds for new papers"""

    BASE_URL = "http://export.arxiv.org/api/query"

    def __init__(self):
        self.subscriptions: dict = {}

    def fetch_feed(self, category: str, max_results: int = 20) -> List[RSSEntry]:
        """Fetch papers from arXiv RSS"""
        url = f"{self.BASE_URL}?search_query=cat:{category}&max_results={max_results}&sortBy=submittedDate&sortOrder=descending"

        try:
            feed = feedparser.parse(url)
            entries = []

            for entry in feed.entries:
                authors = (
                    [a.name for a in entry.authors] if hasattr(entry, "authors") else []
                )
                pdf_url = None
                if hasattr(entry, "links"):
                    for link in entry.links:
                        if link.type == "application/pdf":
                            pdf_url = link.href
                            break

                rss_entry = RSSEntry(
                    id=entry.id.split("/")[-1],
                    title=entry.title.replace("\n", " "),
                    summary=entry.summary[:500] if hasattr(entry, "summary") else "",
                    published=datetime(*entry.published_parsed[:6])
                    if hasattr(entry, "published_parsed")
                    else datetime.now(),
                    authors=authors,
                    pdf_url=pdf_url,
                )
                entries.append(rss_entry)

            return entries
        except Exception as e:
            print(f"RSS fetch error: {e}")
            return []

    def subscribe(self, user_id: str, category: str) -> dict:
        """Subscribe user to category feed"""
        if user_id not in self.subscriptions:
            self.subscriptions[user_id] = []

        if category not in self.subscriptions[user_id]:
            self.subscriptions[user_id].append(category)

        return {"user_id": user_id, "category": category, "subscribed": True}

    def unsubscribe(self, user_id: str, category: str) -> dict:
        """Unsubscribe from category"""
        if user_id in self.subscriptions and category in self.subscriptions[user_id]:
            self.subscriptions[user_id].remove(category)

        return {"user_id": user_id, "category": category, "subscribed": False}

    def get_subscriptions(self, user_id: str) -> List[str]:
        """Get user's subscriptions"""
        return self.subscriptions.get(user_id, [])


rss_monitor = RSSMonitor()
