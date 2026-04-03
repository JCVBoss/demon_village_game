<!-- [TAG] 所有者:PO|维护责任人:SM|创建时间:2026-04-02|生效标记:✅|最后更新:2026-04-02|版本:v1.0 -->
# 🔐 GitHub CLI 认证指南

> 完成认证后，Alice 就可以帮你管理 Project 了！

---

## 📋 认证步骤

### 方式 1：网页认证（推荐 ✅）

**最简单，只需 1 分钟**

**步骤：**

1. **运行认证命令**
   ```bash
   gh auth login
   ```

2. **选择认证方式**
   ```
   ? What account do you want to log into?
   ❯ GitHub.com
     GitHub Enterprise Server
   
   ? What is your preferred protocol for Git operations?
   ❯ HTTPS
     SSH
   
   ? Authenticate Git with your GitHub credentials?
   ❯ Yes
     No
   
   ? How would you like to authenticate GitHub CLI?
   ❯ Login with a web browser
     Paste an authentication token
   ```

3. **按回车选择默认选项**

4. **浏览器会自动打开授权页面**
   - 如果没有自动打开，复制终端显示的代码
   - 访问 https://github.com/login/device
   - 输入代码

5. **在 GitHub 页面确认授权**
   - 点击 "Authorize github"
   - 回到终端，按回车

6. **认证完成！**
   ```
   ✓ Authentication complete.
   - gh config set -h github.com git_protocol https
   ✓ Configured git protocol
   ✓ Logged in as JCVBoss
   ```

---

### 方式 2：Token 认证（备用）

**如果网页认证失败，使用此方法**

**步骤：**

1. **创建 Personal Access Token**
   - 访问 https://github.com/settings/tokens/new
   - 勾选以下权限：
     - ✅ `repo` (Full control of private repositories)
     - ✅ `project` (Read and write access to projects)
     - ✅ `workflow` (Update GitHub Action workflows)
   - 点击 "Generate token"
   - **复制 Token（只显示一次！）**

2. **使用 Token 认证**
   ```bash
   gh auth login --with-token
   ```
   
3. **粘贴 Token**
   - 粘贴你刚才复制的 Token
   - 按回车

4. **认证完成**

---

## ✅ 验证认证

**检查登录状态：**
```bash
gh auth status
```

**成功输出：**
```
github.com
  ✓ Logged in to github.com as JCVBoss (~/.config/gh/hosts.yml)
  ✓ Git operations for github.com configured to use https:// protocol.
  ✓ Token: ghp_************************************
```

---

## 🎯 认证后可以做的事

### Project 管理
```bash
# 列出所有项目
gh project list --owner JCVBoss

# 创建项目
gh project create --title "魔王城 - Sprint Board" --owner JCVBoss

# 查看项目
gh project view 1 --owner JCVBoss

# 添加字段
gh project field-create --id 1 --owner JCVBoss --name "Priority" --type SINGLE_SELECT --options "P0,P1,P2,P3"
```

### Issue 管理
```bash
# 创建 Issue
gh issue create --title "DS-002 对话树解析器" --body "实现对话树 JSON 解析器" --label "feature" --assignee "Claude"

# 列出 Issue
gh issue list --limit 10

# 查看 Issue
gh issue view 123

# 编辑 Issue（添加项目字段）
gh issue edit 123 --add-project "魔王城 - Sprint Board" --set-field "Priority=P0"
```

### 批量操作
```bash
# 从 backlog.md 批量创建 Issue
# 脚本示例
while IFS= read -r line; do
  title=$(echo $line | cut -d'|' -f2 | xargs)
  priority=$(echo $line | cut -d'|' -f3 | xargs)
  points=$(echo $line | cut -d'|' -f4 | xargs)
  
  gh issue create \
    --title "$title" \
    --body "从 backlog.md 迁移" \
    --label "feature" \
    --project "魔王城 - Sprint Board"
done < backlog_tasks.txt
```

---

## 🔒 安全提示

### Token 存储
- Token 存储在 `~/.config/gh/hosts.yml`
- 权限设置为 `600`（只有你可读）
- 不要分享这个文件

### Token 过期
- Personal Access Token 默认永不过期
- 建议每 90 天更新一次
- 可以在 https://github.com/settings/tokens 查看和管理

### 权限最小化
- 只授予必要的权限
- 对于只读操作，使用 `read:project` 即可
- 对于管理操作，需要 `repo` 和 `project` 权限

---

## 🆘 故障排除

### Q1: gh auth login 卡住？
**A:** 使用 `--web` 强制网页认证
```bash
gh auth login --web
```

### Q2: Token 无效？
**A:** 重新生成 Token
1. 访问 https://github.com/settings/tokens
2. 删除旧 Token
3. 创建新 Token
4. 重新认证

### Q3: 权限不足？
**A:** 检查 Token 权限
```bash
gh auth refresh --scopes repo,project,workflow
```

### Q4: 多个 GitHub 账号？
**A:** 使用 switch 命令
```bash
gh auth switch
```

---

## 📚 下一步

**认证完成后，我可以帮你：**

1. ✅ 创建 GitHub Project
2. ✅ 配置自定义字段
3. ✅ 从 backlog.md 批量创建 Issue
4. ✅ 设置自动化工作流
5. ✅ 每日同步进度

**请运行以下命令开始认证：**
```bash
gh auth login
```

**认证完成后告诉我，我会立即开始创建 Project！** 🚀

---

*文档创建：2026-04-02 15:55*
*版本：v1.0*
*认证指南*
*盒子管理员：Alice 🤖*
