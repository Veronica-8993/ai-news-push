## 项目概述
- **名称**: 新闻推送工作流
- **功能**: 每天早上8点自动抓取AI人工智能及科技热点新闻，推送到企业微信群聊

### 节点清单
| 节点名 | 文件位置 | 类型 | 功能描述 | 分支逻辑 | 配置文件 |
|-------|---------|------|---------|---------|---------|
| news_search | `nodes/news_search_node.py` | task | 搜索巴德富产业链和热点新闻 | - | - |
| news_filter | `nodes/news_filter_node.py` | agent | 筛选重要新闻并进行四分类 | - | `config/news_filter_llm_cfg.json` |
| news_summary | `nodes/news_summary_node.py` | agent | 为每条新闻生成详细摘要 | - | `config/news_summary_llm_cfg.json` |
| format_output | `nodes/format_output_node.py` | task | 格式化新闻列表为精简格式（适合企业微信单条消息） | - | - |
| wechat_push | `nodes/wechat_push_node.py` | task | 推送到企业微信群聊（单条消息） | - | - |

**类型说明**: task(任务节点) / agent(大模型节点) / condition(条件分支) / looparray(列表循环) / loopcond(条件循环)

## 子图清单
无子图

## 技能使用
- 节点`news_search`使用web-search技能
- 节点`news_filter`使用大语言模型
- 节点`news_summary`使用大语言模型
- 节点`wechat_push`使用wechat-bot技能

## 定时任务

### 方式一：GitHub Actions（推荐）
- **执行时间**: 每天 UTC 0:00（北京时间 8:00）
- **配置文件**: `.github/workflows/daily_push.yml`
- **推送脚本**: `scripts/run_push_github.py`
- **配置说明**: 见 `GITHUB_ACTIONS_README.md`
- **优势**: 免费、稳定、无需服务器

### 方式二：Crontab（备用）
- **执行时间**: 每天早上 08:00（北京时间）
- **脚本位置**: `scripts/run_push.sh`
- **日志位置**: `/workspace/projects/logs/cron_push.log`
- **配置命令**: `crontab -l` 查看配置

### 手动测试
```bash
# 本地测试
bash scripts/run_push.sh

# GitHub Actions 脚本测试
export WECHAT_WEBHOOK_KEY="your-key"
python scripts/run_push_github.py
```

### 查看日志
```bash
tail -f logs/cron_push.log
```

## 新闻优先级
**AI人工智能相关新闻优先级最高**，包括：
- 大模型动态：ChatGPT、GPT、Claude、文心一言、通义千问等
- AI企业动态：OpenAI、Google、百度、阿里、腾讯、字节跳动、华为等
- AI技术应用：AI+医疗、AI+金融、AI+教育、自动驾驶、智能机器人
- AI基础设施：AI芯片、算力、云计算、数据中心
- AI投融资：创业公司、融资事件、IPO

## 输出格式示例
```
📅 每日新闻精选 | YYYY年MM月DD日

【政策动态】
1、[简洁摘要40-60字]
...

【行业观察】
1、[简洁摘要40-60字]
...

【热点新闻】
1、[简洁摘要40-60字]
...

【国外动态】
1、[简洁摘要40-60字]
...
```

**格式说明**：
- 去掉发布时间、来源标注和原文链接
- 每条摘要40-60字，包含主体、事件、关键信息
- 消息总大小控制在4096字节以内（企业微信Markdown限制）
- 超过限制时自动精简（每个分类最多5条）
- 实测：15条新闻约2318字节，空间充裕
