# 贡献指南

感谢你关注 Demon Village Game 项目！

## 贡献者角色

本项目采用多协作者模式，不同角色负责不同领域。详细角色说明请查看 **[CONTRIBUTORS.md](CONTRIBUTORS.md)**。

| 角色 | 成员 | 工作目录 |
|------|------|----------|
| 项目所有者 | JCVBoss | 整体协调 |
| 代码开发 | Claude (AI Agent) | `code/` |
| 文档设计 | Remote Agent (AI Agent) | `docs/` |
| 美术设计 | *待招募* | `code/assets/` |

## 项目协作方式

## Co-authored-by 使用规范

为了正确记录每位贡献者的工作，我们使用 `Co-authored-by` 标签在提交信息中标注协作者。

### 格式

```
<提交标题>

<提交描述>

Co-authored-by: 姓名 <邮箱>
```

### 示例

#### Claude 提交代码时的格式：
```
实现玩家移动系统

- 添加玩家输入处理
- 实现基础移动逻辑
- 添加动画状态机

Co-authored-by: Claude <noreply@anthropic.com>
```

#### 远端 Agent 提交文档时的格式：
```
编写游戏设计文档初稿

- 完成核心玩法设计
- 添加角色设定
- 绘制关卡草图

Co-authored-by: Remote Agent <remote-agent@example.com>
```

#### 多人协作时的格式：
```
集成玩家系统和关卡设计

- 实现玩家移动（Claude）
- 更新关卡文档（Remote Agent）

Co-authored-by: Claude <noreply@anthropic.com>
Co-authored-by: Remote Agent <remote-agent@example.com>
```

## 如何提交

### 对于 Claude (AI Agent)
当在 `code/` 目录进行开发时，在提交信息末尾添加：
```
Co-authored-by: Claude <noreply@anthropic.com>
```

### 对于远端 Agent
当在 `docs/` 目录进行工作时，在提交信息末尾添加：
```
Co-authored-by: [Agent名称] <[agent-email]>
```

### 对于项目所有者
可以直接提交，也可以标注协作者：
```
项目初始化和配置

Co-authored-by: Claude <noreply@anthropic.com>
```

## GitHub 识别

GitHub 会自动识别 `Co-authored-by` 标签，并将该提交同时显示在所有协作者的贡献记录中。

### 要求
1. 邮箱地址必须是协作者 GitHub 账户关联的邮箱
2. 格式必须正确（注意空格和尖括号）
3. 可以有多个 Co-authored-by 行

## 最佳实践

1. **清晰描述**：提交标题简洁明了，描述详细说明改动内容
2. **正确标注**：确保标注了所有实际贡献者
3. **及时同步**：定期推送和拉取更新
4. **冲突处理**：遇到冲突时及时沟通解决

## 测试要求

### 代码提交前测试

代码开发者在提交前必须验证代码能正常工作：

```bash
# 使用 Godot headless 模式验证项目
./godot/Godot_v4.6.1-stable_win64_console.exe --headless --quit --path demon_village_game/code
```

### 验证内容

- 项目能正常加载
- 无脚本语法错误
- Autoload 单例正常初始化

### 美术资源提交

- 确保文件格式正确（PNG/OGG）
- 文件命名规范：`[类型]_[名称].[扩展名]`
- 放入正确的目录结构

## 工作进展记录

每位贡献者应在 `daily_logs/<your_name>/` 目录下记录每日工作：

```markdown
# 日期：YYYY-MM-DD

## 今日完成
- [列出完成的工作]

## 进行中
- [正在进行的工作]

## 遇到的问题
- [问题描述及解决方案]

## 明日计划
- [下一步计划]
```