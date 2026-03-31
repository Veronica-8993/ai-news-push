"""
新闻筛选节点
"""
import os
import json
import logging
from typing import List
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from graphs.state import NewsFilterInput, NewsFilterOutput, NewsItem

logger = logging.getLogger(__name__)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")


def news_filter_node(
    state: NewsFilterInput,
    config: RunnableConfig,
    runtime: Runtime[Context]
) -> NewsFilterOutput:
    """
    title: 新闻筛选
    desc: 筛选AI相关新闻并分类
    integrations: 无
    """
    
    # 简单筛选：按标题关键词分类
    categories = {
        "政策动态": ["policy", "regulation", "law", "government", "policy", "法规", "政策"],
        "行业观察": ["openai", "google", "meta", "百度", "阿里", "腾讯", "startup", "funding", "融资", "投资"],
        "国外动态": ["us", "eu", "europe", "america", "美国", "欧洲"]
    }
    
    filtered = []
    for item in state.raw_news_list:
        title_lower = item.title.lower()
        
        # 确定分类
        category = "热点新闻"
        for cat, keywords in categories.items():
            if any(kw in title_lower for kw in keywords):
                category = cat
                break
        
        item.category = category
        item.summary = item.snippet[:60] if item.snippet else item.title[:60]
        filtered.append(item)
    
    return NewsFilterOutput(filtered_news_list=filtered[:15])
