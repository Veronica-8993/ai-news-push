"""
新闻搜索节点 - 使用web-search技能搜索AI人工智能相关新闻
"""
import json
import logging
import re
from typing import List
from datetime import datetime, timedelta, timezone
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from coze_coding_dev_sdk import SearchClient
from coze_coding_utils.runtime_ctx.context import new_context
from graphs.state import NewsSearchInput, NewsSearchOutput, NewsItem

# 配置日志
logger = logging.getLogger(__name__)


def parse_publish_time(publish_time_str: str) -> datetime:
    """
    解析发布时间字符串为datetime对象
    支持多种时间格式，包括相对时间
    """
    if not publish_time_str:
        return None
    
    # 尝试多种时间格式
    time_formats = [
        "%Y-%m-%dT%H:%M:%S%z",  # ISO 8601 with timezone (2026-03-27T08:39:00+08:00)
        "%Y-%m-%dT%H:%M:%S",    # ISO 8601 without timezone
        "%Y-%m-%d %H:%M:%S",    # Standard datetime
        "%Y-%m-%d",             # Date only
        "%Y/%m/%d %H:%M:%S",    # Alternative format
        "%Y/%m/%d",             # Alternative date only
    ]
    
    for fmt in time_formats:
        try:
            dt = datetime.strptime(publish_time_str, fmt)
            # 如果没有时区信息，假设为本地时间
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt
        except (ValueError, TypeError):
            continue
    
    # 尝试解析相对时间（如"22分钟前"、"2小时前"）
    try:
        if "分钟前" in publish_time_str:
            minutes = int(re.search(r'(\d+)分钟前', publish_time_str).group(1))
            return datetime.now(timezone.utc) - timedelta(minutes=minutes)
        elif "小时前" in publish_time_str:
            hours = int(re.search(r'(\d+)小时前', publish_time_str).group(1))
            return datetime.now(timezone.utc) - timedelta(hours=hours)
        elif "天前" in publish_time_str:
            days = int(re.search(r'(\d+)天前', publish_time_str).group(1))
            return datetime.now(timezone.utc) - timedelta(days=days)
    except (AttributeError, ValueError):
        pass
    
    return None


def is_within_24_hours(publish_time_str: str, current_time: datetime) -> bool:
    """
    判断发布时间是否在过去24小时内
    如果无法解析时间，返回True（保留该新闻）
    """
    publish_time = parse_publish_time(publish_time_str)
    
    # 如果无法解析时间，保守起见保留该新闻
    if publish_time is None:
        return True
    
    # 计算时间差
    time_diff = current_time - publish_time
    
    # 判断是否在24小时内
    return time_diff <= timedelta(hours=24)


def news_search_node(
    state: NewsSearchInput,
    config: RunnableConfig,
    runtime: Runtime[Context]
) -> NewsSearchOutput:
    """
    title: 新闻搜索
    desc: 使用web-search技能搜索多个权威媒体的AI领域新闻
    integrations: web-search
    """
    ctx = runtime.context
    
    # 初始化搜索客户端
    search_client = SearchClient(ctx=ctx)
    
    # 定义权威新闻源关键词（用于搜索）
    authority_sources = [
        "量子位",
        "人民日报 AI",
        "新华网 人工智能",
        "虎嗅 AI",
        "网易科技 AI",
        "36氪 AI",
        "钛媒体 AI",
        "界面新闻 AI",
        "财新网 AI",
        "科技日报 AI",
        "中国新闻网 AI",
        "经济日报 AI"
    ]
    
    # 定义搜索查询列表
    search_queries = [
        # AI 人工智能（优先级最高）
        "AI 人工智能 最新动态",
        "大模型 ChatGPT GPT 最新",
        "人工智能 行业 应用 落地",
        "AI 芯片 算力 发展",
        "机器学习 深度学习 突破",
        
        # AI 企业动态
        "OpenAI Google AI 百度 阿里 腾讯 AI",
        "字节跳动 AI 大模型",
        "华为 AI 芯片 昇腾",
        "AI 创业 投资 融资",
        
        # AI 行业应用
        "AI 医疗 金融 教育 应用",
        "自动驾驶 AI 汽车",
        "AI 机器人 最新进展",
        
        # 科技热点
        "科技新闻 最新突破",
        "人工智能 政策 法规"
    ]
    
    # 存储所有搜索结果
    all_news_items: List[NewsItem] = []
    
    # 获取当前时间（用于24小时过滤）
    current_time = datetime.now(timezone.utc)
    
    # 执行多个搜索查询
    for query in search_queries:
        try:
            # 使用search方法搜索，添加time_range参数限制为24小时内
            response = search_client.search(
                query=query,
                search_type="web",
                count=15,  # 增加每个查询返回的结果数量
                need_summary=True,
                time_range="1d"  # 仅搜索过去24小时内的新闻
            )
            
            # 处理搜索结果
            if response.web_items:
                for item in response.web_items:
                    # 严格的时间过滤：只保留过去24小时内的新闻
                    if item.publish_time:
                        if not is_within_24_hours(item.publish_time, current_time):
                            # 跳过超过24小时的新闻
                            continue
                    
                    # 创建NewsItem对象
                    news_item = NewsItem(
                        title=item.title or "",
                        url=item.url or "",
                        snippet=item.snippet or "",
                        source=item.site_name or "",
                        publish_time=item.publish_time or "",
                        category="",  # 分类将在后续节点中填充
                        summary=""  # 摘要将在后续节点中填充
                    )
                    all_news_items.append(news_item)
        except Exception as e:
            # 记录错误但继续执行
            logger.error(f"搜索查询 '{query}' 失败: {str(e)}")
            continue
    
    # 去重：根据URL去重
    unique_news_items: List[NewsItem] = []
    seen_urls = set()
    
    for item in all_news_items:
        if item.url and item.url not in seen_urls:
            seen_urls.add(item.url)
            unique_news_items.append(item)
    
    logger.info(f"搜索完成，共找到 {len(unique_news_items)} 条过去24小时内的新闻")
    
    return NewsSearchOutput(raw_news_list=unique_news_items)
