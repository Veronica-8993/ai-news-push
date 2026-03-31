"""
新闻搜索节点 - 使用免费API搜索AI新闻
"""
import os
import logging
import requests
from typing import List
from datetime import datetime, timezone
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from graphs.state import NewsSearchInput, NewsSearchOutput, NewsItem

logger = logging.getLogger(__name__)


def news_search_node(
    state: NewsSearchInput,
    config: RunnableConfig,
    runtime: Runtime[Context]
) -> NewsSearchOutput:
    """
    title: 新闻搜索
    desc: 使用免费API搜索AI新闻
    integrations: 无
    """
    
    all_news_items: List[NewsItem] = []
    
    # 方案1: Reddit AI新闻
    try:
        reddit_url = "https://www.reddit.com/r/artificial/hot.json?limit=15"
        headers = {"User-Agent": "AI-News-Bot/1.0"}
        resp = requests.get(reddit_url, headers=headers, timeout=15)
        
        if resp.status_code == 200:
            data = resp.json()
            for post in data.get("data", {}).get("children", []):
                post_data = post.get("data", {})
                created = post_data.get("created_utc", 0)
                pub_time = datetime.fromtimestamp(created, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+00:00") if created else ""
                
                all_news_items.append(NewsItem(
                    title=post_data.get("title", ""),
                    url=post_data.get("url", ""),
                    snippet=post_data.get("title", "")[:200],
                    source="Reddit",
                    publish_time=pub_time,
                    category="",
                    summary=""
                ))
    except Exception as e:
        logger.warning(f"Reddit fetch failed: {e}")
    
    # 方案2: Hacker News AI相关
    try:
        hn_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
        resp = requests.get(hn_url, timeout=10)
        
        if resp.status_code == 200:
            story_ids = resp.json()[:30]
            ai_keywords = ["ai", "artificial", "machine learning", "chatgpt", "openai", "gpt", "llm"]
            
            for story_id in story_ids:
                try:
                    story_resp = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json", timeout=5)
                    if story_resp.status_code == 200:
                        story = story_resp.json()
                        if story and story.get("title"):
                            title_lower = story.get("title", "").lower()
                            if any(kw in title_lower for kw in ai_keywords):
                                created = story.get("time", 0)
                                pub_time = datetime.fromtimestamp(created, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+00:00") if created else ""
                                
                                all_news_items.append(NewsItem(
                                    title=story.get("title", ""),
                                    url=story.get("url", "") or f"https://news.ycombinator.com/item?id={story_id}",
                                    snippet=story.get("title", ""),
                                    source="Hacker News",
                                    publish_time=pub_time,
                                    category="",
                                    summary=""
                                ))
                except:
                    continue
    except Exception as e:
        logger.warning(f"Hacker News fetch failed: {e}")
    
    # 去重
    unique_items = []
    seen_titles = set()
    for item in all_news_items:
        title_key = item.title.lower().strip()[:50]
        if title_key and title_key not in seen_titles:
            seen_titles.add(title_key)
            unique_items.append(item)
    
    logger.info(f"搜索完成，共 {len(unique_items)} 条新闻")
    return NewsSearchOutput(raw_news_list=unique_items[:25])
