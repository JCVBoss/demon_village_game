<!-- [TAG] 所有者:PO|维护责任人:SM|创建时间:2026-04-03|生效标记:✅|最后更新:2026-04-03|版本:v1.0 -->

# 🤖 GitHub Projects 自动化配置指南

> 实现 Issue 和看板的自动同步

---

## 🎯 自动化目标

1. **新 Issue 自动同步到看板** — 创建 Issue 时自动添加到 Project 的 Todo 列
2. **Issue 关闭自动移动到 Done** — Issue 关闭时自动移动到 Done 列
3. **PR 合并自动关闭 Issue** — PR 合并时自动关闭关联的 Issue

---

## 📋 配置步骤

### 方式一：使用 GitHub 内置自动化（推荐）

GitHub Projects 提供了内置的自动化功能，无需编写代码。

#### 步骤 1：访问 Project 设置

1. 打开 Project Board: https://github.com/users/JCVBoss/projects/1
2. 点击右上角的 **⋯** (三个点)
3. 选择 **Settings**

#### 步骤 2：配置自动添加 Issue

**目标：** 新创建的 Issue 自动添加到看板

1. 在 Settings 页面，找到 **Automations** 部分
2. 点击 **Add automation** 按钮
3. 选择触发器：**"When an issue is created"**
4. 配置条件（可选）：
   - 可以设置只添加特定仓库的 Issue
   - 可以设置只添加带有特定标签的 Issue
5. 点击 **Save**

**效果：**
- ✅ 所有新创建的 Issue 自动出现在 Project 中
- ✅ 默认状态为 "Todo"（或你设置的默认列）

---

#### 步骤 3：配置 Issue 关闭时自动移动到 Done

**目标：** Issue 关闭时自动移动到 Done 列

1. 在 Settings 页面，找到 **Automations** 部分
2. 点击 **Add automation** 按钮
3. 选择触发器：**"When an issue is closed"**
4. 配置操作：
   - **Field to update:** Status（或你使用的状态字段）
   - **New value:** Done
5. 点击 **Save**

**效果：**
- ✅ Issue 关闭时自动移动到 Done 列
- ✅ 无需手动拖拽

---

#### 步骤 4：配置 PR 合并时自动关闭 Issue

**目标：** PR 合并时自动关闭关联的 Issue

这个功能在 GitHub Issue/PR 层面配置，不需要在 Project 中设置。

**在 Issue 中关联 PR：**
1. 在 PR 描述中使用关键字：
   ```
   Closes #123
   ```
   或
   ```
   Fixes #123
   ```
2. 当 PR 合并时，Issue 会自动关闭
3. Project 会自动检测到 Issue 关闭，并移动到 Done 列（如果配置了步骤 3）

**效果：**
- ✅ PR 合并 → Issue 自动关闭
- ✅ Issue 关闭 → Project 自动移动到 Done

---

### 方式二：使用 GitHub Actions（高级）

如果需要更复杂的自动化逻辑，可以使用 GitHub Actions。

#### 创建自动化 Workflow

**文件位置：** `.github/workflows/project-automation.yml`

```yaml
name: Project Automation

on:
  issues:
    types: [opened, closed, reopened]
  pull_request:
    types: [closed]

jobs:
  update-project:
    runs-on: ubuntu-latest
    steps:
      - name: Update project when issue opened
        if: github.event_name == 'issues' && github.event.action == 'opened'
        uses: actions/add-to-project@v0.5.0
        with:
          project-url: https://github.com/users/JCVBoss/projects/1
          github-token: ${{ secrets.PROJECT_ACCESS_TOKEN }}

      - name: Update project when issue closed
        if: github.event_name == 'issues' && github.event.action == 'closed'
        uses: actions/github-script@v6
        with:
          github-token: ${{ secrets.PROJECT_ACCESS_TOKEN }}
          script: |
            // 更新 Issue 的状态字段为 Done
            const issue = context.payload.issue;
            // 使用 GraphQL API 更新 Project 字段
            // 具体实现参考 GitHub Actions 文档
```

