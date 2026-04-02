# 🚀 GitHub Project 创建操作指南

> 一步步教你创建魔王城项目管理看板

---

## 📋 准备工作

**访问地址：** https://github.com/JCVBoss/demon_village_game

**需要权限：** 仓库管理员权限（@JCVBoss）

**预计时间：** 15-20 分钟

---

## 步骤 1：创建 Project

### 1.1 进入 Projects 页面

1. 打开 https://github.com/JCVBoss/demon_village_game
2. 点击顶部导航栏的 **"Projects"** 标签
3. 点击 **"New project"** 按钮

![New Project 按钮]

### 1.2 选择模板

1. 在 "Start from scratch" 下选择 **"Board"**
2. 输入项目名称：**魔王城 - Sprint Board**
3. 点击 **"Create project"**

---

## 步骤 2：配置自定义字段

### 2.1 进入字段设置

1. 在项目页面，点击右上角的 **⋮**（三个点菜单）
2. 点击 **"Settings"**
3. 在左侧菜单点击 **"Fields"**

### 2.2 添加 Priority 字段

1. 点击 **"New field"**
2. 字段名：`Priority`
3. 类型：**Single select**
4. 添加选项：
   - 🔴 `P0`（选择红色）
   - 🟠 `P1`（选择橙色）
   - 🟡 `P2`（选择黄色）
   - ⚪ `P3`（选择灰色）
5. 点击 **"Save"**

### 2.3 添加 Story Points 字段

1. 点击 **"New field"**
2. 字段名：`Story Points`
3. 类型：**Number**
4. 点击 **"Save"**

### 2.4 添加 Sprint 字段

1. 点击 **"New field"**
2. 字段名：`Sprint`
3. 类型：**Iteration**
4. 配置迭代：
   - 开始日期：`2026-04-08`
   - 迭代长度：`2 weeks`
   - 添加 5 个迭代（Sprint 0-4）
5. 点击 **"Save"**

### 2.5 添加 Epic 字段

1. 点击 **"New field"**
2. 字段名：`Epic`
3. 类型：**Single select**
4. 添加选项：
   - 🔵 `核心系统`
   - 🟢 `对话系统`
   - 🟣 `美术资源`
   - 🔴 `战斗系统`
   - 🟡 `多结局系统`
5. 点击 **"Save"**

### 2.6 添加 Status 字段

1. 点击 **"New field"**
2. 字段名：`Status`
3. 类型：**Single select**
4. 添加选项：
   - ⚪ `Todo`
   - 🔵 `In Progress`
   - 🟣 `In Review`
   - 🟢 `Done`
5. 点击 **"Save"**

---

## 步骤 3：配置看板视图

### 3.1 设置 Board 分组

1. 返回项目主页
2. 点击 **"Board"** 视图
3. 点击右上角 **"⋮"** → **"Group by"**
4. 选择 **"Status"**

### 3.2 添加过滤器

1. 点击 **"Filter"**
2. 输入过滤条件：`Sprint: Sprint 1`
3. 保存过滤器为 **"Sprint 1 View"**

### 3.3 添加 Table 视图

1. 点击 **"+ Add view"**
2. 选择 **"Table"**
3. 命名为 **"Backlog"**
4. 配置显示字段：
   - Title
   - Priority
   - Story Points
   - Epic
   - Assignee
   - Sprint

---

## 步骤 4：配置自动化

### 4.1 添加内置自动化

1. 点击 **"Workflows"**（左侧菜单）
2. 点击 **"New workflow"**
3. 选择 **"Built-in workflows"**

### 4.2 配置状态自动更新

**自动化 1：新 Issue 自动设为 Todo**
```
Trigger: When an item is added to the project
Action: Set status to Todo
```

**自动化 2：分配负责人时自动设为 In Progress**
```
Trigger: When assignee is set
Action: Set status to In Progress
```

**自动化 3：Issue 关闭时自动设为 Done**
```
Trigger: When issue is closed
Action: Set status to Done
```

### 4.3 配置自动归档

```
Trigger: When status is Done for 7 days
Action: Archive item
```

---

## 步骤 5：创建 Issue 模板

### 5.1 创建功能任务模板

**文件路径：** `.github/ISSUE_TEMPLATE/feature.md`

```markdown
---
name: 功能任务
about: 新功能开发
title: '[FEAT] '
labels: feature
---

## 用户故事
作为 [角色]，我希望 [功能]，以便 [价值]

## 验收标准
- [ ] 标准 1
- [ ] 标准 2
- [ ] 标准 3

## 技术实现
- [ ] 设计文档链接
- [ ] API 定义
- [ ] 测试用例

## 项目字段
- Priority: P0/P1/P2/P3
- Story Points: 1/2/3/5/8/13
- Epic: 核心系统/对话系统/美术/战斗/结局
- Sprint: Sprint 0/1/2/3/4
```

**创建步骤：**
1. 在仓库根目录创建文件夹 `.github`
2. 在其中创建 `ISSUE_TEMPLATE` 文件夹
3. 创建文件 `feature.md`
4. 粘贴以上内容

### 5.2 创建 Bug 模板

**文件路径：** `.github/ISSUE_TEMPLATE/bug.md`

