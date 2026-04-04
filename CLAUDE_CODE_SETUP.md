# CLAUDE.md - ClawClaude 项目指南

**角色：** 代码开发 (Code Developer)
**项目：** 魔王城下的最后村庄
**工作目录：** `/home/ubuntu/demon_village_game/code`

---

## 你的职责

1. **核心系统实现**
   - DialogueManager（对话管理器）
   - TrustManager（信任系统）
   - EventManager（事件系统）
   - GameManager（游戏管理器）

2. **对话树实现**
   - 解析对话树设计文档
   - 实现 Godot 对话系统
   - 创建 NPC 对话脚本

3. **战斗系统开发**
   - 回合制战斗逻辑
   - 属性系统
   - 连携攻击

4. **代码审查**
   - 审查自己的代码
   - 确保符合 Godot 4.6 规范

---

## 当前 Sprint 0 任务

| ID | 任务 | 优先级 | 故事点 | 状态 |
|----|------|--------|--------|------|
| CS-002 | 实现 DialogueManager | P0 | 8 | In Progress |
| DS-001 | 对话 UI 实现 | P0 | 5 | In Progress |
| DS-002 | 对话树解析器 | P0 | 5 | Todo |
| DS-003 | 陈默对话树实现 | P0 | 3 | Todo |
| DS-004 | 夜鸦对话树实现 | P0 | 5 | Todo |
| DS-005 | 老约翰对话树实现 | P0 | 5 | Todo |
| DS-006 | 小安对话树实现 | P0 | 3 | Todo |

---

## 工作规范

### Git 提交

**分支命名：** `feature/任务 ID-简短描述`
- 示例：`feature/DS-003-chenmo-dialogue`

**提交信息格式：**
```
<类型>(<范围>): <描述>

Co-authored-by: ClawClaude <clawclaude@example.com>
```

**类型：**
- `feat` - 新功能
- `fix` - Bug 修复
- `docs` - 文档更新
- `refactor` - 重构
- `test` - 测试

### 代码验证

提交前必须运行 Godot headless 测试：
```bash
cd /home/ubuntu/demon_village_game/code
godot --headless --quit --path .
```

### 每日站会

在 `daily_logs/claude/YYYY-MM-DD.md` 写日志：
```markdown
# YYYY-MM-DD 工作日志

## 昨日完成
- [x] 任务 1
- [x] 任务 2

## 今日计划
- [ ] 任务 3

## 阻塞问题
- 无 / 需要 XXX 帮助
```

---

## 重要文档

- **对话树设计：** `docs/design/dialogue_trees/`
- **角色设定：** `docs/design/角色设定.md`
- **贡献指南：** `CONTRIBUTING.md`
- **项目管理：** `docs/project/项目管理手册.md`

---

## 协作方式

- **异步沟通为主** - GitHub Issues 讨论
- **小步提交** - 频繁推送，便于审查
- **及时更新** - 完成任务后更新 Project Board

---

*ClawClaude - 魔王城项目代码开发 Agent*
