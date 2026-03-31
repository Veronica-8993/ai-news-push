"""
新闻摘要生成节点 - 使用LLM为每条新闻生成一句话摘要
"""
import os
import json
import logging
from typing import List
from jinja2 import Template
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from coze_coding_dev_sdk import LLMClient
from langchain_core.messages import SystemMessage, HumanMessage
from graphs.state import NewsSummaryInput, NewsSummaryOutput, NewsItem

# 配置日志
logger = logging.getLogger(__name__)


def news_summary_node(
    state: NewsSummaryInput,
    config: RunnableConfig,
    runtime: Runtime[Context]
) -> NewsSummaryOutput:
    """
    title: 新闻摘要生成
    desc: 使用大语言模型为每条新闻生成不超过50字的一句话摘要
    integrations: 大语言模型
    """
    ctx = runtime.context
    
    # 读取配置文件
    cfg_file = os.path.join(os.getenv("COZE_WORKSPACE_PATH", ""), config['metadata']['llm_cfg'])
    with open(cfg_file, 'r', encoding='utf-8') as fd:
        _cfg = json.load(fd)
    
    llm_config = _cfg.get("config", {})
    sp = _cfg.get("sp", "")
    up = _cfg.get("up", "")
    
    # 准备新闻列表数据
    filtered_news_data = []
    for item in state.filtered_news_list:
        filtered_news_data.append({
            "title": item.title,
            "url": item.url,
            "snippet": item.snippet,
            "source": item.source,
            "publish_time": item.publish_time,
            "category": item.category
        })
    
    # 使用jinja2模板渲染用户提示词
    up_tpl = Template(up)
    user_prompt_content = up_tpl.render(filtered_news_list=json.dumps(filtered_news_data, ensure_ascii=False, indent=2))
    
    # 初始化LLM客户端
    llm_client = LLMClient(ctx=ctx)
    
    # 构建消息
    messages = [
        SystemMessage(content=sp),
        HumanMessage(content=user_prompt_content)
    ]
    
    # 调用大模型
    response = llm_client.invoke(
        messages=messages,
        model=llm_config.get("model", "doubao-seed-2-0-pro-260215"),
        temperature=llm_config.get("temperature", 0.3),
        max_completion_tokens=llm_config.get("max_completion_tokens", 8192)
    )
    
    # 解析响应
    response_content = response.content
    if isinstance(response_content, list):
        # 如果是列表，提取文本部分
        text_parts = []
        for item in response_content:
            if isinstance(item, dict) and item.get("type") == "text":
                text_parts.append(item.get("text", ""))
        response_content = " ".join(text_parts)
    
    # 尝试解析JSON
    try:
        # 尝试找到JSON部分
        json_start = response_content.find("{")
        json_end = response_content.rfind("}") + 1
        if json_start != -1 and json_end > json_start:
            json_str = response_content[json_start:json_end]
            result = json.loads(json_str)
            
            # 提取最终新闻列表
            final_news_data = result.get("final_news", [])
            final_news_list: List[NewsItem] = []
            
            for item_data in final_news_data:
                news_item = NewsItem(
                    title=item_data.get("title", ""),
                    url=item_data.get("url", ""),
                    snippet=item_data.get("snippet", ""),
                    source=item_data.get("source", ""),
                    publish_time=item_data.get("publish_time", ""),
                    category=item_data.get("category", ""),
                    summary=item_data.get("summary", "")
                )
                final_news_list.append(news_item)
            
            return NewsSummaryOutput(final_news_list=final_news_list)
        else:
            logger.error("未找到有效的JSON响应")
            return NewsSummaryOutput(final_news_list=state.filtered_news_list)
            
    except json.JSONDecodeError as e:
        logger.error(f"JSON解析失败: {str(e)}")
        return NewsSummaryOutput(final_news_list=state.filtered_news_list)