**注意：** 方式二需要配置 Personal Access Token，适合高级用户。

---

## ✅ 验证配置

### 测试 1：创建新 Issue

1. 创建一个新的 Issue: https://github.com/JCVBoss/demon_village_game/issues/new
2. 填写标题和描述
3. 点击 "Submit new issue"
4. 访问 Project Board: https://github.com/users/JCVBoss/projects/1
5. **预期结果：** Issue 出现在 "Todo" 列

### 测试 2：关闭 Issue

1. 打开任意一个 Issue
2. 点击 "Close issue" 按钮
3. 访问 Project Board
4. **预期结果：** Issue 自动移动到 "Done" 列

### 测试 3：PR 合并自动关闭

1. 创建一个 PR，描述中包含 `Closes #123`
2. 合并 PR
3. **预期结果：**
   - Issue #123 自动关闭
   - Issue 自动移动到 Done 列

---

## 🔧 故障排查

### 问题 1：新 Issue 没有自动添加到看板

**可能原因：**
- 自动化未启用
- 仓库未关联到 Project

**解决方法：**
1. 检查 Project Settings → Automations 是否启用
2. 检查 Project 是否关联了正确的仓库
3. 手动添加一次 Issue 到 Project，然后重试

---

### 问题 2：Issue 关闭后没有移动到 Done

**可能原因：**
- "When issue is closed" 自动化未配置
- Status 字段名称不匹配

**解决方法：**
1. 检查 Project Settings → Automations
2. 确认 "When an issue is closed" 自动化存在且启用
3. 确认 Status 字段名称正确（Done vs Closed）

---

### 问题 3：PR 合并没有关闭 Issue

**可能原因：**
- PR 描述中没有使用正确的关键字
- Issue 编号错误

**解决方法：**
1. 确认 PR 描述中包含 `Closes #123` 或 `Fixes #123`
2. 确认 Issue 编号正确
3. 检查 Issue 和 PR 是否在同一个仓库

---

## 📊 推荐配置

### 魔王城项目推荐配置

| 自动化 | 配置 | 状态 |
|--------|------|------|
| 新 Issue 自动添加 | 启用，所有仓库 | ✅ 推荐 |
| Issue 关闭自动移动 | 启用，移动到 Done | ✅ 推荐 |
| PR 合并自动关闭 | 使用 `Closes #123` | ✅ 推荐 |
| 自动归档完成项 | 可选，30 天后 | ⏳ 可选 |
| 自动分配负责人 | 按标签分配 | ⏳ 可选 |

---

## 🎯 快速配置清单

**5 分钟快速配置：**

- [ ] 访问 Project Settings: https://github.com/users/JCVBoss/projects/1/settings
- [ ] 启用 "When an issue is created" 自动化
- [ ] 启用 "When an issue is closed" 自动化
- [ ] 测试创建新 Issue，确认自动添加
- [ ] 测试关闭 Issue，确认自动移动到 Done

**高级配置（可选）：**

- [ ] 配置按标签自动分配负责人
- [ ] 配置自动归档（30 天后）
- [ ] 配置 GitHub Actions 高级自动化
- [ ] 配置燃尽图和累积流图

---

## 🔗 相关资源

- [GitHub Projects 官方文档](https://docs.github.com/en/issues/planning-and-tracking-with-projects)
- [GitHub Projects 自动化](https://docs.github.com/en/issues/planning-and-tracking-with-projects/automating-your-project)
- [GitHub Actions 参考](https://docs.github.com/en/actions)

---

## 📝 配置记录

| 日期 | 配置内容 | 配置人 |
|------|---------|--------|
| 2026-04-03 | 创建自动化配置指南 | AliceDesigner |

---

*文档创建：2026-04-03*
*GitHub Projects 自动化配置指南*
*盒子管理员：Alice 🤖*
