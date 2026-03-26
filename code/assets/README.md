# 像素画生成工具使用说明

## 🎨 工具概述

这是一个基于 Python Pillow 的像素画生成工具，可以程序化生成像素风格的游戏美术资源。

**工具位置**: `tools/pixel_art_generator.py`

## ✅ 已生成的资源

### 陈默（主角）立绘
| 文件 | 尺寸 | 描述 |
|------|------|------|
| `chenmo_normal.png` | 64x64 | 普通表情 |
| `chenmo_happy.png` | 64x64 | 开心表情 |
| `chenmo_sad.png` | 64x64 | 悲伤表情 |
| `chenmo_surprised.png` | 64x64 | 惊讶表情 |
| `chenmo_angry.png` | 64x64 | 生气表情 |
| `chenmo_spritesheet.png` | 320x64 | 表情合集（用于动画） |

### 色卡
| 文件 | 描述 |
|------|------|
| `color_palette.png` | 暮色村主题色板（皮肤/头发/衣服/背景） |

## 🛠️ 使用方法

### 生成角色立绘
```bash
python3 tools/pixel_art_generator.py
```

### 自定义角色
编辑 `pixel_art_generator.py` 中的角色定义：

```python
# 添加新角色
NEW_CHARACTER = {
    'name': '角色名',
    'size': (64, 64),
    'colors': {
        'hair': 'hair_color_key',
        'skin': 'skin_color_key',
        'cloth': 'cloth_color_key',
    },
}
```

### 扩展功能
可以添加：
- 更多角色设计
- 场景背景生成
- UI 元素生成
- 动画帧序列
- 更大尺寸的立绘（128x128, 256x256）

## 📋 当前色板

```python
COLOR_PALETTE = {
    # 皮肤色
    'skin_light': (255, 224, 189),
    'skin_medium': (234, 194, 155),
    'skin_dark': (210, 160, 120),
    
    # 头发颜色
    'hair_black': (30, 25, 20),
    'hair_brown': (80, 50, 30),
    'hair_blonde': (200, 170, 100),
    'hair_gray': (128, 128, 128),
    
    # 衣服颜色
    'cloth_white': (240, 240, 240),
    'cloth_blue': (60, 90, 140),
    'cloth_red': (140, 50, 50),
    'cloth_green': (60, 100, 60),
    'cloth_brown': (100, 70, 40),
    'cloth_black': (40, 35, 30),
    
    # 背景/环境
    'bg_dark': (30, 25, 35),
    'bg_twilight': (60, 50, 80),
    'highlight': (200, 180, 100),
    
    # 轮廓
    'outline': (20, 15, 25),
}
```

## 📝 下一步计划

### 待生成的角色（9 位村民）
- [ ] 夜芽（女巫）
- [ ] 铁臂（铁匠）
- [ ] 草语（药师）
- [ ] 老约翰（村长）
- [ ] 小铃（酒馆老板女儿）
- [ ] 影刃（神秘旅人）
- [ ] 麦穗（农夫）
- [ ] 书虫（学者）
- [ ] 石心（守卫）

### 待生成的场景
- [ ] 村庄全景（白天/黄昏/夜晚）
- [ ] 酒馆内部
- [ ] 铁匠铺
- [ ] 药房
- [ ] 村长家
- [ ] 村口道路

### 待生成的 UI 元素
- [ ] 对话框背景
- [ ] 选项按钮
- [ ] 信任度指示器
- [ ] 日期/时间显示
- [ ] 菜单图标

## 🎯 输出规格

| 资源类型 | 尺寸 | 格式 | 说明 |
|----------|------|------|------|
| 角色立绘 | 64x64 / 128x128 | PNG | 支持透明背景 |
| 场景背景 | 1280x720 | PNG | 全屏背景 |
| UI 元素 | 可变 | PNG | 支持 9-slice 缩放 |
| Sprite Sheet | 可变 | PNG | 动画帧序列 |

## 💡 提示

- 当前是基础版本，可以扩展更精细的像素画算法
- 可以导入 Aseprite 工程文件进行二次编辑
- 支持批量生成和色板替换
- 可以添加随机变异功能生成 NPC 变体

---
*最后更新：2026-03-26 by AliceBussiness*
