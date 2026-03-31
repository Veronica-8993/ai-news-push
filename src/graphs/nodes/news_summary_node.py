"""
新闻摘要节点
"""
import logging
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from graphs.state import NewsSummaryInput, NewsSummaryOutput

logger = logging.getLogger(__name__)


def news_summary_node(
    state: NewsSummaryInput,
    config: RunnableConfig,
    runtime: Runtime[Context]
) -> NewsSummaryOutput:
    """
    title: 新闻摘要
    desc: 生成新闻摘要
    integrations: 无
    """
    
    for item in state.filtered_news_list:
        if not item.summary:
            item.summary = item.snippet[:60] if item.snippet else item.title[:60]
    
    return NewsSummaryOutput(final_news_list=state.filtered_news_list)
