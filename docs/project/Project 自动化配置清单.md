<!-- [TAG] 所有者:PO|维护责任人:SM|创建时间:2026-04-03|生效标记:✅|最后更新:2026-04-03|版本:v1.1 -->

# ⚙️ Project 自动化配置清单

> 已完成和待配置的自动化项目

---

## ✅ 已完成的自动化

### 1. Issue 关闭 → 自动移动到 Done

**状态：** ✅ 已启用

**测试验证：**
- Issue #25 关闭后 → 出现在 Done 列 ✅
- Issue #28 关闭后 → 出现在 Done 列 ✅

**配置位置：** Project Settings → Automations → "When an issue is closed"

---

## ⏳ 待配置的自动化

### 1. 新 Issue 创建 → 自动添加到 Project

**状态：** ❌ 未启用

**问题：** 新创建的 Issue 不会自动出现在 Project 中，需要手动添加

**配置步骤：**

#### 方法 1：使用 GitHub 内置自动化（推荐）

1. 访问 Project Settings: https://github.com/users/JCVBoss/projects/1/settings

2. 找到 **Automations** 部分

3. 点击 **"Add automation"** 按钮

4. 选择触发器：**"When an issue is created"**

5. 配置（可选）：
   - **Repository filter:** `JCVBoss/demon_village_game`
   - 或者留空，对所有仓库生效

6. 点击 **Save**

**效果：**
- ✅ 所有新创建的 Issue 自动添加到 Project
- ✅ 默认状态为第一个列（通常是 Todo）

---

#### 方法 2：使用 GitHub Actions（高级）

如果内置自动化不可用，可以使用 GitHub Actions。

**文件：** `.github/workflows/project-auto-add.yml`

```yaml
name: Auto Add Issues to Project

on:
  issues:
    types: [opened]

jobs:
  add-to-project:
    name: Add issue to project
    runs-on: ubuntu-latest
    steps:
      - uses: actions/add-to-project@v0.5.0
        with:
          project-url: https://github.com/users/JCVBoss/projects/1
          github-token: ${{ secrets.PROJECT_ACCESS_TOKEN }}
```

**需要配置：**
1. 创建 Personal Access Token (PAT)
2. 在仓库 Settings → Secrets 中添加 `PROJECT_ACCESS_TOKEN`

---

## 🧪 测试验证

### 测试步骤

配置完成后，运行以下测试：

```bash
# 1. 创建测试 Issue
gh issue create --title "🧪 测试自动添加" --body "验证自动化" --repo JCVBoss/demon_village_game

# 2. 等待 5 秒
sleep 5

# 3. 检查是否在 Project 中
gh project item-list 1 --owner JCVBoss --limit 30 | grep "测试自动添加"

# 预期：能看到新 Issue
```

---

## 📊 当前自动化状态

| 自动化 | 状态 | 测试 Issue | 结果 |
|--------|------|-----------|------|
| 新 Issue 自动添加 | ❌ 待配置 | #27, #28 | 需要手动添加 |
| Issue 关闭自动 Done | ✅ 已启用 | #25, #28 | 自动移动到 Done |
| PR 合并自动关闭 | ⏳ 待测试 | - | 使用 `Closes #123` |

---

## 🔧 快速配置链接

| 用途 | 链接 |
|------|------|
| Project Board | https://github.com/users/JCVBoss/projects/1 |
| Project Settings | https://github.com/users/JCVBoss/projects/1/settings |
| 添加自动化 | 点击 Settings → Add automation |

---

## 📝 配置记录

| 日期 | 操作 | 操作人 |
|------|------|--------|
| 2026-04-03 | 测试关闭自动化 | AliceDesigner |
| 2026-04-03 | 确认关闭自动化生效 | AliceDesigner |
| 2026-04-03 | 创建配置清单 | AliceDesigner |

---

*文档创建：2026-04-03*
*Project 自动化配置清单*
*盒子管理员：Alice 🤖*
