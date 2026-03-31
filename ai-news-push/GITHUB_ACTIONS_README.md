# GitHub Actions 自动推送配置说明

## 功能说明

使用 GitHub Actions 实现每天早上 8:00（北京时间）自动推送 AI 新闻到企业微信群。

## 优势

- ✅ **完全免费**：GitHub Actions 公开仓库无限制使用
- ✅ **稳定可靠**：GitHub 服务不会中断
- ✅ **无需服务器**：不需要维护自己的服务器
- ✅ **日志可查**：每次执行都有详细日志
- ✅ **支持手动触发**：可在 GitHub 页面手动执行

## 配置步骤

### 1. 上传代码到 GitHub

如果还没有上传，先将项目推送到 GitHub：

```bash
git init
git add .
git commit -m "Initial commit: AI news push workflow"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

### 2. 配置 Secrets

1. 打开 GitHub 仓库页面
2. 点击 **Settings** → **Secrets and variables** → **Actions**
3. 点击 **New repository secret**
4. 添加以下 Secret：

| Name | Value |
|------|-------|
| `WECHAT_WEBHOOK_KEY` | `34f209bf-c5c2-4790-9f7e-4e4b683ee24e` |

### 3. 启用 GitHub Actions

1. 打开仓库的 **Actions** 标签页
2. 如果看到提示，点击 **I understand my workflows, go ahead and enable them**
3. 找到 **每日AI新闻推送** 工作流
4. 确保工作流已启用

### 4. 手动测试（可选）

1. 进入 **Actions** 页面
2. 选择 **每日AI新闻推送** 工作流
3. 点击 **Run workflow** → **Run workflow**
4. 等待执行完成，查看日志

## 执行时间

- **定时执行**：每天 UTC 0:00（北京时间 8:00）
- **手动执行**：可在 Actions 页面随时手动触发

## 查看执行日志

1. 进入 **Actions** 页面
2. 点击具体的执行记录
3. 展开 **push-news** job 查看详细日志
4. 可下载 **push-log** artifact 查看完整日志

## 修改执行时间

编辑 `.github/workflows/daily_push.yml` 文件中的 cron 表达式：

```yaml
schedule:
  - cron: '0 0 * * *'  # UTC 时间
```

常用时间配置：

| 北京时间 | UTC cron |
|---------|----------|
| 8:00 | `0 0 * * *` |
| 7:00 | `0 23 * * *` |
| 9:00 | `0 1 * * *` |
| 18:00 | `0 10 * * *` |

## 常见问题

### Q: 为什么没有执行？

检查以下项目：
1. GitHub Actions 是否已启用
2. Secrets 是否正确配置
3. 查看 Actions 页面是否有错误日志

### Q: 如何修改推送内容？

修改以下文件：
- `src/graphs/nodes/news_search_node.py` - 搜索关键词
- `config/news_filter_llm_cfg.json` - 筛选规则
- `config/news_summary_llm_cfg.json` - 摘要规则

### Q: 如何停止自动推送？

1. 进入 **Actions** 页面
2. 选择 **每日AI新闻推送** 工作流
3. 点击 **Disable workflow**

或者删除 `.github/workflows/daily_push.yml` 文件。

## 项目结构

```
.github/
└── workflows/
    └── daily_push.yml     # GitHub Actions 工作流配置

scripts/
├── run_push.sh            # 本地/crontab 推送脚本
└── run_push_github.py     # GitHub Actions 推送脚本
```
