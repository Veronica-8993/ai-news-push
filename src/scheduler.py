"""
新闻推送定时任务
每天早上8点自动执行新闻推送工作流
"""
import os
import sys
import json
import logging
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

# 添加项目根目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from graphs.graph import main_graph

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('/app/work/logs/news_scheduler.log')
    ]
)
logger = logging.getLogger(__name__)


def run_news_workflow():
    """
    执行新闻推送工作流
    """
    try:
        logger.info("=" * 60)
        logger.info(f"开始执行新闻推送任务 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info("=" * 60)
        
        # 执行工作流
        result = main_graph.invoke({})
        
        # 记录结果
        if result and result.get("formatted_output"):
            output_length = len(result["formatted_output"])
            logger.info(f"工作流执行成功，输出长度: {output_length} 字符")
            logger.info(f"推送结果: {result.get('wechat_push', {}).get('message', '未知')}")
        else:
            logger.warning("工作流执行完成，但无输出内容")
        
        logger.info("=" * 60)
        logger.info(f"新闻推送任务完成 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info("=" * 60)
        
        return result
        
    except Exception as e:
        logger.error(f"新闻推送任务执行失败: {str(e)}", exc_info=True)
        raise


def main():
    """
    启动定时任务调度器
    """
    logger.info("=" * 60)
    logger.info("新闻推送定时任务启动")
    logger.info("执行时间: 每天早上 08:00")
    logger.info("=" * 60)
    
    # 创建调度器
    scheduler = BlockingScheduler()
    
    # 添加定时任务：每天早上8点执行
    scheduler.add_job(
        run_news_workflow,
        CronTrigger(hour=8, minute=0),
        id='news_push_job',
        name='新闻推送任务',
        misfire_grace_time=3600  # 如果任务错过执行时间，1小时内仍然执行
    )
    
    # 可选：启动时立即执行一次（测试用）
    if os.getenv("RUN_IMMEDIATELY", "false").lower() == "true":
        logger.info("启动时立即执行一次任务...")
        run_news_workflow()
    
    try:
        logger.info("定时任务调度器已启动，等待执行...")
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logger.info("定时任务调度器已停止")
        scheduler.shutdown()


if __name__ == "__main__":
    main()
