# 错误日志

_记录开发过程中遇到的错误和解决方案_

---

## 2026-04-15 - web_fetch 403 错误

### 错误描述
```
web_fetch failed (403): SECURITY NOTICE
```

### 触发场景
尝试抓取 https://www.spriters-resource.com/pc_computer/stardewvalley/ 获取星露谷素材参考

### 原因分析
- 网站有 Cloudflare 等反爬虫保护
- web_fetch 工具被识别为机器人
- 403 Forbidden 拒绝访问

### 解决方案
1. ✅ 改用 web_search 搜索相关资源链接
2. ✅ 手动整理已知参考资源到文档
3. ✅ 提供链接让美工设计师自行访问

### 经验教训
- 对于有反爬保护的网站，优先使用 web_search 而非 web_fetch
- 参考资源文档提供链接即可，无需抓取具体内容
- 某些资源网站（如 Spriters Resource）需要人工浏览

---

## 通用错误处理指南

### exec 命令失败
- 检查路径是否存在：`ls -la <path>`
- 检查权限：`sudo <command>` 或确认用户权限
- 检查工作目录：`pwd`

### Git 操作失败
- 先 `git status` 查看状态
- 有冲突时 `git diff` 查看差异
- 需要时 `git stash` 暂存更改

### 文件操作失败
- 检查文件路径是否正确
- 检查父目录是否存在
- 检查文件权限

---

_持续更新中..._
