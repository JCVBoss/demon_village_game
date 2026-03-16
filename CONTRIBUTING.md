# 贡献指南

## 项目协作方式

本项目由多位协作者共同维护：
- **JCVBoss** - 项目所有者，负责整体协调和审核
- **Claude (AI Agent)** - 负责 `code/` 目录的游戏代码开发
- **远端 Agent** - 负责 `docs/` 目录的设计文档编写

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