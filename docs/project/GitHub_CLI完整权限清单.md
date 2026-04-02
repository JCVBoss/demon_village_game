# 🔐 GitHub CLI 完整权限清单

> 一次性申请所有项目管理需要的权限

---

## 📋 所需权限总览

### 已拥有的权限 ✅
- `repo` - 仓库完全控制（创建 Issue/PR）
- `workflow` - 工作流管理（自动化）
- `read:org` - 组织信息读取
- `read:project` - 项目读取
- `gist` - Gist 管理

### 还需要申请的权限 ⏳
- `project` - 项目写入（创建/编辑 Project）

---

## 🎯 完整权限列表（推荐一次性申请）

### 核心权限（必须）
| 权限 | 用途 | 必需性 |
|------|------|--------|
| `repo` | 创建/管理 Issue、PR、仓库 | ✅ 必须 |
| `project` | 创建/管理 Project、字段、视图 | ✅ 必须 |
| `workflow` | 管理 GitHub Actions 自动化 | ✅ 必须 |

### 辅助权限（推荐）
| 权限 | 用途 | 推荐度 |
|------|------|--------|
| `read:org` | 读取组织信息、团队成员 | 🟡 推荐 |
| `write:org` | 管理组织成员、团队 | 🟡 推荐 |
| `read:package` | 读取包信息 | ⚪ 可选 |
| `write:package` | 发布/管理包 | ⚪ 可选 |

### 高级权限（按需）
| 权限 | 用途 | 使用场景 |
|------|------|----------|
| `admin:org` | 组织管理 | 管理大型组织 |
| `write:packages` | 发布 Docker 包 | 容器化部署 |
| `codespace` | 管理 Codespaces | 云端开发 |

---

## 🚀 一次性申请命令

### 方案 A：最小权限集（推荐）

**适合：** 小型团队，专注项目管理

```bash
gh auth refresh --hostname github.com \
  -s repo,project,workflow,read:org
```

**权限说明：**
- `repo` - Issue/PR/仓库管理
- `project` - Project 创建和管理
- `workflow` - 自动化工作流
- `read:org` - 读取组织信息

---

### 方案 B：完整权限集（推荐管理员）

**适合：** 项目所有者，需要完整管理

```bash
gh auth refresh --hostname github.com \
  -s repo,project,workflow,read:org,write:org,read:package,write:package
```

**权限说明：**
- 包含方案 A 所有权限
- + `write:org` - 组织管理
- + `read:package` - 包读取
- + `write:package` - 包发布

---

### 方案 C：超级管理员权限

**适合：** 组织管理员，完全控制

```bash
gh auth refresh --hostname github.com \
  -s repo,project,workflow,read:org,write:org,admin:org,read:package,write:package,codespace
```

**注意：** 权限过大，谨慎使用

---

## 📝 当前状态

### 已认证权限 ✅
```
✓ repo - 仓库管理
✓ workflow - 工作流
✓ read:org - 组织读取
✓ read:project - 项目读取
✓ gist - Gist 管理
```

### 待申请权限 ⏳
```
⏳ project - 项目写入（创建/编辑 Project）
```

---

## 🎯 立即执行

**运行以下命令，一次性申请所有需要的权限：**

```bash
gh auth refresh --hostname github.com \
  -s repo,project,workflow,read:org,write:org
```

**然后：**
1. 浏览器会自动打开
2. 或者访问 https://github.com/login/device
3. 输入显示的设备代码
4. 点击 "Authorize github"
5. 完成！

---

## ✅ 验证权限

**申请完成后，验证权限：**

```bash
gh auth status
```

**期望输出：**
```
github.com
  ✓ Logged in to github.com account JCVBoss
  - Token scopes: 'repo', 'project', 'workflow', 'read:org', 'write:org'
```

**测试 Project 写入权限：**

```bash
gh project list --owner JCVBoss
gh project create --title "测试项目" --owner JCVBoss
```

---

## 🔒 安全提示

### 权限原则
- **最小权限原则** - 只申请需要的权限
- **定期审查** - 每 90 天检查一次
- **及时撤销** - 不再使用的权限及时删除

### Token 管理
- **查看 Token：** https://github.com/settings/tokens
- **撤销 Token：** 点击 Delete
- **重新生成：** 删除后重新认证

---

## 📚 权限详解

### repo
**范围：** 所有仓库
**权限：**
- ✅ 创建/编辑/删除 Issue
- ✅ 创建/编辑/合并 PR
- ✅ 管理仓库设置
- ✅ 管理 Releases
- ✅ 管理 Wiki

### project
**范围：** 所有项目
**权限：**
- ✅ 创建/编辑/删除 Project
- ✅ 添加/编辑/删除自定义字段
- ✅ 管理项目视图
- ✅ 添加/移动/删除项目项

### workflow
**范围：** 所有工作流
**权限：**
- ✅ 运行/取消工作流
- ✅ 查看工作流日志
- ✅ 管理工作流文件

### read:org / write:org
**范围：** 组织
**权限：**
- ✅ 读取组织信息
- ✅ 管理团队成员
- ✅ 管理团队权限

---

## 🎯 推荐方案

**对于魔王城项目，推荐使用方案 A + write:org：**

```bash
gh auth refresh --hostname github.com \
  -s repo,project,workflow,read:org,write:org
```

**原因：**
- ✅ 覆盖所有项目管理需求
- ✅ 不过度授权
- ✅ 未来扩展性好

---

*文档创建：2026-04-02 16:22*
*版本：v2.0*
*完整权限清单*
*盒子管理员：Alice 🤖*
