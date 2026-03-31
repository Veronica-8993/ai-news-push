# 新闻推送定时任务使用说明

## 功能说明

每天早上8点自动执行新闻推送工作流，抓取巴德富产业链和社会热点新闻，并推送到企业微信群。

## 使用方式

### 方式一：启动定时任务服务（推荐）

```bash
# 启动定时任务调度器
bash scripts/start_scheduler.sh
```

调度器将在后台运行，每天早上8点自动执行新闻推送任务。

### 方式二：立即执行一次（测试用）

```bash
# 立即执行一次新闻推送
bash scripts/test_scheduler.sh
```

### 方式三：使用Python直接运行

```bash
# 启动定时任务调度器
python3 src/scheduler.py

# 立即执行一次（测试用）
RUN_IMMEDIATELY=true python3 src/scheduler.py
```

## 定时任务配置

定时任务使用APScheduler实现，配置如下：

- **执行时间**：每天早上 08:00
- **时区**：系统默认时区
- **错过执行处理**：如果任务错过执行时间，1小时内仍然执行

## 日志查看

日志文件位置：`/app/work/logs/news_scheduler.log`

```bash
# 查看最新日志
tail -f /app/work/logs/news_scheduler.log

# 查看最近100行日志
tail -n 100 /app/work/logs/news_scheduler.log
```

## 修改执行时间

编辑 `src/scheduler.py` 文件，修改以下代码：

```python
# 修改执行时间
scheduler.add_job(
    run_news_workflow,
    CronTrigger(hour=8, minute=0),  # 修改这里：hour=小时, minute=分钟
    id='news_push_job',
    name='新闻推送任务',
    misfire_grace_time=3600
)
```

例如，改为每天早上7点30分执行：

```python
CronTrigger(hour=7, minute=30)
```

## 后台运行

### 使用 nohup 后台运行

```bash
nohup bash scripts/start_scheduler.sh > /dev/null 2>&1 &
```

### 使用 systemd（推荐）

创建服务文件 `/etc/systemd/system/news-scheduler.service`：

```ini
[Unit]
Description=News Push Scheduler
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/path/to/your/project
ExecStart=/usr/bin/python3 /path/to/your/project/src/scheduler.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

启动服务：

```bash
sudo systemctl daemon-reload
sudo systemctl start news-scheduler
sudo systemctl enable news-scheduler  # 开机自启
```

## 企业微信配置

企业微信webhook地址已配置在环境变量中，如需修改，请更新企业微信机器人配置。

## 故障排查

### 1. 任务未执行

- 检查日志文件是否有错误信息
- 确认系统时间是否正确
- 确认调度器进程是否在运行

### 2. 推送失败

- 检查企业微信webhook地址是否正确
- 检查网络连接是否正常
- 查看日志中的错误详情

### 3. 工作流执行失败

- 检查新闻搜索API是否正常
- 检查LLM模型配置是否正确
- 查看详细错误日志

## 停止定时任务

### 方式一：Ctrl+C

如果在前台运行，按 `Ctrl+C` 停止。

### 方式二：杀死进程

```bash
# 查找进程
ps aux | grep scheduler.py

# 杀死进程
kill -9 <PID>
```

### 方式三：停止systemd服务

```bash
sudo systemctl stop news-scheduler
```
