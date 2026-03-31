"""
AI新闻编辑工作流主图编排
"""
from langgraph.graph import StateGraph, END
from graphs.state import (
    GlobalState,
    GraphInput,
    GraphOutput
)
from graphs.nodes.news_search_node import news_search_node
from graphs.nodes.news_filter_node import news_filter_node
from graphs.nodes.news_summary_node import news_summary_node
from graphs.nodes.format_output_node import format_output_node
from graphs.nodes.wechat_push_node import wechat_push_node


# 创建状态图
builder = StateGraph(
    GlobalState,
    input_schema=GraphInput,
    output_schema=GraphOutput
)

# 添加节点
# 1. 新闻搜索节点（使用web-search技能）
builder.add_node("news_search", news_search_node)

# 2. 新闻筛选与分类节点（Agent节点，使用LLM）
builder.add_node(
    "news_filter",
    news_filter_node,
    metadata={
        "type": "agent",
        "llm_cfg": "config/news_filter_llm_cfg.json"
    }
)

# 3. 新闻摘要生成节点（Agent节点，使用LLM）
builder.add_node(
    "news_summary",
    news_summary_node,
    metadata={
        "type": "agent",
        "llm_cfg": "config/news_summary_llm_cfg.json"
    }
)

# 4. 格式化输出节点（普通节点）
builder.add_node("format_output", format_output_node)

# 5. 企业微信推送节点（使用wechat-bot集成）
builder.add_node("wechat_push", wechat_push_node)

# 设置入口点
builder.set_entry_point("news_search")

# 添加边
builder.add_edge("news_search", "news_filter")
builder.add_edge("news_filter", "news_summary")
builder.add_edge("news_summary", "format_output")
builder.add_edge("format_output", "wechat_push")
builder.add_edge("wechat_push", END)

# 编译图
main_graph = builder.compile()
