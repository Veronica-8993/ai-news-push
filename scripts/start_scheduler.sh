#!/bin/bash

# 新闻推送定时任务启动脚本

echo "=========================================="
echo "新闻推送定时任务"
echo "执行时间: 每天早上 08:00"
echo "=========================================="

# 切换到项目根目录
cd "$(dirname "$0")/.."

# 启动定时任务
# 设置 RUN_IMMEDIATELY=true 可以在启动时立即执行一次
export RUN_IMMEDIATELY=false

echo "启动定时任务调度器..."
python3 src/scheduler.py
