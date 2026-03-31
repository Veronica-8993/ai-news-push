"""
AI新闻编辑工作流状态定义
"""
from typing import List, Optional
from pydantic import BaseModel, Field


class NewsItem(BaseModel):
    """单条新闻数据"""
    title: str = Field(..., description="新闻标题")
    url: str = Field(..., description="新闻链接")
    snippet: str = Field(default="", description="新闻摘要")
    source: str = Field(default="", description="新闻来源")
    publish_time: str = Field(default="", description="发布时间")
    category: str = Field(default="", description="新闻分类：政策动态、行业观察、热点新闻、国外动态")
    summary: str = Field(default="", description="一句话摘要，不超过50字")


class GlobalState(BaseModel):
    """全局状态定义"""
    raw_news_list: List[NewsItem] = Field(default=[], description="原始新闻列表")
    filtered_news_list: List[NewsItem] = Field(default=[], description="筛选后的新闻列表")
    final_news_list: List[NewsItem] = Field(default=[], description="最终整理的新闻列表")
    formatted_output: str = Field(default="", description="格式化后的输出文本")


class GraphInput(BaseModel):
    """工作流的输入"""
    pass


class GraphOutput(BaseModel):
    """工作流的输出"""
    formatted_output: str = Field(..., description="格式化后的新闻摘要文本")


# 新闻搜索节点
class NewsSearchInput(BaseModel):
    """新闻搜索节点的输入"""
    pass


class NewsSearchOutput(BaseModel):
    """新闻搜索节点的输出"""
    raw_news_list: List[NewsItem] = Field(..., description="原始新闻列表")


# 新闻筛选与分类节点
class NewsFilterInput(BaseModel):
    """新闻筛选与分类节点的输入"""
    raw_news_list: List[NewsItem] = Field(..., description="原始新闻列表")


class NewsFilterOutput(BaseModel):
    """新闻筛选与分类节点的输出"""
    filtered_news_list: List[NewsItem] = Field(..., description="筛选后的新闻列表")


# 新闻摘要生成节点
class NewsSummaryInput(BaseModel):
    """新闻摘要生成节点的输入"""
    filtered_news_list: List[NewsItem] = Field(..., description="筛选后的新闻列表")


class NewsSummaryOutput(BaseModel):
    """新闻摘要生成节点的输出"""
    final_news_list: List[NewsItem] = Field(..., description="最终整理的新闻列表")


# 格式化输出节点
class FormatOutputInput(BaseModel):
    """格式化输出节点的输入"""
    final_news_list: List[NewsItem] = Field(..., description="最终整理的新闻列表")


class FormatOutputOutput(BaseModel):
    """格式化输出节点的输出"""
    formatted_output: str = Field(..., description="格式化后的输出文本")


# 推送到企业微信节点
class WeChatPushInput(BaseModel):
    """企业微信推送节点的输入"""
    formatted_output: str = Field(..., description="格式化后的新闻摘要文本")


class WeChatPushOutput(BaseModel):
    """企业微信推送节点的输出"""
    success: bool = Field(..., description="推送是否成功")
    message: str = Field(default="", description="推送结果信息")
