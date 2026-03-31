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
    desc: 将筛选和摘要后的新闻列表格式化为精简格式（适合企业微信单条消息）
    """
    ctx = runtime.context
    
    # 获取当前日期
    current_date = datetime.now().strftime("%Y年%m月%d日")
    
    # 按分类组织新闻
    categories = {
        "政策动态": [],
        "行业观察": [],
        "热点新闻": [],
        "国外动态": []
    }
    
    # 将新闻按分类分组
    for news_item in state.final_news_list:
        category = news_item.category
        if category in categories:
            categories[category].append(news_item)
    
    # 构建输出文本
    output_lines = []
    
    # 添加标题
    output_lines.append(f"📅 每日新闻精选 | {current_date}")
    output_lines.append("")
    
    # 按分类添加新闻
    for category_name, news_list in categories.items():
        if not news_list:
            continue
        
        output_lines.append(f"【{category_name}】")
        
        # 添加每条新闻（精简格式：序号 + 摘要，无链接）
        for idx, news_item in enumerate(news_list, 1):
            # 只保留摘要，去掉链接
            line = f"{idx}、{news_item.summary}"
            output_lines.append(line)
        
        output_lines.append("")
    
    # 合并输出文本
    formatted_output = "\n".join(output_lines).strip()
    
    # 检查消息长度，如果超过4000字节，进一步精简
    if len(formatted_output.encode('utf-8')) > 4000:
        # 重新生成，减少新闻数量
        output_lines = [f"📅 每日新闻精选 | {current_date}", ""]
        
        for category_name, news_list in categories.items():
            if not news_list:
                continue
            
            output_lines.append(f"【{category_name}】")
            
            # 每个分类最多5条
            for idx, news_item in enumerate(news_list[:5], 1):
                line = f"{idx}、{news_item.summary}"
                output_lines.append(line)
            
            output_lines.append("")
        
        formatted_output = "\n".join(output_lines).strip()
    
    return FormatOutputOutput(formatted_output=formatted_output)
