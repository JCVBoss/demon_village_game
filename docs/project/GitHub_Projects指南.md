<!-- [TAG] 所有者:PO|维护责任人:SM|创建时间:2026-04-02|生效标记:✅|最后更新:2026-04-02|版本:v1.0 -->
# 🎯 GitHub Projects 实施指南

> 利用 GitHub 官方项目管理工具实现高效协作

---

## 📊 GitHub Projects 核心功能

### 1. 三种视图布局

| 视图 | 用途 | 适用场景 |
|------|------|----------|
| **Table（表格）** | 详细列表视图 | Product Backlog、任务清单 |
| **Board（看板）** | Kanban 板式 | Sprint 追踪、每日站会 |
| **Roadmap（路线图）** | 时间线视图 | 里程碑规划、发布计划 |

---

### 2. 自定义字段（Custom Fields）

**内置字段：**
- Assignee（负责人）
- Labels（标签）
- Milestone（里程碑）
- Repository（仓库）

**自定义字段（最多 50 个）：**
- **Text** - 文本说明
- **Number** - 故事点估算
- **Date** - 目标日期
- **Single Select** - 优先级（P0/P1/P2）
- **Iteration** - Sprint 周期

---

### 3. 自动化（Automations）

**内置自动化：**
- 当 Issue 状态变更时自动更新字段
- 当 PR 合并时自动标记任务完成
- 自动归档已完成任务
- 自动添加符合规则的 Issue

**高级自动化：**
- GitHub Actions 触发
- GraphQL API 管理

---

### 4. 图表和洞察（Insights）

**可用图表：**
- 燃尽图（Burndown Chart）
- 累积流图（Cumulative Flow）
- 任务分布图
- 完成率统计

---

## 🚀 魔王城项目实施方案

### 方案 A：轻量级（推荐起步）

**适用：** 3-4 人小团队，异步协作

**配置：**
```
Project 名称：魔王城下的最后村庄
仓库关联：JCVBoss/demon_village_game
视图：Board（Kanban）+ Table（Backlog）
```

**字段设置：**
| 字段名 | 类型 | 选项 |
|--------|------|------|
| Priority | Single Select | P0/P1/P2/P3 |
| Story Points | Number | 1/2/3/5/8/13 |
| Sprint | Iteration | Sprint 0/1/2/3... |
| Epic | Single Select | 核心系统/对话系统/美术/战斗/结局 |
| Status | Single Select | Todo/InProgress/Review/Done |

**自动化配置：**
- 当 Issue 关闭时 → Status 自动设为 Done
- 当 PR 合并时 → 关联 Issue 自动关闭
- 新 Issue 添加标签 P0 → 自动分配给 Claude

---

### 方案 B：专业级（推荐扩展）

**适用：** 团队扩大，多仓库协作

**配置：**
```
Organization: JCVBoss-Game-Studio
Projects: 
  - 魔王城 - Product Backlog
  - 魔王城 - Sprint Board
  - 魔王城 - Roadmap
Repositories:
  - demon_village_game（主项目）
  - demon_village_assets（美术资源）
  - demon_village_docs（设计文档）
```

**多视图配置：**
1. **Backlog View**（Table）
   - 过滤：Milestone = "v1.0"
   - 排序：Priority ASC
   - 显示：Epic/Story Points/Assignee

2. **Sprint View**（Board）
   - 分组：Status
   - 过滤：Sprint = "Sprint 1"
   - 显示：Assignee/Story Points

3. **Roadmap View**（Timeline）
   - 时间轴：Date 字段
   - 分组：Epic
   - 显示：Milestone/Assignee

---

## 📋 实施步骤

### 步骤 1：创建 Project

1. 访问 https://github.com/JCVBoss/demon_village_game
2. 点击 "Projects" 标签
3. 点击 "New project"
4. 选择 "Board" 模板
5. 命名："魔王城 - Sprint Board"
6. 点击 "Create project"

---

### 步骤 2：配置自定义字段

1. 点击右上角菜单 → Settings
2. 点击 "Fields" → "New field"
3. 添加以下字段：

**Priority（优先级）**
```
类型：Single Select
选项：
- P0（红色）
- P1（橙色）
- P2（黄色）
- P3（灰色）
```

**Story Points（故事点）**
```
类型：Number
最小值：1
最大值：21
```

**Sprint（迭代）**
```
类型：Iteration
迭代周期：2 周
开始日期：2026-04-08
```

**Epic（史诗）**
```
类型：Single Select
选项：
- 核心系统（蓝色）
- 对话系统（绿色）
- 美术资源（紫色）
- 战斗系统（红色）
- 多结局系统（金色）
```

---

### 步骤 3：创建 Issue 模板

**位置：** `.github/ISSUE_TEMPLATE/`

**功能任务模板：** `feature.md`
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

## 估算
- 故事点：
- 优先级：
- Sprint：
```

**Bug 模板：** `bug.md`
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

## 优先级
- 优先级：
- 严重程度：
```

---

### 步骤 4：配置自动化

**内置自动化：**
1. 点击 "Workflows" → "New workflow"
2. 选择 "Built-in workflows"
3. 配置以下自动化：

**自动状态更新：**
```yaml
当 Issue 状态变更时：
- 新 Issue → Status = Todo
- 分配负责人 → Status = In Progress
- PR 合并 → Status = Review
- Issue 关闭 → Status = Done
```

