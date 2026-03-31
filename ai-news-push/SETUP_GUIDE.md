# 快速配置指南

## 📋 配置步骤（3步完成）

### 步骤 1：推送代码到 GitHub

```bash
# 初始化仓库（如果还没有）
git init

# 添加所有文件
git add .

# 提交
git commit -m "配置 GitHub Actions 自动推送"

# 添加远程仓库（替换为你的仓库地址）
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git

# 推送
git push -u origin main
```

### 步骤 2：配置 Secret

1. 打开 GitHub 仓库 → **Settings** → **Secrets and variables** → **Actions**
2. 点击 **New repository secret**
3. 填写：
   - **Name**: `WECHAT_WEBHOOK_KEY`
   - **Value**: `34f209bf-c5c2-4790-9f7e-4e4b683ee24e`
4. 点击 **Add secret**

### 步骤 3：启用并测试

1. 进入 **Actions** 标签页
2. 启用工作流
3. 点击 **Run workflow** 手动测试

---

## ✅ 完成！

现在每天早上 8:00（北京时间）会自动推送 AI 新闻到企业微信群！

---

## 📁 相关文件

| 文件 | 说明 |
|------|------|
| `.github/workflows/daily_push.yml` | GitHub Actions 配置 |
| `scripts/run_push_github.py` | 推送脚本 |
| `GITHUB_ACTIONS_README.md` | 详细配置说明 |
