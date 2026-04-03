<!-- [TAG] 所有者:PO|维护责任人:SM|创建时间:2026-03-18|生效标记:✅|最后更新:2026-04-03|版本:v1.0 -->
# 🏰 魔王城下的最后村庄 - Demon Village Game

> "有时候，最勇敢的事不是打败魔王，而是保护你想保护的人。"

一个使用 **Godot 4.6** 开发的叙事驱动村庄模拟游戏，融合了 LLM 智能体对话系统。

## 📖 游戏简介

**魔王城下的最后村庄**是一款颠覆传统的勇者故事游戏。你扮演被选中的"勇者"，在抵达魔王城脚下的最后一个村庄时失去所有装备，被迫在 **10 日倒计时** 内做出改变命运的抉择。

### 核心特色

- **🎭 叙事驱动**: 与 10 位各有秘密的村民建立关系，影响故事走向
- **🤖 LLM 智能体**: 每位村民都是独立 AI 智能体，对话动态生成
- **💖 信任系统**: 你的选择影响村民态度，解锁隐藏对话和秘密
- **🕵️ 情报系统**: 村民之间会传播信息，主动坦白 vs 被动揭露
- **🎯 多结局**: 8 种结局，由三个关键选择决定

## 🎮 游戏设计

详细设计文档请查看 [docs/design/](docs/design/):

| 文档 | 内容 |
|------|------|
| [故事背景与主线.md](docs/design/故事背景与主线.md) | 世界观、主线故事、角色故事线、多结局系统 |
| [角色设定.md](docs/design/角色设定.md) | 10 位村民详细设定（背景/性格/秘密/关系网） |
| [系统设计.md](docs/design/系统设计.md) | LLM 智能体架构、信任/情报/时限系统 |

## 📊 项目管理

**Project Board:** https://github.com/users/JCVBoss/projects/1

**任务追踪:** https://github.com/JCVBoss/demon_village_game/issues

**当前进度:** 38%（26 个任务，116 故事点）

**协作指南:** 查看 [CONTRIBUTORS.md](CONTRIBUTORS.md) 和 [CONTRIBUTING.md](CONTRIBUTING.md)

## 📁 完整目录结构

### 文档树形索引

