#!/usr/bin/env python3
"""
GitHub Actions 每日新闻推送脚本
从环境变量获取企业微信 Webhook Key
"""
import os
import sys
import json
import requests
from datetime import datetime

# 设置路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# 切换工作目录
os.chdir(os.path.join(os.path.dirname(__file__), '..'))

from graphs.graph import main_graph


def main():
    print("=" * 60)
    print(f"开始执行每日新闻推送 - {datetime.now()}")
    print("=" * 60)

    # 获取企业微信 Webhook Key
    webhook_key = os.getenv('WECHAT_WEBHOOK_KEY')
    if not webhook_key:
        print("❌ 错误: 未配置 WECHAT_WEBHOOK_KEY 环境变量")
        sys.exit(1)

    webhook_url = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={webhook_key}"

    try:
        # 执行工作流
        print("正在搜索过去24小时内的AI新闻...")
        result = main_graph.invoke({})

        if result and result.get('formatted_output'):
            formatted_output = result['formatted_output']

            print("\n" + "=" * 60)
            print("📰 新闻内容：")
            print("=" * 60)
            print(formatted_output)
            print("=" * 60)

            # 推送到企业微信
            msg_size = len(formatted_output.encode('utf-8'))
            print(f"\n消息大小: {msg_size} 字节")

            payload = {
                'msgtype': 'markdown',
                'markdown': {
                    'content': formatted_output
                }
            }

            response = requests.post(webhook_url, json=payload, timeout=30)
            result_wx = response.json()

            if result_wx.get('errcode', 0) == 0:
                print("✅ 推送成功！")
                return 0
            else:
                print(f"❌ 推送失败: {result_wx}")
                return 1
        else:
            print("❌ 工作流执行失败，无输出内容")
            return 1

    except Exception as e:
        print(f"❌ 执行异常: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

    finally:
        print("=" * 60)
        print(f"推送任务完成 - {datetime.now()}")
        print("=" * 60)


if __name__ == '__main__':
    sys.exit(main())
