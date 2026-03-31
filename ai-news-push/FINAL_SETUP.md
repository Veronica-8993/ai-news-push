# 最终配置步骤

## ✅ 已完成的配置

所有代码和配置文件已准备就绪，包括：

| 文件 | 状态 | 说明 |
|------|------|------|
| `.github/workflows/daily_push.yml` | ✅ | GitHub Actions 工作流 |
| `scripts/run_push_github.py` | ✅ | 推送脚本 |
| `requirements.txt` | ✅ | Python 依赖 |
| `src/graphs/*` | ✅ | 工作流代码 |
| `config/*` | ✅ | 模型配置 |

---

## 🔧 您需要做的 3 步操作

### 步骤 1：创建 GitHub 仓库

1. 登录 [GitHub](https://github.com)
2. 点击右上角 **+** → **New repository**
3. 填写：
   - Repository name: `ai-news-push`（或其他名称）
   - 选择 **Public**（公开仓库可免费使用 Actions）
4. 点击 **Create repository**

### 步骤 2：推送代码

在您的电脑终端执行：

```bash
# 如果项目在当前沙箱，先下载项目
# 然后在本地执行：

# 初始化 Git（如果还没有）
git init

# 添加所有文件
git add .

# 提交
git commit -m "初始化 AI 新闻推送项目"

# 添加远程仓库（替换 YOUR_USERNAME 为您的 GitHub 用户名）
git remote add origin https://github.com/YOUR_USERNAME/ai-news-push.git

# 推送
git branch -M main
git push -u origin main
```

### 步骤 3：配置 Secret

1. 打开 GitHub 仓库页面
2. 点击 **Settings** → **Secrets and variables** → **Actions**
3. 点击 **New repository secret**
4. 填写：
   - **Name**: `WECHAT_WEBHOOK_KEY`
   - **Secret**: `34f209bf-c5c2-4790-9f7e-4e4b683ee24e`
5. 点击 **Add secret**

---

## ✅ 完成！

配置完成后：

- **每天北京时间 8:00** 自动推送 AI 新闻
- 可在 **Actions** 页面查看执行日志
- 可手动点击 **Run workflow** 测试

---

## 📋 常用操作

### 手动测试
Actions 页面 → 选择工作流 → Run workflow

### 查看日志
Actions 页面 → 点击具体执行记录 → 展开 push-news

### 修改推送时间
编辑 `.github/workflows/daily_push.yml`：
```yaml
schedule:
  - cron: '0 0 * * *'  # UTC 时间，北京时间 = UTC + 8
```

### 暂停推送
Actions 页面 → 选择工作流 → Disable workflow

---

## ❓ 问题排查

**Q: Actions 没有执行？**
- 检查仓库是否为 Public
- 检查 Actions 是否已启用
- 查看 Actions 页面是否有错误日志

**Q: 推送失败？**
- 检查 Secret 是否正确配置
- 查看 Actions 日志了解具体错误

---

## 📞 需要帮助？

- 查看 `GITHUB_ACTIONS_README.md` 了解更多细节
- 查看 `SETUP_GUIDE.md` 快速指南
