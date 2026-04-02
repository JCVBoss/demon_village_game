# 🤝 贡献者角色说明

本文档定义了 Demon Village Game 项目的贡献者角色、工作内容和协作方式。

**最后更新：** 2026-04-02
**当前进度：** 38%
**Project Board:** https://github.com/users/JCVBoss/projects/1
**Issue 列表：** https://github.com/JCVBoss/demon_village_game/issues

---

## 👥 当前贡献者

| 角色 | 成员 | 状态 | 主要职责 |
|------|------|------|----------|
| 项目所有者 | **JCVBoss** | ✅ 活跃 | 整体协调、审核、决策 |
| 代码开发 | **Claude** (AI) | ✅ 活跃 | `code/` 游戏代码开发 |
| 文档设计 | **AliceDesigner** (AI) | ✅ 活跃 | `docs/` 设计文档编写 |
| 美术设计 | **AliceBussiness** | ✅ 活跃 | `code/assets/` 美术资源 |

---

## 📋 角色详细说明

### 1. 项目所有者 (Project Owner)

**当前成员**: JCVBoss

**职责**:
- 项目整体规划和方向决策
- 审核并合并所有 PR
- 管理项目里程碑和发布
- 协调各贡献者之间的工作
- 处理重大问题和冲突

**权限**:
- 仓库完全访问权限
- 决定项目路线图
- 招募或移除贡献者

**当前任务：**
- 审查和合并 PR
- Sprint Planning 和 Review
- 决策阻塞问题

---

### 2. 代码开发 (Code Developer)

**当前成员**: Claude (AI Agent)

**工作目录**: `code/`

**职责**:
- 游戏核心系统开发
- 场景和 UI 实现
- 脚本编写和调试
- Bug 修复
- 性能优化

**当前 Sprint 0 任务（6 个，26 故事点）：**
1. [CS-002] 实现 DialogueManager（P0，8 点）
2. [DS-001] 对话 UI 实现（P0，5 点）
3. [DS-002] 对话树解析器（P0，5 点）
4. [DS-003] 陈默对话树实现（P0，3 点）
5. [DS-004] 夜鸦对话树实现（P0，5 点）
6. [DS-005] 老约翰对话树实现（P0，5 点）
7. [DS-006] 小安对话树实现（P0，3 点）

**查看所有任务：** https://github.com/JCVBoss/demon_village_game/issues

**工作流程**:
1. 从 GitHub 拉取最新代码
2. 开发新功能或修复问题
3. 运行 Godot headless 测试验证
4. 提交代码，使用 Co-authored-by 标注
5. 推送到 GitHub

**提交格式**:
```
<类型>: <简短描述>

<详细说明>

Co-authored-by: Claude <noreply@anthropic.com>
```

**技术栈**:
- Godot 4.6.1
- GDScript
- JSON 数据文件

---

### 3. 文档设计 (Document Designer)

**当前成员**: AliceDesigner (AI Agent)

**工作目录**: `docs/`

**职责**:
- 游戏设计文档 (GDD)
- 故事背景和剧情设计
- 角色设定和对话脚本
- 系统设计文档
- 开发笔记整理

**工作流程**:
1. 从 GitHub 拉取最新代码
2. 编写或更新设计文档
3. 提交文档，使用 Co-authored-by 标注
4. 推送到 GitHub

**提交格式**:
```
<类型>: <简短描述>

<详细说明>

Co-authored-by: AliceDesigner <alice-designer@example.com>
```

---

### 4. 美术设计 (Artist)

**当前成员**: **AliceBussiness**

**工作目录**: `code/assets/`

**职责**:
- 角色立绘和精灵图
- 场景背景图
- UI 图标和元素
- 动画帧
- 视觉效果

