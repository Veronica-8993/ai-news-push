"""
企业微信推送节点 - 将格式化后的新闻推送到企业微信群聊
"""
import json
import re
import logging
import requests
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from coze_workload_identity import Client
from graphs.state import WeChatPushInput, WeChatPushOutput

# 配置日志
logger = logging.getLogger(__name__)


def wechat_push_node(
    state: WeChatPushInput,
    config: RunnableConfig,
    runtime: Runtime[Context]
) -> WeChatPushOutput:
    """
    title: 企业微信推送
    desc: 将格式化后的新闻摘要推送到企业微信群聊（单条消息）
    integrations: wechat-bot
    """
    ctx = runtime.context
    
    try:
        # 获取企业微信机器人凭证
        client = Client()
        wechat_bot_credential = client.get_integration_credential("integration-wechat-bot")
        webhook_key_dict = json.loads(wechat_bot_credential)
        webhook_key = webhook_key_dict["webhook_key"]
        
        # 如果webhook_key是完整URL，提取key参数
        if "https" in webhook_key:
            match = re.search(r"key=([a-zA-Z0-9-]+)", webhook_key)
            if match:
                webhook_key = match.group(1)
        
        # 构建webhook URL
        webhook_url = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={webhook_key}"
        
        # 构建Markdown消息
        markdown_content = state.formatted_output
        
        # 检查消息长度
        msg_size = len(markdown_content.encode('utf-8'))
        logger.info(f"消息大小: {msg_size} 字节")
        
        if msg_size > 4000:
            logger.warning(f"消息超过4000字节限制（{msg_size}字节），需要精简")
            # 返回错误，让格式化节点重新生成
            return WeChatPushOutput(
                success=False,
                message=f"消息超过限制（{msg_size}字节），需要精简内容"
            )
        
        # 准备请求payload
        payload = {
            "msgtype": "markdown",
            "markdown": {
                "content": markdown_content
            }
        }
        
        # 发送请求
        headers = {"Content-Type": "application/json"}
        response = requests.post(webhook_url, json=payload, headers=headers, timeout=15)
        response.raise_for_status()
        result = response.json()
        
        if result.get("errcode", 0) == 0:
            logger.info(f"新闻推送成功，消息大小: {msg_size} 字节")
            return WeChatPushOutput(
                success=True,
                message=f"新闻推送成功，消息大小: {msg_size} 字节"
            )
        else:
            logger.error(f"企业微信推送失败: {result}")
            return WeChatPushOutput(
                success=False,
                message=f"推送失败: {result.get('errmsg', '未知错误')}"
            )
            
    except Exception as e:
        logger.error(f"企业微信推送异常: {str(e)}")
        return WeChatPushOutput(
            success=False,
            message=f"推送异常: {str(e)}"
        )
