# 贡献指南

感谢你关注 **魔王城下的最后村庄** 项目！

## 👥 当前团队

| 角色 | 成员 | 职责 |
|------|------|------|
| 项目所有者 | JCVBoss | 决策、审核、方向把控 |
| 开发 | Alice (AI Agent) | 代码、文档、资源整合 |

## 🚀 参与方式

### 提交代码或建议

1. Fork 项目仓库
2. 创建功能分支：`git checkout -b feature/your-feature`
3. 提交更改：`git commit -m "feat: 描述"`
4. 推送分支：`git push origin feature/your-feature`
5. 创建 Pull Request

### 报告问题

在 [Issues](https://github.com/JCVBoss/demon_village_game/issues) 中提交 Bug 或功能建议。

## 📋 开发规范

### Git 提交格式

```
<type>(<scope>): <subject>

<body>
```

**Type 说明：**
- `feat` - 新功能
- `fix` - 修复
- `docs` - 文档
- `refactor` - 重构
- `art` - 美术资源
- `chore` - 杂项

**示例：**
```
feat(dialogue): 补充金铃对话树

- 添加 4 个信任阶段的对话节点
- 补充特殊事件触发对话
```

### 代码规范

- GDScript 遵循 Godot 官方风格指南
- 函数和变量使用 snake_case
- 场景节点使用 PascalCase
- 添加必要注释

### 美术资源

- 使用开源/免费资源（OpenGameArt、Itch.io 等）
- 格式：PNG（精灵图）、OGG（音频）
- 命名：`[类型]_[名称].[扩展名]`
- 像素风格：16x16 或 32x32 瓦片

---

*最后更新：2026-05-09*