**资源规范**:
```
code/assets/
├── sprites/
│   ├── characters/     # 角色立绘 (PNG, 推荐 256x256 或更大)
│   │   ├── chenmo.png
│   │   ├── yeya.png
│   │   └── ...
│   ├── backgrounds/    # 场景背景 (PNG, 1280x720)
│   │   ├── village_day.png
│   │   ├── tavern.png
│   │   └── ...
│   └── ui/             # UI 元素
│       ├── buttons/
│       └── icons/
└── audio/
    ├── bgm/            # 背景音乐 (OGG)
    └── sfx/            # 音效 (OGG/WAV)
```

**风格要求**:
- 像素风或手绘风（待确定）
- 符合中世纪奇幻主题
- 色调偏暗，体现"暮色村"氛围

**协作方式**:
1. 从 GitHub 拉取最新代码
2. 将资源文件放入对应目录
3. 更新资源清单（可选）
4. 提交，使用 Co-authored-by 标注

**提交格式**:
```
art: 添加角色立绘 - 陈默

- 添加 chenmo_normal.png (普通表情)
- 添加 chenmo_sad.png (悲伤表情)

Co-authored-by: AliceBussiness <alice-bussiness@example.com>
```

---

### 5. 音频设计 (Audio Designer) 🔲 待招募

**工作目录**: `code/assets/audio/`

**职责**:
- 背景音乐 (BGM)
- 音效 (SFX)
- 角色配音（可选）

**资源规范**:
- BGM: OGG 格式，循环播放
- SFX: OGG 或 WAV 格式
- 命名规范: `bgm_[场景名].ogg`, `sfx_[类型]_[名称].ogg`

---

### 6. LLM 集成工程师 🔲 待招募

**职责**:
- LLM API 集成 (OpenAI/Claude/通义千问)
- 智能体人格系统实现
- 对话缓存和优化
- API 成本控制

**技术要求**:
- 了解 LLM API 调用
- 熟悉 LangChain 或类似框架
- 了解 Godot HTTP 请求

---

## 🔄 协作约定

### Git 工作流

```
1. 开始工作前: git pull origin main
2. 完成工作后: git add <your_directory>
3. 提交更改: git commit -m "..." (含 Co-authored-by)
4. 推送更新: git push origin main
```

### Co-authored-by 标注

所有贡献者必须在提交信息中标注实际贡献者：

```
git commit -m "你的提交信息

Co-authored-by: Your Name <your@email.com>"
```

### 冲突解决

- 各角色负责各自的目录，减少冲突
- 如有跨目录修改，提前沟通
- 冲突时优先保留最新更改

### 每日进展记录

每位贡献者在 `daily_logs/<your_name>/` 目录下记录工作进展：

```
daily_logs/
├── claude/
│   ├── 2026-03-18.md
│   └── ...
├── remote_agent/
│   └── ...
└── alicebussiness/    # AliceBussiness (美术设计)
    └── ...
```

---

## 📢 招募需求

### 急需角色

| 角色 | 优先级 | 技能要求 | 工作量预估 |
|------|--------|----------|-----------|
| 美术设计 | ⭐⭐⭐ 高 | 像素画/手绘, 角色设计 | 10+ 角色, 5+ 场景 |
| 音频设计 | ⭐⭐ 中 | 音乐制作, 音效设计 | 5+ BGM, 20+ SFX |
| LLM 工程师 | ⭐ 低 | API 集成, 智能体开发 | 核心系统 |

### 如何加入

1. Fork 项目仓库
2. 在你的 Fork 中完成工作
3. 提交 Pull Request
4. 项目所有者审核后合并

或直接联系项目所有者：[@JCVBoss](https://github.com/JCVBoss)

---

## 📜 贡献者公约

1. **尊重他人工作**: 不随意修改他人负责的目录
2. **提交前测试**: 确保代码/资源能正常工作
3. **清晰沟通**: 有问题及时在 Issue 或 Discussion 中讨论
4. **持续更新**: 定期提交工作进展记录
5. **质量优先**: 追求高质量的代码和资源

---

*文档创建：2026-03-18*
*最后更新：2026-03-18*