**自动归档：**
```yaml
当任务满足条件时自动归档：
- Status = Done
- 关闭时间 > 7 天
```

---

### 步骤 5：迁移现有任务

**从 backlog.md 迁移：**

1. 打开 `docs/project/backlog.md`
2. 为每个任务创建 GitHub Issue
3. 填写自定义字段：
   - Priority
   - Story Points
   - Epic
   - Sprint
4. 关联到 Project

**批量导入脚本：**
```bash
#!/bin/bash
# 使用 GitHub CLI 批量创建 Issue

gh issue create \
  --title "DS-002 对话树解析器" \
  --body "实现对话树 JSON 解析器" \
  --label "feature" \
  --assignee "Claude" \
  --project "魔王城 - Sprint Board"
```

---

## 📊 最佳实践

### 1. Issue 管理规范

**命名规范：**
```
[类型] 简短描述

示例：
[FEAT] 实现对话树解析器
[FIX] 修复信任值计算错误
[DOCS] 更新项目管理手册
[TEST] 添加对话系统测试
```

**标签体系：**
```
优先级：
- P0-Critical
- P1-High
- P2-Medium
- P3-Low

类型：
- feature
- bug
- docs
- design
- art
- test

状态：
- blocked（需要帮助）
- needs-review（待评审）
- good-first-issue（适合新人）
```

---

### 2. Sprint 管理流程

**Sprint Planning：**
1. 创建 Sprint Milestone
2. 从 Backlog 拖拽任务到 Sprint
3. 估算故事点
4. 确认团队产能

**Daily Standup：**
1. 查看 Board 视图
2. 更新任务状态
3. 标记阻塞问题
4. 评论当日进展

**Sprint Review：**
1. 演示完成的 Issue
2. 收集反馈
3. 调整 Backlog 优先级

**Sprint Retrospective：**
1. 查看 Insights 图表
2. 分析 Velocity 变化
3. 制定改进计划

---

### 3. 可视化报告

**燃尽图配置：**
```
数据源：当前 Sprint
X 轴：日期
Y 轴：剩余故事点
过滤：Sprint = "Sprint 1"
```

**累积流图配置：**
```
数据源：所有任务
分组：Status
时间范围：最近 30 天
```

---

## 🔗 集成工作流

### 与 daily_logs 集成

**工作流：**
1. 每日站会更新 Issue 状态
2. 在 `daily_logs/` 写日志时引用 Issue
3. GitHub Actions 自动汇总到 Project

**示例：**
```markdown
## 2026-04-02 工作日志

### 今日完成
- [x] #123 实现对话系统
- [x] #125 陈默对话树设计

### 明日计划
- [ ] #126 夜鸦对话树设计
- [ ] #127 对话 UI 优化
```

---

### 与 PROGRESS.md 集成

**自动化同步：**
```yaml
name: Sync Progress

on:
  project:
    types: [item_converted]

jobs:
  update-progress:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Update PROGRESS.md
        run: |
          # 从 Project 读取数据
          # 更新 PROGRESS.md 进度矩阵
          # 提交更改
```

---

## 📈 成功指标

### 采用度指标
- [ ] 100% 任务在 Project 中追踪
- [ ] 100% 成员每日更新状态
- [ ] 100% PR 关联 Issue

### 效率指标
- [ ] 平均任务周期 < 3 天
- [ ] Sprint 完成率 > 80%
- [ ] 阻塞问题 < 24 小时解决

### 质量指标
- [ ] Bug 重开率 < 10%
- [ ] 代码评审时间 < 24 小时
- [ ] 文档更新及时率 > 90%

---

## 🎯 实施清单

### 第 1 周（准备）
- [ ] 创建 GitHub Project
- [ ] 配置自定义字段
- [ ] 创建 Issue 模板
- [ ] 配置自动化
- [ ] 团队培训

### 第 2 周（试点）
- [ ] 迁移 Backlog 任务
- [ ] 开始 Sprint 1
- [ ] 每日站会使用 Board
- [ ] 收集反馈

### 第 3 周（优化）
- [ ] 调整字段配置
- [ ] 优化自动化
- [ ] 完善 Issue 模板
- [ ] 形成习惯

### 第 4 周（常规）
- [ ] 全面使用 Project
- [ ] 停止使用本地 Kanban
- [ ] 只保留 Project 为事实来源
- [ ] 持续改进

---

## 📚 参考资源

### 官方文档
- [About Projects](https://docs.github.com/en/issues/planning-and-tracking-with-projects/learning-about-projects/about-projects)
- [Creating a project](https://docs.github.com/en/issues/planning-and-tracking-with-projects/creating-projects/creating-a-project)
- [Understanding fields](https://docs.github.com/en/issues/planning-and-tracking-with-projects/understanding-fields)
- [Best practices](https://docs.github.com/en/issues/planning-and-tracking-with-projects/learning-about-projects/best-practices-for-projects)

### 视频教程
- [GitHub Projects Tutorial](https://www.youtube.com/results?search_query=github+projects+tutorial)
- [Kanban with GitHub Projects](https://www.youtube.com/results?search_query=github+projects+kanban)

### 模板项目
- [Software Development Project](https://github.com/orgs/github/templates/software-development-project)
- [Bug Tracking](https://github.com/orgs/github/templates/bug-tracking)

---

*文档创建：2026-04-02 15:45*
*版本：v1.0*
*基于 GitHub Projects 官方文档*
*盒子管理员：Alice 🤖*
