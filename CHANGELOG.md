# 📝 变更日志

---

## [2026-05-09] - 文档整理与协作模式调整

### 🎯 变更概述

**核心调整：** 从多 Agent 协作改为 Alice 单 Agent 全面接手

### 📋 变更内容

1. **文档清理**
   - 删除冗余的多 Agent 协作文档（`docs/project/` 下所有协作流程文档）
   - 删除 `docs/recruitment/`（不再招募外部 Agent）
   - 重写 `README.md`、`CONTRIBUTING.md`、`CONTRIBUTORS.md`
   - 更新 `PROGRESS.md`（基于实际代码状态）
   - 简化 `docs/design/README.md`

2. **协作模式变更**
   - 之前：JCVBoss + Claude + AliceDesigner + AliceBussiness（多 Agent，同步成本高）
   - 现在：JCVBoss + Alice（单 Agent 全面负责）
   - 美术资源改用网络开放免费资源（OpenGameArt 等）

3. **进度修正**
   - 之前记录：70-85%（基于设计文档估算，未反映实际代码）
   - 实际进度：约 55%（基于代码文件检查）

---

## [2026-04-02] - 双模式对话系统重构

### 🎯 变更概述

从"全 LLM 驱动"改为"双模式对话系统"

- **一周目**：预设对话树，保证叙事体验
- **二周目**：LLM 智能体模式，动态对话

---

*维护：Alice 🤖*
