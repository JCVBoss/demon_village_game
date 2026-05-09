# 🏰 魔王城下的最后村庄

> "有时候，最勇敢的事不是打败魔王，而是保护你想保护的人。"

一个使用 **Godot 4.6** 开发的叙事驱动像素风 RPG。你扮演失去所有装备的勇者，在魔王城脚下的最后村庄里，用 10 天时间寻找伙伴和信念。

## 📖 游戏简介

- **🎭 叙事驱动** — 10 位各有秘密的村民，你的选择影响故事走向
- **🤖 双模式对话** — 一周目预设对话树保证叙事质量，二周目 LLM 智能体解锁动态对话
- **💖 信任系统** — 每个村民有隐藏信任值，影响对话和结局
- **🎯 多结局** — 12 种结局，由陈默/夜鸦/勇者三个关键选择决定
- **🕹️ 游戏时长** — 约 3.5 小时

## 📊 当前进度：约 55%

| 模块 | 状态 | 说明 |
|------|------|------|
| 核心系统 | ✅ 基本完成 | GameManager、DialogueManager、TrustManager、EventManager、SaveSystem |
| 对话系统 | ✅ 基本完成 | DialogueTreeParser + JSON 对话树（陈默等 NPC 已录入） |
| 玩家角色 | ✅ 完成 | 8 方向移动、动画、交互检测 |
| 村民 NPC | ✅ 基础完成 | Villager 场景 + 10 个角色立绘（多表情） |
| 地图系统 | ✅ 基本完成 | TileMap + 村庄地图 + 瓦片集 |
| UI 系统 | ✅ 基本完成 | 主菜单、对话框、暂停菜单、存档/读档 |
| 对话内容 | 🟡 部分完成 | 部分 NPC 对话树已录入 JSON |
| 美术资源 | ✅ 占位完成 | 10 位村民立绘、场景背景、UI 素材（待替换为高质量资源） |
| 战斗系统 | ❌ 未开始 | 设计中有，代码中待实现 |
| 多结局 | ❌ 部分 | trigger_final_chapter() 有占位 |
| LLM 集成 | ❌ 未开始 | 二周目功能 |
| 音频 | ❌ 未开始 | 待添加 |

## 🎮 快速开始

1. 安装 [Godot 4.6.1](https://godotengine.org/download)
2. 打开 Godot → 导入项目 → 选择 `code/project.godot`
3. 按 F5 运行

## 📁 项目结构

```
demon_village_game/
├── code/                          # 游戏源代码（Godot 项目）
│   ├── project.godot              # Godot 项目配置
│   ├── scenes/                    # 场景文件
│   ├── scripts/                   # GDScript 脚本
│   │   ├── core/                  # 核心系统（单例）
│   │   ├── ui/                    # UI 脚本
│   │   ├── characters/            # 角色脚本
│   │   ├── dialogue/              # 对话解析器
│   │   └── locations/             # 场景脚本
│   ├── assets/                    # 美术资源
│   │   └── sprites/               # 精灵图（角色/场景/UI/瓦片）
│   └── resources/                 # 数据文件
│       ├── dialogues/             # 对话树 JSON
│       ├── events/                # 事件触发配置
│       ├── maps/                  # 地图配置
│       └── tilesets/              # 瓦片集
├── docs/                          # 设计文档
│   ├── design/                    # 游戏设计
│   │   ├── 角色设定.md            # 10 位村民详细设定
│   │   ├── 故事背景与主线.md      # 世界观 + 主线 + 多结局
│   │   ├── 系统设计.md            # 核心系统架构
│   │   ├── 双模式对话设计.md      # 对话系统架构
│   │   ├── dialogue_trees/        # 各 NPC 对话树设计
│   │   ├── maps/                  # 地图设计文档
│   │   └── personas/              # 角色人格卡（LLM 用）
│   └── reference/                 # 参考资料
├── tools/                         # 资源生成工具
└── daily_logs/                    # 开发日志
```

## 🗺️ 下一步计划

1. **可运行 Demo** — 整合现有代码，确保 F5 能跑起一个可玩场景
2. **对话内容补充** — 完成全部 10 个 NPC 的对话树 JSON 录入
3. **战斗系统** — 回合制战斗 + 对话驱动
4. **美术资源替换** — 用开源/免费高质量像素资源替换占位图
5. **多结局实现** — 最终章 + 结局分支

## 📄 许可证

待定

## 📬 联系方式

- 仓库: [JCVBoss/demon_village_game](https://github.com/JCVBoss/demon_village_game)
- 项目所有者: @JCVBoss
- 开发: Alice (AI Agent)

---

*最后更新：2026-05-09*
*文档维护：Alice 🤖*
