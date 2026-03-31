"""
格式化输出节点 - 将新闻列表格式化为指定格式
"""
from datetime import datetime
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from graphs.state import FormatOutputInput, FormatOutputOutput


def format_output_node(
    state: FormatOutputInput,
    config: RunnableConfig,
    runtime: Runtime[Context]
) -> FormatOutputOutput:
    """
    title: 格式化输出
    desc: 将筛选和摘要后的新闻列表格式化为精简格式
    """
    
    current_date = datetime.now().strftime("%Y年%m月%d日")
    
    categories = {
        "政策动态": [],
        "行业观察": [],
        "热点新闻": [],
        "国外动态": []
    }
    
    for news_item in state.final_news_list:
        category = news_item.category or "热点新闻"
        if category in categories:
            categories[category].append(news_item)
        else:
            categories["热点新闻"].append(news_item)
    
    output_lines = [f"📅 每日新闻精选 | {current_date}", ""]
    
    for category_name, news_list in categories.items():
        if not news_list:
            continue
        
        output_lines.append(f"【{category_name}】")
        
        for idx, news_item in enumerate(news_list, 1):
            # 关键修复：如果 summary 为空，使用 snippet 或 title
            content = news_item.summary or news_item.snippet or news_item.title
            line = f"{idx}、{content}"
            output_lines.append(line)
        
        output_lines.append("")
    
    formatted_output = "\n".join(output_lines).strip()
    
    if len(formatted_output.encode('utf-8')) > 4000:
        formatted_output = formatted_output[:3900]
    
    return FormatOutputOutput(formatted_output=formatted_output)
