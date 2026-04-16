# 暮色村美术资源使用指南

_最后更新：2026-04-16_

---

## 📁 目录结构

```
code/assets/sprites/
├── buildings/           # 建筑 Sprite（独立，Y-sorting）
│   ├── building_blacksmith.png      # 铁匠铺 (256×192)
│   ├── building_church.png          # 教堂 (320×256)
│   ├── building_tavern.png          # 酒馆 (320×192)
│   ├── building_merchant.png        # 商人行会 (256×192)
│   ├── building_school.png          # 学校 (192×192)
│   ├── building_chenmo_hut.png      # 陈默小屋 (192×128)
│   ├── building_baizhi_garden.png   # 白芷药园 (256×192)
│   ├── building_guard_post.png      # 守卫营房 (256×192)
│   ├── building_abandoned_warehouse.png  # 废弃仓库 (192×128)
│   └── building_ying_home.png       # 影的住所 (192×128)
│
├── decorations/         # 原有装饰物（树木/石头/花朵等）
│   ├── tree_1/2/3.png   # 临时树木
│   ├── flower_*.png     # 花朵
│   ├── rock_*.png       # 石头
│   └── bush.png         # 灌木
│
├── decorations_new/     # 新增装饰物（伪 3D 风格）
│   ├── tree_pine.png    # 松树 (64×128)
│   ├── tree_oak.png     # 橡树 (64×96)
│   ├── tree_fruit.png   # 果树 (64×96)
│   ├── street_light.png # 路灯 (32×96)
│   ├── flower_bed.png   # 花坛 (64×64)
│   ├── bench.png        # 长椅 (96×32)
│   ├── well.png         # 水井 (64×96)
│   └── barrel.png       # 木桶 (32×32)
│
├── tilesets/            # 地面纹理 TileSet
│   ├── grass.png        # 草地 (256×256, 16 变体)
│   ├── roads.png        # 道路 (256×256, 16 变体)
│   ├── water.png        # 水域 (256×256, 16 变体)
│   ├── borders.png      # 边界 (256×256, 16 变体)
│   └── buildings.png    # 建筑瓦片（旧，待替换）
│
├── characters/          # 角色 Sprite
│   ├── player/          # 玩家
│   ├── [villager]_*.png # 村民（10 位）
│   └── CHARACTERS_MANIFEST.md
│
├── ui/                  # UI 元素
│   ├── button_*.png     # 按钮
│   ├── dialogue_box.png # 对话框
│   └── icon_*.png       # 图标
│
└── backgrounds/         # 背景图
    └── [场景背景].png
```

---

## 🏠 建筑 Sprite 使用

### 渲染模式

建筑使用 **Y-sorting 独立 Sprite** 渲染：
- 每栋建筑是一个 `Sprite2D` 节点
- 放在 `YSortRoot/Buildings` 容器下
- Godot 自动按 Y 坐标排序（遮挡关系）

### Godot 集成示例

```gdscript
# Village.gd
func spawn_building(building_id: String, pos: Vector2) -> void:
    var sprite = Sprite2D.new()
    sprite.name = building_id
    sprite.position = pos
    sprite.texture = load(f"res://assets/sprites/buildings/building_{building_id}.png")
    buildings_container.add_child(sprite)  # buildings_container 在 YSortRoot 下
```

### 建筑位置配置

```gdscript
# 村民位置 = 建筑位置（村民站在建筑门口）
const VILLAGER_POSITIONS: Dictionary = {
    "chenmo": Vector2(352, 352),     # 陈默小屋
    "leishu": Vector2(352, 672),     # 铁匠铺
    "jinling": Vector2(1440, 800),   # 商人行会
    # ... 其他村民
}

# 建筑位置 = 村民位置 - 偏移（建筑底部对齐）
const BUILDING_OFFSETS: Dictionary = {
    "chenmo_hut": Vector2(0, -64),   # 小屋矮，偏移小
    "blacksmith": Vector2(0, -96),   # 铁匠铺高，偏移大
    # ... 其他建筑
}
```

### 建筑尺寸参考

| 建筑 | 尺寸 | Y 偏移建议 |
|------|------|-----------|
| 教堂 | 320×256 | -128 |
| 酒馆 | 320×192 | -96 |
| 铁匠铺 | 256×192 | -96 |
| 学校 | 192×192 | -96 |
| 小屋 | 192×128 | -64 |

---

## 🌳 装饰物 Sprite 使用

### 分类

| 类型 | 数量 | 尺寸 | 碰撞 |
|------|------|------|------|
| 松树 | 28 | 64×128 | 是 |
| 橡树 | 6 | 64×96 | 是 |
| 果树 | 4 | 64×96 | 是 |
| 路灯 | 8 | 32×96 | 是 |
| 花坛 | 4 | 64×64 | 是 |
| 长椅 | 3 | 96×32 | 是（可交互） |
| 水井 | 1 | 64×96 | 是 |
| 木桶 | 10 | 32×32 | 部分 |

### Godot 集成示例

```gdscript
# 生成装饰物（带碰撞）
func spawn_decoration(deco_id: String, pos: Vector2, has_collision: bool) -> void:
    if has_collision:
        var body = StaticBody2D.new()
        var sprite = Sprite2D.new()
        sprite.texture = load(f"res://assets/sprites/decorations_new/{deco_id}.png")
        body.add_child(sprite)
        
        # 添加碰撞形状
        var collision = CollisionShape2D.new()
        var shape = RectangleShape2D.new()
        shape.size = Vector2(32, 32)  # 根据实际尺寸调整
        collision.shape = shape
        body.add_child(collision)
        
        objects_container.add_child(body)
    else:
        var sprite = Sprite2D.new()
        sprite.texture = load(f"res://assets/sprites/decorations_new/{deco_id}.png")
        sprite.position = pos
        objects_container.add_child(sprite)
```

---

## 🎨 风格说明

### 伪 3D 斜角视角

- **视角**: 45°斜角俯视
- **结构**: 屋顶斜面 + 墙壁侧面 + 正面
- **遮挡**: Y-sorting 自动处理（底部 Y 坐标决定前后）

### 色彩主题

| 建筑类型 | 墙壁色 | 屋顶色 | 氛围 |
|----------|--------|--------|------|
| 铁匠铺 | 棕色 | 红色 | 温暖、锻造 |
| 教堂 | 白色 | 棕色 | 神圣、庄严 |
| 酒馆 | 深木色 | 红棕色 | 温馨、热闹 |
| 学校 | 米色 | 灰色 | 朴素、安静 |
| 小屋 | 深棕色 | 棕色 | 简陋、隐蔽 |
| 影的住所 | 暗紫色 | 暗青色 | 神秘、阴暗 |

---

## 🔄 临时资源说明

### 当前状态

- ✅ **地面纹理**: 程序生成（v2.0 无缝版本）
- ✅ **建筑 Sprite**: 程序生成（临时占位）
- ✅ **装饰物**: 程序生成（临时占位）+ 原有资源

### 后续计划

等美工到位后替换：
1. 建筑 → 手绘精品（保留尺寸和视角）
2. 装饰物 → 统一风格细化
3. 地面纹理 → 可选保留或重做

---

## 📝 生成工具

### 地面纹理生成
```bash
cd tools
python3 generate_tilesets.py
# 输出：grass.png, roads.png, water.png, borders.png
```

### 建筑和装饰物生成
```bash
cd tools
python3 generate_buildings_and_decorations.py
# 输出：buildings/*.png, decorations_new/*.png
```

---

_文档持续更新中..._
