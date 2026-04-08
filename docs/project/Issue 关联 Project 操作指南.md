<!-- [TAG] 所有者:PO|维护责任人:SM|创建时间:2026-04-03|生效标记:✅|最后更新:2026-04-03|版本:v1.0 -->

# 📋 Issue 关联 Project 操作指南

> 手动关联 Issue 到项目看板，保持看板整洁

---

## 🎯 设计原则

**为什么不自动关联？**

- ❌ 避免无关 Issue 进入看板（如问题咨询、文档勘误）
- ✅ 保持看板聚焦于**开发任务**
- ✅ 只有**正式任务**才进入 Project Board

---

## 📝 何时关联 Issue 到 Project

### ✅ 应该关联的情况

| 类型 | 示例 | 关联 |
|------|------|------|
| 功能开发 | `[CS-005] LLM API 集成` | ✅ 是 |
| 对话树实现 | `[DS-003] 陈默对话树` | ✅ 是 |
| 美术资源 | `[AR-011] 村庄场景` | ✅ 是 |
| 战斗系统 | `[BS-001] 战斗 UI` | ✅ 是 |
| 多结局实现 | `[ME-001] 结局分支逻辑` | ✅ 是 |

### ❌ 不需要关联的情况

| 类型 | 示例 | 关联 |
|------|------|------|
| 问题咨询 | "如何运行游戏？" | ❌ 否 |
| 文档勘误 | "README 有个错别字" | ❌ 否 |
| 讨论建议 | "建议增加 XX 功能" | ❌ 否 |
| Bug 报告（轻微） | "UI 颜色不对" | ❌ 否 |

---

## 🔧 关联步骤

### 方法 1：创建 Issue 时关联（推荐）

**步骤：**

1. 创建 Issue: https://github.com/JCVBoss/demon_village_game/issues/new

2. 填写标题和描述

3. 在右侧边栏找到 **Projects** 部分

4. 点击设置图标 ⚙️

5. 选择：**"魔王城下的最后村庄"** (Project #1)

6. 创建 Issue

**效果：** Issue 创建后自动出现在 Project 的 Todo 列

---

### 方法 2：Issue 创建后关联

**步骤：**

1. 打开已创建的 Issue

2. 点击右侧边栏的 **Projects** 部分

3. 点击设置图标 ⚙️

4. 选择：**"魔王城下的最后村庄"**

**效果：** Issue 会添加到 Project，默认在 Todo 列

---

### 方法 3：使用 GitHub CLI

```bash
# 关联现有 Issue 到 Project
gh project item-add 1 --owner JCVBoss --url "https://github.com/JCVBoss/demon_village_game/issues/25"
```

---

## 📊 Project 自动化状态

| 自动化 | 状态 | 说明 |
|--------|------|------|
| 新 Issue 自动添加 | ❌ **禁用** | 手动关联，保持看板整洁 |
| Issue 关闭自动 Done | ✅ **启用** | 关闭后自动移动到 Done 列 |
| PR 合并自动关闭 | ✅ **GitHub 原生** | 使用 `Closes #123` 语法 |

---

## 🎯 推荐工作流程

### 创建新任务

```
1. 创建 Issue
   ↓
2. 判断是否需要进入 Project
   ↓
3. 是 → 手动关联到 Project
   ↓
4. Issue 出现在 Todo 列
   ↓
5. 拖拽到 In Progress（开始工作）
   ↓
6. 完成任务，关闭 Issue
   ↓
7. 自动移动到 Done 列 ✅
```

---

## 📝 Issue 命名规范

**推荐格式：**
```
[类型 - 编号] 任务描述
```

**示例：**
- `[CS-002] 实现 DialogueManager`
- `[DS-003] 陈默对话树实现`
- `[AR-011] 村庄场景`
- `[BS-001] 战斗 UI 实现`

**类型代码：**
| 代码 | 类型 | 说明 |
|------|------|------|
| CS | Core System | 核心系统 |
| DS | Dialogue System | 对话系统 |
| AR | Art Resources | 美术资源 |
| BS | Battle System | 战斗系统 |
| ME | Multi-Ending | 多结局系统 |

---

## 🧪 测试验证

### 测试手动关联

```bash
# 1. 创建测试 Issue（不关联 Project）
gh issue create --title "[TEST] 测试手动关联" --body "测试" --repo JCVBoss/demon_village_game

# 2. 手动关联到 Project
gh project item-add 1 --owner JCVBoss --url "https://github.com/JCVBoss/demon_village_game/issues/XX"

# 3. 验证是否在 Project 中
gh project item-list 1 --owner JCVBoss --limit 30 | grep "TEST"
```

---

## 🔗 快速链接

| 用途 | 链接 |
|------|------|
| Project Board | https://github.com/users/JCVBoss/projects/1 |
| 新建 Issue | https://github.com/JCVBoss/demon_village_game/issues/new |
| Issue 列表 | https://github.com/JCVBoss/demon_village_game/issues |

---

## 📝 更新记录

| 日期 | 更新内容 | 更新人 |
|------|---------|--------|
| 2026-04-03 | 初始版本，明确手动关联原则 | AliceDesigner |

---

*文档创建：2026-04-03*
*Issue 关联 Project 操作指南*
*盒子管理员：Alice 🤖*
