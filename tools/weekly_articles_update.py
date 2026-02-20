from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional

import feedparser
import requests
from dateutil import parser as dtparser

ARTICLES_MD = Path("content/community/articles.md")

PE_RSS = "https://platformengineering.org/blog/rss.xml"
WEAVE_RSS = "https://api.feedifyrss.com/weaveintelligence/research/feed.xml"

WEEK_LOOKBACK_DAYS = 7
UA = "weekly-articles-bot/1.0 (+github-actions)"


@dataclass(frozen=True)
class Post:
    title: str
    url: str
    published: datetime  # UTC tz-aware
    attribution: str


def _to_utc(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def _extract_existing_urls(md: str) -> set[str]:
    return set(re.findall(r"https?://[^\s)>\"]+", md))


def _fetch_feed(url: str) -> feedparser.FeedParserDict:
    # feedparser can fetch URLs itself, but using requests gives us better headers/timeouts.
    r = requests.get(url, headers={"User-Agent": UA}, timeout=30)
    r.raise_for_status()
    return feedparser.parse(r.content)


def _entry_datetime(entry: feedparser.FeedParserDict) -> Optional[datetime]:
    # Prefer structured fields if present
    for key in ("published", "updated"):
        if key in entry:
            try:
                return _to_utc(dtparser.parse(entry[key]))
            except Exception:
                pass

    # Some feeds provide parsed structs
    for key in ("published_parsed", "updated_parsed"):
        if key in entry and entry[key]:
            try:
                # time.struct_time -> timestamp
                ts = datetime(*entry[key][:6], tzinfo=timezone.utc)
                return ts
            except Exception:
                pass

    return None


def _entry_link(entry: feedparser.FeedParserDict) -> Optional[str]:
    if "link" in entry and entry["link"]:
        return entry["link"]
    # fallback: look through links
    for l in entry.get("links", []):
        href = l.get("href")
        if href:
            return href
    return None


def _clean_title(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "").strip())


def posts_from_rss(feed_url: str, attribution: str, cutoff_utc: datetime) -> list[Post]:
    feed = _fetch_feed(feed_url)

    posts: list[Post] = []
    for entry in feed.entries:
        link = _entry_link(entry)
        if not link:
            continue

        title = _clean_title(entry.get("title", ""))
        if not title:
            continue

        published = _entry_datetime(entry)
        if not published or published < cutoff_utc:
            continue

        posts.append(Post(title=title, url=link, published=published, attribution=attribution))

    # newest first
    posts.sort(key=lambda p: p.published, reverse=True)
    return posts


def _ensure_year_section(md: str, year: int) -> str:
    if re.search(rf"^##\s+{year}\b", md, flags=re.MULTILINE):
        return md

    # Insert before the first year heading if present, else append
    m = re.search(r"^##\s+\d{4}\b", md, flags=re.MULTILINE)
    insert = f"\n## {year}\n"
    if m:
        return md[: m.start()] + insert + md[m.start() :]
    return md.rstrip() + insert


def _insert_posts_into_year(md: str, year: int, new_posts: list[Post]) -> str:
    heading = re.search(rf"^##\s+{year}\b.*$", md, flags=re.MULTILINE)
    if not heading:
        raise RuntimeError(f"Could not find year section for {year}")

    insert_at = heading.end()

    # Match existing page style: two spaces before '*'
    bullet_lines = [f"  * [{p.title}]({p.url}) {p.attribution}" for p in new_posts]
    block = "\n" + "\n".join(bullet_lines) + "\n"
    return md[:insert_at] + block + md[insert_at:]


def main() -> None:
    if not ARTICLES_MD.exists():
        raise SystemExit(f"Expected file not found: {ARTICLES_MD}")

    md = ARTICLES_MD.read_text(encoding="utf-8")
    existing_urls = _extract_existing_urls(md)

    now_utc = datetime.now(timezone.utc)
    cutoff_utc = now_utc - timedelta(days=WEEK_LOOKBACK_DAYS)
    year = now_utc.year

    pe_posts = posts_from_rss(PE_RSS, "Platform Engineering", cutoff_utc)
    weave_posts = posts_from_rss(WEAVE_RSS, "Weave Intelligence", cutoff_utc)

    fresh = [p for p in (pe_posts + weave_posts) if p.url not in existing_urls]

    # Optional guardrail: avoid runaway PRs if something changes in the feed
    MAX_NEW = 20
    fresh = sorted(fresh, key=lambda p: p.published, reverse=True)[:MAX_NEW]

    if not fresh:
        print("No new RSS posts found for the last week. No changes made.")
        return

    md = _ensure_year_section(md, year)
    md = _insert_posts_into_year(md, year, fresh)

    ARTICLES_MD.write_text(md, encoding="utf-8")
    print(f"Added {len(fresh)} new post(s) to {ARTICLES_MD}")


if __name__ == "__main__":
    main()