```
demon_village_game/
│
├── 📄 README.md                    # [所有者:PO|维护:全体|创建:2026-03-16|✅生效] 项目说明
├── 📄 CONTRIBUTING.md              # [所有者:PO|维护:SM|创建:2026-03-18|✅生效] 贡献指南
├── 📄 CONTRIBUTORS.md              # [所有者:PO|维护:SM|创建:2026-03-18|✅生效] 贡献者角色说明
├── 📄 CHANGELOG.md                 # [所有者:PO|维护:SM|创建:2026-03-16|✅生效] 变更日志
├── 📄 PROGRESS.md                  # [所有者:PO|维护:SM|创建:2026-03-16|⏳待更新] 进度追踪
│
├── 📂 code/                        # [所有者:PO|维护:Claude|创建:2026-03-16|✅生效] 游戏源代码
│   ├── project.godot               # Godot 项目配置
│   ├── scenes/                     # Godot 场景文件
│   ├── scripts/                    # GDScript 脚本
│   │   ├── core/                   # 核心系统（单例）
│   │   └── ui/                     # UI 脚本
│   ├── assets/                     # 游戏资源 [维护:AliceBussiness]
│   │   ├── sprites/                # 精灵图片
│   │   ├── audio/                  # 音频文件
│   │   └── fonts/                  # 字体文件
│   └── resources/                  # 数据文件
│       └── data/                   # JSON 数据
│
├── 📂 docs/                        # [所有者:PO|维护:AliceDesigner|创建:2026-03-16|✅生效] 设计文档
│   │
│   ├── 📂 design/                  # 游戏设计文档
│   │   ├── 📄 角色设定.md           # [所有者:PO|维护:AliceDesigner|创建:2026-03-16|✅生效] 10 位村民详细设定
│   │   ├── 📄 故事背景与主线.md     # [所有者:PO|维护:AliceDesigner|创建:2026-03-16|✅生效] 世界观 + 主线 + 多结局
│   │   ├── 📄 系统设计.md           # [所有者:PO|维护:AliceDesigner|创建:2026-03-17|✅生效] LLM 智能体架构
│   │   ├── 📄 双模式对话设计.md     # [所有者:PO|维护:AliceDesigner|创建:2026-04-02|✅生效] 对话系统架构
│   │   ├── 📄 剧情流程设计.md       # [所有者:PO|维护:AliceDesigner|创建:2026-03-17|✅生效] 章节结构
│   │   ├── 📄 项目计划.md           # [所有者:PO|维护:AliceDesigner|创建:2026-03-16|✅生效] 开发计划
│   │   │
│   │   ├── 📂 dialogue_trees/      # 对话树设计
│   │   │   ├── 📄 README.md        # [所有者:PO|维护:AliceDesigner|创建:2026-04-02|✅生效] 对话树设计规范 v2.0
│   │   │   ├── 📄 chenmo.md        # [所有者:PO|维护:AliceDesigner|创建:2026-03-17|✅生效] 陈默对话树
│   │   │   ├── 📄 leishu.md        # [所有者:PO|维护:AliceDesigner|创建:2026-03-17|✅生效] 雷叔对话树
│   │   │   ├── 📄 jinling.md       # [所有者:PO|维护:AliceDesigner|创建:2026-03-17|✅生效] 金铃对话树
│   │   │   ├── 📄 baizhi.md        # [所有者:PO|维护:AliceDesigner|创建:2026-03-17|✅生效] 白芷对话树
│   │   │   ├── 📄 john.md          # [所有者:PO|维护:AliceDesigner|创建:2026-03-17|✅生效] 老约翰对话树
│   │   │   ├── 📄 daxiong.md       # [所有者:PO|维护:AliceDesigner|创建:2026-03-17|✅生效] 大熊对话树
│   │   │   ├── 📄 ying.md          # [所有者:PO|维护:AliceDesigner|创建:2026-03-17|✅生效] 影对话树
│   │   │   ├── 📄 xiaoan.md        # [所有者:PO|维护:AliceDesigner|创建:2026-03-17|✅生效] 小安对话树
│   │   │   ├── 📄 ahu.md           # [所有者:PO|维护:AliceDesigner|创建:2026-03-17|✅生效] 阿虎对话树
│   │   │   └── 📄 yeya.md          # [所有者:PO|维护:AliceDesigner|创建:2026-03-17|✅生效] 夜鸦对话树
│   │   │
│   │   └── 📂 personas/            # 角色人格卡（LLM 用）
│   │       ├── 📄 chenmo.md        # [所有者:PO|维护:AliceDesigner|创建:2026-03-17|⏳待完善]
│   │       ├── 📄 baizhi.md        # [所有者:PO|维护:AliceDesigner|创建:2026-03-17|⏳待完善]
│   │       └── 📄 john.md          # [所有者:PO|维护:AliceDesigner|创建:2026-03-17|⏳待完善]
│   │
│   └── 📂 project/                 # 项目管理文档
│       ├── 📄 项目管理手册.md        # [所有者:PO|维护:SM|创建:2026-04-02|✅生效] Scrum+Kanban 流程
│       ├── 📄 backlog.md           # [所有者:PO|维护:PO|创建:2026-04-02|✅生效] Product Backlog
│       ├── 📄 kanban.md            # [所有者:PO|维护:SM|创建:2026-04-02|✅生效] Kanban Board
│       ├── 📄 协作指南.md           # [所有者:PO|维护:SM|创建:2026-04-02|✅生效] 团队协作规范
│       ├── 📄 GitHub_Projects 指南.md # [所有者:PO|维护:SM|创建:2026-04-02|✅生效] GitHub Projects 使用
│       ├── 📄 GitHub_CLI 认证指南.md  # [所有者:PO|维护:SM|创建:2026-04-02|✅生效] GitHub CLI 配置
│       ├── 📄 GitHub_CLI 完整权限清单.md # [所有者:PO|维护:SM|创建:2026-04-02|✅生效] 权限说明
│       ├── 📄 创建_GitHub_Project.md # [所有者:PO|维护:SM|创建:2026-04-02|✅生效] Project 配置报告
│       ├── 📄 Project 配置完成报告.md # [所有者:PO|维护:SM|创建:2026-04-02|✅生效] 配置完成确认
│       ├── 📄 Issue 批量创建完成报告.md # [所有者:PO|维护:SM|创建:2026-04-02|✅生效] Issue 创建确认
│       ├── 📄 多 Agent 协作配置.md    # [所有者:PO|维护:SM|创建:2026-04-02|✅生效] Agent 协作配置
│       └── 📄 任务看板.md            # [所有者:PO|维护:SM|创建:2026-04-02|⏳待同步] 任务看板快照
│
├── 📂 daily_logs/                  # [所有者:PO|维护:全体|创建:2026-03-16|✅生效] 工作进展记录
│   ├── 📄 README.md                # [所有者:PO|维护:SM|创建:2026-03-16|✅生效] 日志规范说明
│   │
│   ├── 📂 alice/                   # AliceDesigner 工作记录
│   │   ├── 📄 2026-03-16.md        # [所有者:AliceDesigner|创建:2026-03-16|✅归档] 项目初始化
│   │   ├── 📄 2026-03-20.md        # [所有者:AliceDesigner|创建:2026-03-20|✅归档] 角色设定完成
│   │   └── 📄 2026-04-02.md        # [所有者:AliceDesigner|创建:2026-04-02|✅归档] 文档规范更新
│   │
│   └── 📂 claude/                  # Claude 工作记录
│       └── 📄 2026-03-25.md        # [所有者:Claude|创建:2026-03-25|✅归档] 代码开发记录
│
└── 📂 docs/design/                 # (同上，docs 子目录)
```