```markdown
---
name: Bug 报告
about: 报告问题
title: '[BUG] '
labels: bug
---

## 问题描述
清晰简洁地描述问题

## 复现步骤
1. 步骤 1
2. 步骤 2
3. 步骤 3

## 期望行为
应该发生什么

## 实际行为
实际发生了什么

## 环境信息
- 系统：
- Godot 版本：
- 分支：

## 项目字段
- Priority: P0/P1/P2/P3
- Severity: Critical/Major/Minor
```

---

## 步骤 6：迁移现有任务

### 6.1 从 backlog.md 迁移

**待迁移任务列表：**

**核心系统 Epic：**
- [ ] CS-002 实现 DialogueManager（P0，8 点）
- [ ] CS-005 LLM API 集成（P1，8 点）

**对话系统 Epic：**
- [ ] DS-002 对话树解析器（P0，5 点）
- [ ] DS-001 对话 UI 实现（P0，5 点）
- [ ] DS-003 陈默对话树实现（P0，3 点）
- [ ] DS-004 夜鸦对话树实现（P0，5 点）
- [ ] DS-005 老约翰对话树实现（P0，5 点）
- [ ] DS-006 小安对话树实现（P0，3 点）

**美术资源 Epic：**
- [ ] AR-011 村庄场景（P0，5 点）
- [ ] AR-012 UI 素材包（P1，5 点）

### 6.2 创建 Issue 方法

**方法 A：手动创建（推荐新手）**

1. 点击仓库 **"Issues"** 标签
2. 点击 **"New issue"**
3. 选择模板（Feature/Bug）
4. 填写标题和描述
5. 在右侧边栏设置：
   - Assignee
   - Labels
   - Projects（选择"魔王城 - Sprint Board"）
   - Milestone
6. 点击 **"Submit new issue"**
7. 在新创建的 Issue 中设置自定义字段（Priority/Story Points/Epic/Sprint）

**方法 B：批量导入（高级）**

使用 GitHub Importer 工具或脚本批量创建。

---

## 步骤 7：邀请协作者

### 7.1 添加团队成员

1. 点击项目页面右上角 **"⋮"**
2. 点击 **"Settings"**
3. 点击 **"Collaborators"**
4. 点击 **"Add people"**
5. 输入协作者 GitHub 用户名：
   - Claude（如果使用 Claude Code）
   - 其他团队成员

### 7.2 设置权限

| 角色 | 权限 | 人员 |
|------|------|------|
| Admin | 完全控制 | JCVBoss |
| Write | 编辑 Issue/Project | Claude/AliceDesigner/AliceBussiness |
| Read | 查看 | 其他利益相关者 |

---

## 步骤 8：团队培训

### 8.1 培训材料

创建培训文档：`docs/project/GitHub_Projects使用教程.md`

**培训内容：**
1. 如何查看项目看板
2. 如何更新任务状态
3. 如何创建新 Issue
4. 如何使用过滤器
5. 如何查看图表

### 8.2 使用规范

**每日流程：**
1. 早上：查看 Board，确认今日任务
2. 工作中：更新任务状态（Todo → In Progress → Review → Done）
3. 晚上：在 Issue 评论中记录进展

**每周流程：**
1. 周一：Sprint Planning（从 Backlog 拖拽任务到 Sprint）
2. 周五：Sprint Review（演示完成的 Issue）

---

## ✅ 检查清单

### 创建完成后检查

- [ ] Project 已创建（Board 视图）
- [ ] 5 个自定义字段已配置（Priority/Story Points/Sprint/Epic/Status）
- [ ] 自动化已启用（状态自动更新）
- [ ] Issue 模板已创建（Feature/Bug）
- [ ] 至少创建了 5 个测试 Issue
- [ ] 协作者已邀请
- [ ] Table 视图已配置（Backlog）
- [ ] Board 视图已分组（按 Status）

### 第一周检查

- [ ] 100% 新任务在 Project 中创建
- [ ] 团队成员每日更新状态
- [ ] Sprint 1 已开始
- [ ] 每日站会使用 Board 视图
- [ ] 无阻塞问题超过 24 小时

---

## 🆘 常见问题

### Q1: 自定义字段不显示？
**A:** 确保在 Project Settings → Fields 中已启用，并且在视图中已配置显示。

### Q2: Issue 没有自动添加到 Project？
**A:** 检查自动化配置，或手动在 Issue 右侧边栏添加 Project。

### Q3: 如何查看燃尽图？
**A:** 点击 "Insights" → "Burndown chart"，选择当前 Sprint。

### Q4: 如何复制项目到其他仓库？
**A:** 在项目设置中使用 "Copy project" 功能。

---

## 📚 参考资源

- [GitHub Projects 官方文档](https://docs.github.com/en/issues/planning-and-tracking-with-projects)
- [项目管理最佳实践](https://docs.github.com/en/issues/planning-and-tracking-with-projects/learning-about-projects/best-practices-for-projects)
- [GitHub Issues 使用指南](https://docs.github.com/en/issues/tracking-your-work-with-issues)

---

*文档创建：2026-04-02 15:45*
*版本：v1.0*
*操作指南*
*盒子管理员：Alice 🤖*
