"""
企业微信推送节点
"""
import os
import logging
import requests
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from graphs.state import WeChatPushInput, WeChatPushOutput

logger = logging.getLogger(__name__)


def wechat_push_node(
    state: WeChatPushInput,
    config: RunnableConfig,
    runtime: Runtime[Context]
) -> WeChatPushOutput:
    """
    title: 企业微信推送
    desc: 推送新闻到企业微信
    integrations: 无
    """
    
    webhook_key = os.getenv("WECHAT_WEBHOOK_KEY", "")
    
    if not webhook_key:
        logger.error("未配置 WECHAT_WEBHOOK_KEY")
        return WeChatPushOutput(success=False, message="未配置 WECHAT_WEBHOOK_KEY")
    
    webhook_url = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={webhook_key}"
    
    try:
        payload = {
            "msgtype": "markdown",
            "markdown": {"content": state.formatted_output}
        }
        
        resp = requests.post(webhook_url, json=payload, timeout=15)
        result = resp.json()
        
        if result.get("errcode", 0) == 0:
            logger.info("推送成功")
            return WeChatPushOutput(success=True, message="推送成功")
        else:
            logger.error(f"推送失败: {result}")
            return WeChatPushOutput(success=False, message=str(result))
            
    except Exception as e:
        logger.error(f"推送异常: {e}")
        return WeChatPushOutput(success=False, message=str(e))
