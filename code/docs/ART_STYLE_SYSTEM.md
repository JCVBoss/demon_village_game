# 美术风格切换系统 - 使用文档

## 概述

这个系统允许通过简单替换资源目录来切换游戏的美术风格。

## 目录结构

```
code/assets/
├── styles/
│   ├── default/              # 默认风格
│   │   ├── manifest.json     # 风格清单文件
│   │   ├── tilesets/         # 瓦片集图片
│   │   │   ├── grass.png
│   │   │   ├── roads.png
│   │   │   ├── water.png
│   │   │   └── borders.png
│   │   ├── buildings/        # 建筑图片
│   │   ├── decorations/      # 装饰物图片
│   │   ├── characters/       # 角色图片
│   │   ├── ui/               # UI 图片
│   │   └── backgrounds/      # 背景图片
│   └── pixel_art/            # 其他风格（示例）
│       └── ...
└── common/                   # 公共资源（不随风格变化）
```

## 快速开始

### 1. 添加新风格

1. 在 `code/assets/styles/` 下创建新文件夹，例如 `pixel_art`
2. 复制 `default/manifest.json` 到新文件夹
3. 修改清单文件中的风格信息
4. 放入你的美术资源
5. 在代码中调用 `ArtStyleManager.switch_style("pixel_art")`

### 2. 在代码中使用

```gdscript
# 获取资源路径
var building_path = ArtStyleManager.get_resource_path("building", "blacksmith")

# 获取资源完整数据（包含尺寸、偏移）
var building_data = ArtStyleManager.get_resource_data("building", "blacksmith")
var texture_path = building_data["full_path"]
var size = Vector2(building_data["size"][0], building_data["size"][1])
var offset = Vector2(building_data["offset"][0], building_data["offset"][1])

# 切换风格
ArtStyleManager.switch_style("pixel_art")

# 获取可用风格列表
var styles = ArtStyleManager.get_available_styles()
```

### 3. 在 Village 场景中使用

在 `Village.gd` 的 `_ready` 函数中添加：

```gdscript
func _ready() -> void:
	# ... 现有代码 ...
	
	# 生成建筑和装饰物（使用 ArtStyleManager）
	ArtStyleIntegration.spawn_buildings_from_style(buildings_container)
	ArtStyleIntegration.spawn_decorations_from_style(objects_container)
```

## Manifest.json 格式

```json
{
  "name": "风格名称",
  "version": "1.0",
  "author": "作者",
  "description": "描述",
  "tile_size": 64,
  
  "tilesets": {
    "grass": {
      "path": "tilesets/grass.png",
      "columns": 4,
      "rows": 1
    }
  },
  
  "buildings": {
    "blacksmith": {
      "path": "buildings/building_blacksmith.png",
      "size": [256, 192],
      "offset": [0, -96]
    }
  },
  
  "decorations": {
    "tree_pine": {
      "path": "decorations/tree_pine.png",
      "size": [64, 128],
      "has_collision": true
    }
  },
  
  "characters": {
    "player": {
      "path": "characters/player.png",
      "size": [64, 64],
      "frames": 4
    }
  },
  
  "ui": {
    "dialogue_box": "ui/dialogue_box.png"
  },
  
  "backgrounds": {
    "village": "backgrounds/village_background.png"
  }
}
```

## 资源类型

- `tileset`: 瓦片集
- `building`: 建筑
- `decoration`: 装饰物
- `character`: 角色
- `ui`: UI 元素
- `background`: 背景

## 资源规格

### 瓦片集

- 格式: PNG（支持透明）
- 尺寸: 256x256 像素（4x4 瓦片）
- 瓦片大小: 64x64 像素

### 建筑

- 格式: PNG（支持透明）
- 基准点: 图片底部中心
- 尺寸建议:
  - 小型: 192x128
  - 中型: 256x192
  - 大型: 320x256

### 装饰物

- 格式: PNG（支持透明）
- 基准点: 图片底部中心

### 角色

- 格式: PNG（支持透明）
- 尺寸: 64x64 像素（单帧）或 256x64 像素（4 帧动画）

## API 参考

### ArtStyleManager

#### `get_available_styles() -> Array`
获取可用的风格列表

#### `load_style_manifest(style_name: String) -> Dictionary`
加载风格清单文件

#### `switch_style(style_name: String) -> bool`
切换美术风格

#### `is_style_available(style_name: String) -> bool`
检查风格是否可用

#### `get_resource_path(resource_type: String, resource_name: String) -> String`
获取资源的完整路径

#### `get_resource_data(resource_type: String, resource_name: String) -> Dictionary`
获取资源的完整数据

#### `get_tile_size() -> int`
获取当前风格的瓦片大小

### ArtStyleIntegration

#### `spawn_buildings_from_style(buildings_container: Node2D) -> void`
从当前风格生成所有建筑

#### `spawn_decorations_from_style(objects_container: Node2D) -> void`
从当前风格生成示例装饰物

## 注意事项

1. 如果某个风格缺少某个资源，系统会自动从 `default` 风格获取
2. 资源文件名建议使用小写字母和下划线
3. 确保在 Godot 项目设置中将新资源文件夹加入到导出列表中
4. 切换风格时会发出 `style_changed` 信号，可以连接这个信号来刷新界面

## 占位符资源

当前 `characters/`、`ui/`、`backgrounds/` 目录下的资源是占位符，替换为真实资源即可。

标记为 `"placeholder": true` 的资源表示这是占位符。
