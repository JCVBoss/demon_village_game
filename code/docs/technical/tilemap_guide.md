# TileMap 地图系统技术文档

## 概述

本文档描述魔王城下的最后村庄的 TileMap 地图系统实现。

## 瓦片规格

| 属性 | 数值 |
|------|------|
| 基础瓦片尺寸 | 64x64 像素 |
| 地图大小（村庄） | 30x25 瓦片 (1920x1600 像素) |
| 地图大小（森林） | 40x30 瓦片 (2560x1920 像素) |

## 图层结构

| 图层 | Z-Index | 用途 | 碰撞 |
|------|---------|------|------|
| Ground | -10 | 地面（草地、泥土） | 无 |
| Water | -8 | 水体 | 有 |
| Roads | -5 | 道路 | 无 |
| Buildings | 0 | 建筑、墙壁 | 有 |
| Decorations | 5 | 装饰物（树木、花草） | 部分有 |
| Borders | 10 | 边界、不可见碰撞 | 有 |

## TileSet 资源

### VillageTileset.tres

整合的村庄 TileSet，包含以下图集源：

- **Source 0 (Grass)**: 草地瓦片
- **Source 1 (Roads)**: 道路瓦片
- **Source 2 (Buildings)**: 建筑瓦片（含碰撞）
- **Source 3 (Water)**: 水体瓦片（含碰撞）
- **Source 4 (Borders)**: 边界瓦片（含碰撞）

### 碰撞配置

碰撞层设置：
- Layer 1: 玩家
- Layer 2: 障碍物（建筑、水体、边界）

玩家 `collision_mask = 2`，障碍物 `collision_layer = 2`。

## 地图配置文件

位置: `resources/maps/village_map_config.json`

```json
{
    "map_name": "暮色村",
    "tile_size": 64,
    "map_width": 30,
    "map_height": 25,
    "buildings": [...],
    "npc_positions": {...},
    "transitions": [...]
}
```

## TileMapManager API

### 核心方法

```gdscript
# 加载地图配置
func load_map_config(path: String) -> bool

# 生成默认地图
func generate_default_map() -> void

# 放置建筑
func place_building(building_id: String, pos: Vector2i, size: Vector2i, has_collision: bool = true) -> void
```

### 坐标转换

```gdscript
# 瓦片坐标 -> 像素坐标
func tile_to_pixel(tile_pos: Vector2i) -> Vector2

# 像素坐标 -> 瓦片坐标
func pixel_to_tile(pixel_pos: Vector2) -> Vector2i
```

### 查询方法

```gdscript
# 获取地图像素尺寸
func get_pixel_size() -> Vector2

# 检查瓦片坐标是否有效
func is_valid_tile(tile_pos: Vector2i) -> bool

# 获取地图边界
func get_map_bounds() -> Rect2
```

## 场景结构

```
VillageMap (Node2D)
├── Ground (TileMapLayer, z=-10)
├── Water (TileMapLayer, z=-8)
├── Roads (TileMapLayer, z=-5)
├── Buildings (TileMapLayer, z=0)
├── Decorations (TileMapLayer, z=5)
├── Borders (TileMapLayer, z=10)
└── MapBounds (StaticBody2D)
    └── CollisionShape2D
```

## 使用示例

### 在场景中使用

```gdscript
# 预加载地图场景
const VillageMap = preload("res://scenes/locations/VillageMap.tscn")

func _ready():
    var map = VillageMap.instantiate()
    add_child(map)
```

### 访问地图管理器

```gdscript
@onready var tilemap_manager: TileMapManager = $VillageMap

func _on_map_loaded(map_name: String):
    print("地图加载完成: ", map_name)
    var bounds = tilemap_manager.get_map_bounds()
```

## 扩展说明

### 添加新建筑

1. 在地图配置 JSON 中添加建筑定义
2. 使用 `place_building()` 方法放置建筑瓦片
3. 配置碰撞和交互点

### 区域切换

地图配置中的 `transitions` 数组定义了区域切换点：

```json
{
    "id": "to_forest",
    "target_scene": "ForestMap.tscn",
    "position": {"x": 15, "y": 24},
    "trigger_area": {"x": 960, "y": 1500, "width": 256, "height": 64}
}
```

## 相关文件

- `resources/tilesets/VillageTileset.tres` - 村庄 TileSet
- `resources/maps/village_map_config.json` - 地图配置
- `scripts/core/TileMapManager.gd` - 地图管理器
- `scenes/locations/VillageMap.tscn` - 地图场景

---

**文档版本**: 1.0
**创建日期**: 2026-04-07
**相关 Issue**: #68 CS-006: TileMap 地图系统