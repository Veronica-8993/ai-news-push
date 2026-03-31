#!/bin/bash
# 每日新闻推送脚本 - 由 crontab 调用
# 执行时间：每天早上 08:00（北京时间）

# 切换到工作目录（实际路径）
cd /workspace/projects

# 记录开始时间
echo "========================================" >> /workspace/projects/logs/cron_push.log
echo "开始执行: $(date '+%Y-%m-%d %H:%M:%S')" >> /workspace/projects/logs/cron_push.log

# 执行推送
/usr/bin/python3 -c "
import sys
import os

# 设置路径
sys.path.insert(0, '/workspace/projects/src')
sys.path.insert(0, '/workspace/projects')
os.chdir('/workspace/projects')

from graphs.graph import main_graph
import requests

try:
    # 执行工作流
    result = main_graph.invoke({})
    
    if result and result.get('formatted_output'):
        formatted_output = result['formatted_output']
        
        # 推送到企业微信
        webhook_url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=34f209bf-c5c2-4790-9f7e-4e4b683ee24e'
        
        payload = {
            'msgtype': 'markdown',
            'markdown': {
                'content': formatted_output
            }
        }
        
        response = requests.post(webhook_url, json=payload, timeout=30)
        result_wx = response.json()
        
        if result_wx.get('errcode', 0) == 0:
            print('推送成功')
        else:
            print(f'推送失败: {result_wx}')
    else:
        print('无输出内容')
        
except Exception as e:
    print(f'执行异常: {e}')
    import traceback
    traceback.print_exc()
" >> /workspace/projects/logs/cron_push.log 2>&1

# 记录结束时间
echo "执行完成: $(date '+%Y-%m-%d %H:%M:%S')" >> /workspace/projects/logs/cron_push.log
