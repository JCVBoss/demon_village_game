# 地图可视化工具

这是一个用于可视化《魔王城下的最后村庄》游戏地图的HTML工具。

## 使用方法

### 本地查看

1. 直接用浏览器打开 `docs/map-viewer/index.html` 文件
2. 选择不同的地图查看：
   - 暮色村
   - 迷雾森林
   - 世界地图

### GitHub Pages 部署

这个工具已经配置好可以直接部署到 GitHub Pages：

1. 提交代码到 GitHub 仓库
2. 在仓库的 Settings > Pages 中配置：
   - Source: Deploy from a branch
   - Branch: main, folder: /docs/map-viewer
3. 等待部署完成，访问提供的 URL

## 功能特性

- 📊 读取 JSON 配置文件动态渲染地图
- 🔍 缩放控制
- 🏘️ 建筑、NPC、事件点可视化
- 📍 点击显示瓦片信息
- 🎨 美观的深色主题界面

## 文件结构

```
docs/map-viewer/
├── index.html          # 主页面
├── styles.css          # 样式文件
├── script.js           # JavaScript 逻辑
├── village_config.json # 村庄地图配置
├── forest_config.json  # 森林地图配置
└── world_config.json   # 世界地图配置
```