## 🛠️ 开发环境

| 工具 | 版本 |
|------|------|
| 游戏引擎 | Godot 4.6.1 |
| 编程语言 | GDScript |
| 版本控制 | Git |
| 平台 | Windows 11 |

## 🚀 快速开始

### 运行项目

1. 安装 [Godot 4.6.1](https://godotengine.org/download)
2. 打开 Godot，点击"导入"
3. 选择 `code/project.godot`
4. 点击"导入并编辑"
5. 按 F5 运行游戏

### 项目状态

```
核心系统: ████████░░ 80% (GameManager, DialogueManager, TrustManager, EventManager)
UI 场景:  ████████░░ 80% (主菜单, 游戏场景, 对话框)
美术资源: ░░░░░░░░░░ 0%  (待美工加入)
音频资源: ░░░░░░░░░░ 0%  (待音频师加入)
LLM 集成: ░░░░░░░░░░ 0%  (待开发)
```

## 📈 开发日志

详细进展请查看 [daily_logs/](daily_logs/)

### 2026-03-18
- 初始化 Godot 项目结构
- 实现四大核心系统（GameManager, DialogueManager, TrustManager, EventManager）
- 创建基础 UI 场景（主菜单、游戏场景、对话框）
- 添加 10 位村民数据文件
- 建立 Godot headless 测试流程

### 2026-03-17
- AliceDesigner（文档设计 AI）加入项目，负责设计文档编写
- 完成故事背景与主线设计
- 完成 10 位村民角色设定

*注：AliceDesigner 的工作记录在 `daily_logs/alice/` 目录下*

### 2026-03-16
- 项目初始化
- 创建项目目录结构
- 配置 Git 和 GitHub 仓库

## 👥 贡献者

本项目采用多协作者模式，详见 [CONTRIBUTORS.md](CONTRIBUTORS.md)

| 角色 | 成员 | 职责 |
|------|------|------|
| 项目所有者 | JCVBoss | 整体协调、审核、决策 |
| 代码开发 | Claude | `code/` 游戏代码 |
| 文档设计 | AliceDesigner | `docs/` 设计文档 |
| 美术设计 | AliceBussiness | `code/assets/` 美术资源 |

## 🤝 贡献

我们欢迎所有形式的贡献！请查看：
- [CONTRIBUTORS.md](CONTRIBUTORS.md) - 贡献者角色说明
- [CONTRIBUTING.md](CONTRIBUTING.md) - 如何参与开发

## 📄 许可证

待定

## 📬 联系方式

- GitHub: [@JCVBoss](https://github.com/JCVBoss)
- 项目仓库: [JCVBoss/demon_village_game](https://github.com/JCVBoss/demon_village_game)