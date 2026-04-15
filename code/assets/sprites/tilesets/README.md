# TileSet 纹理图集

_程序生成的星露谷风格地面纹理_

---

## 📦 文件清单

| 文件 | 尺寸 | 内容 |
|------|------|------|
| `grass.png` | 256×256 | 草地纹理（4×4 瓦片，16 种变体） |
| `roads.png` | 256×256 | 泥土路纹理（4×4 瓦片，16 种变体） |
| `water.png` | 256×256 | 水域纹理（4×4 瓦片，16 种变体） |
| `borders.png` | 256×256 | 边界/悬崖纹理（4×4 瓦片，16 种变体） |
| `buildings.png` | 64×64 | 建筑瓦片（待替换为独立 Sprite） |

---

## 🎨 风格说明

- **风格**: 星露谷风格手绘质感
- **色调**: 暖色调（体现"最后的光明"主题）
- **瓦片尺寸**: 64×64 像素
- **生成方式**: 程序生成（带噪点和细节）

---

## 🛠️ 生成工具

使用 `tools/generate_tilesets.py` 重新生成：

```bash
cd /home/ubuntu/demon_village_game
python3 tools/generate_tilesets.py
```

**随机种子**: 42（可重现）

---

## 📝 使用说明

### Godot 集成

TileSet 已在 `VillageTileset.tres` 中配置：

```gdscript
# VillageTileset.tres 自动加载这些纹理
# TileMapLayer 使用这些纹理铺设地面
```

### 随机铺设

Village.gd 已支持随机变体铺设：

```gdscript
func _generate_ground_layer() -> void:
    for x in range(MAP_WIDTH):
        for y in range(MAP_HEIGHT):
            var tile_coords = Vector2i(randi() % 4, 0)
            ground_layer.set_cell(Vector2i(x, y), SOURCE_GRASS, tile_coords)
```

---

## 📄 许可

- **生成工具**: 项目内部使用
- **纹理输出**: 可自由用于项目
- **灵感来源**: 星露谷物语风格

---

_最后更新：2026-04-15_
