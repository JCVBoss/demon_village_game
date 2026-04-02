# 🎨 UI 素材包清单

**最后更新：** 2026-04-02  
**负责人：** AliceBussiness  
**状态：** ✅ 完成

---

## 📦 对话框

| 文件 | 尺寸 | 描述 | 状态 |
|------|------|------|------|
| `dialogue_box.png` | 800x180 | 主对话框背景 | ✅ |
| `dialogue_box_small.png` | 500x120 | 小型对话框（NPC 对话） | ✅ |

**设计特点:**
- 圆角矩形（15px/12px radius）
- 半透明深色背景
- 金色边框装饰
- 四角金色装饰

---

## 🔘 按钮 (3 状态)

### 大按钮 (200x50)
| 文件 | 尺寸 | 状态 |
|------|------|------|
| `button_large.png` | 200x50 | 正常 |
| `button_large_hover.png` | 200x50 | 悬停 |
| `button_large_pressed.png` | 200x50 | 按下 |

### 中按钮 (150x45)
| 文件 | 尺寸 | 状态 |
|------|------|------|
| `button_medium.png` | 150x45 | 正常 |
| `button_medium_hover.png` | 150x45 | 悬停 |
| `button_medium_pressed.png` | 150x45 | 按下 |

### 小按钮 (100x40)
| 文件 | 尺寸 | 状态 |
|------|------|------|
| `button_small.png` | 100x40 | 正常 |
| `button_small_hover.png` | 100x40 | 悬停 |
| `button_small_pressed.png` | 100x40 | 按下 |

**设计特点:**
- 圆角矩形（8px radius）
- 三态变化（正常/悬停/按下）
- 金色边框
- 悬停时高亮

---

## 📊 进度条

| 文件 | 尺寸 | 描述 |
|------|------|------|
| `progress_bar_bg.png` | 200x20 | 进度条背景 |
| `progress_fill_low.png` | 56x20 | 低进度填充（30%，红色） |
| `progress_fill_mid.png` | 116x20 | 中进度填充（60%，黄色） |
| `progress_fill_high.png` | 196x20 | 高进度填充（100%，绿色） |

---

## 💖 信任值指示器

| 文件 | 尺寸 | 描述 |
|------|------|------|
| `trust_heart.png` | 32x32 | 心形图标 |
| `trust_bar.png` | 100x12 | 信任条（渐变：红→黄→绿） |

**设计特点:**
- 心形使用数学公式绘制
- 信任条三色渐变（低/中/高）
- 符合游戏"信任系统"主题

---

## 🎯 图标 (32x32)

| 文件 | 尺寸 | 描述 | 颜色 |
|------|------|------|------|
| `icon_settings.png` | 32x32 | 设置图标（齿轮） | 金色 |
| `icon_save.png` | 32x32 | 保存图标 | 青铜色 |
| `icon_load.png` | 32x32 | 加载图标 | 银色 |
| `icon_dialogue.png` | 32x32 | 对话图标 | 金色 |
| `icon_map.png` | 32x32 | 地图图标 | 青铜色 |

---

## 📋 菜单面板

| 文件 | 尺寸 | 描述 |
|------|------|------|
| `menu_panel.png` | 400x300 | 菜单/设置面板背景 |

**设计特点:**
- 圆角矩形（20px radius）
- 双层边框（金色 + 深色）
- 顶部装饰线

---

## 🎨 UI 主题色板

| 颜色类型 | RGB 值 | 用途 |
|---------|-------|------|
| 主深色 | (45, 40, 55) | 背景主色 |
| 主中色 | (65, 58, 75) | 次级背景 |
| 主浅色 | (85, 76, 98) | 高光 |
| 金色边框 | (200, 175, 100) | 装饰边框 |
| 按钮背景 | (70, 65, 85) | 按钮 |
| 按钮悬停 | (95, 88, 115) | 按钮 hover |
| 进度条背景 | (40, 35, 50) | 进度条底 |
| 进度条填充 | (120, 180, 80) | 进度条高 |
| 信任值低 | (180, 80, 80) | 红色警告 |
| 信任值中 | (200, 160, 60) | 黄色中等 |
| 信任值高 | (80, 180, 100) | 绿色良好 |

---

## 📂 文件位置

```
code/assets/sprites/ui/
├── dialogue_box.png
├── dialogue_box_small.png
├── button_large.png
├── button_large_hover.png
├── button_large_pressed.png
├── button_medium.png
├── button_medium_hover.png
├── button_medium_pressed.png
├── button_small.png
├── button_small_hover.png
├── button_small_pressed.png
├── progress_bar_bg.png
├── progress_fill_low.png
├── progress_fill_mid.png
├── progress_fill_high.png
├── trust_heart.png
├── trust_bar.png
├── icon_settings.png
├── icon_save.png
├── icon_load.png
├── icon_dialogue.png
├── icon_map.png
└── menu_panel.png
```

**总计:** 23 个 UI 素材文件

---

## 🔧 生成工具

**工具位置:** `tools/ui_generator.py`

**使用方法:**
```bash
python3 tools/ui_generator.py
```

**可定制:**
- 调整色板（UI_COLORS）
- 修改按钮尺寸
- 添加新图标
- 调整圆角半径

---

## 📊 任务完成状态

| 任务 ID | 任务名 | 优先级 | 状态 |
|--------|--------|--------|------|
| AR-012 | UI 素材包 | P1 | ✅ Done |

---

## 🎯 下一步

- [ ] 森林场景 (AR-013)
- [ ] 战斗特效 (AR-014)
- [ ] 结局 CG (ME-003)

---

*文档创建：2026-04-02 by AliceBussiness*
