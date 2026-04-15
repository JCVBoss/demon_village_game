#!/usr/bin/env python3
"""
生成星露谷风格的草地纹理 TileSet
使用 PIL/Pillow 创建 64x64 瓦片，带自然变化
"""

from PIL import Image, ImageDraw, ImageFilter
import random
import os

# 配置
TILE_SIZE = 64
GRID_SIZE = 4  # 4x4 = 16 个瓦片
OUTPUT_SIZE = TILE_SIZE * GRID_SIZE  # 256x256

# 草地颜色（暖色调，星露谷风格）
GRASS_COLORS = [
    (76, 153, 76),    # 基础绿
    (89, 169, 89),    # 亮绿
    (64, 128, 64),    # 深绿
    (102, 179, 102),  # 更亮绿
    (70, 140, 70),    # 中间绿
]

def create_grass_tile(variation=0):
    """创建一个 64x64 草地瓦片"""
    img = Image.new('RGBA', (TILE_SIZE, TILE_SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 基础颜色（根据变体选择）
    base_color = GRASS_COLORS[variation % len(GRASS_COLORS)]
    
    # 填充基础色
    draw.rectangle([0, 0, TILE_SIZE-1, TILE_SIZE-1], fill=base_color + (255,))
    
    # 添加噪点/纹理（模拟手绘感）
    pixels = img.load()
    for x in range(TILE_SIZE):
        for y in range(TILE_SIZE):
            # 随机轻微变色
            noise = random.randint(-15, 15)
            r = max(0, min(255, base_color[0] + noise))
            g = max(0, min(255, base_color[1] + noise))
            b = max(0, min(255, base_color[2] + noise))
            # 边缘稍微暗一点
            dist_from_edge = min(x, y, TILE_SIZE-1-x, TILE_SIZE-1-y)
            edge_factor = 1.0 - (dist_from_edge / (TILE_SIZE/2)) * 0.2
            pixels[x, y] = (int(r * edge_factor), int(g * edge_factor), int(b * edge_factor), 255)
    
    # 添加一些草的细节（随机小点）
    for _ in range(random.randint(20, 40)):
        x = random.randint(2, TILE_SIZE-3)
        y = random.randint(2, TILE_SIZE-3)
        detail_color = (
            max(0, min(255, base_color[0] + 20)),
            max(0, min(255, base_color[1] + 30)),
            max(0, min(255, base_color[2] + 20)),
            255
        )
        draw.point((x, y), fill=detail_color)
    
    return img

def create_grass_tileset():
    """创建完整的草地 TileSet 图集（4x4）"""
    output = Image.new('RGBA', (OUTPUT_SIZE, OUTPUT_SIZE), (0, 0, 0, 0))
    
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            variation = row * GRID_SIZE + col
            tile = create_grass_tile(variation)
            output.paste(tile, (col * TILE_SIZE, row * TILE_SIZE))
    
    return output

def create_water_tileset():
    """创建水域 TileSet 图集"""
    output = Image.new('RGBA', (OUTPUT_SIZE, OUTPUT_SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(output)
    
    # 水颜色（蓝色调，带波纹感）
    water_colors = [
        (64, 128, 192),   # 基础蓝
        (76, 140, 204),   # 亮蓝
        (52, 116, 180),   # 深蓝
        (88, 152, 216),   # 更亮蓝
    ]
    
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            x = col * TILE_SIZE
            y = row * TILE_SIZE
            color = water_colors[(row * GRID_SIZE + col) % len(water_colors)]
            
            # 填充水
            draw.rectangle([x, y, x+TILE_SIZE-1, y+TILE_SIZE-1], fill=color + (255,))
            
            # 添加波纹细节（水平线）
            pixels = output.load()
            for wave in range(3):
                wy = y + 15 + wave * 15
                for wx in range(x, x + TILE_SIZE, 4):
                    if random.random() > 0.5:
                        wave_color = (
                            min(255, color[0] + 40),
                            min(255, color[1] + 40),
                            min(255, color[2] + 60),
                            200
                        )
                        pixels[wx, wy] = wave_color
    
    return output

def create_borders_tileset():
    """创建边界 TileSet 图集"""
    output = Image.new('RGBA', (OUTPUT_SIZE, OUTPUT_SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(output)
    
    # 悬崖/边界颜色（岩石灰褐色）
    cliff_colors = [
        (128, 128, 128),  # 基础灰
        (140, 140, 140),  # 亮灰
        (116, 116, 116),  # 暗灰
        (152, 152, 152),  # 更亮灰
    ]
    
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            x = col * TILE_SIZE
            y = row * TILE_SIZE
            color = cliff_colors[(row * GRID_SIZE + col) % len(cliff_colors)]
            
            # 填充边界
            draw.rectangle([x, y, x+TILE_SIZE-1, y+TILE_SIZE-1], fill=color + (255,))
            
            # 添加岩石纹理
            pixels = output.load()
            for _ in range(random.randint(10, 20)):
                rx = x + random.randint(2, TILE_SIZE-3)
                ry = y + random.randint(2, TILE_SIZE-3)
                rock_color = (
                    max(0, min(255, color[0] - 20)),
                    max(0, min(255, color[1] - 20)),
                    max(0, min(255, color[2] - 20)),
                    255
                )
                pixels[rx, ry] = rock_color
    
    return output

def main():
    print("[TileSet Generator] 生成草地纹理...")
    
    # 设置随机种子（可重现）
    random.seed(42)
    
    # 生成草地 TileSet
    grass_tileset = create_grass_tileset()
    
    # 保存
    output_path = os.path.join(os.path.dirname(__file__), 'grass.png')
    grass_tileset.save(output_path, 'PNG')
    print(f"[TileSet Generator] 已保存：{output_path}")
    
    # 生成道路 TileSet
    print("[TileSet Generator] 生成道路纹理...")
    roads_tileset = create_roads_tileset()
    roads_path = os.path.join(os.path.dirname(__file__), 'roads.png')
    roads_tileset.save(roads_path, 'PNG')
    print(f"[TileSet Generator] 已保存：{roads_path}")
    
    # 生成水域 TileSet
    print("[TileSet Generator] 生成水域纹理...")
    water_tileset = create_water_tileset()
    water_path = os.path.join(os.path.dirname(__file__), 'water.png')
    water_tileset.save(water_path, 'PNG')
    print(f"[TileSet Generator] 已保存：{water_path}")
    
    # 生成边界 TileSet
    print("[TileSet Generator] 生成边界纹理...")
    borders_tileset = create_borders_tileset()
    borders_path = os.path.join(os.path.dirname(__file__), 'borders.png')
    borders_tileset.save(borders_path, 'PNG')
    print(f"[TileSet Generator] 已保存：{borders_path}")

def create_roads_tileset():
    """创建道路 TileSet 图集"""
    output = Image.new('RGBA', (OUTPUT_SIZE, OUTPUT_SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(output)
    
    # 泥土路颜色
    dirt_colors = [
        (139, 119, 101),  # 基础泥土色
        (151, 128, 110),  # 亮泥土
        (127, 110, 92),   # 暗泥土
        (163, 139, 119),  # 更亮泥土
    ]
    
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            x = col * TILE_SIZE
            y = row * TILE_SIZE
            color = dirt_colors[(row * GRID_SIZE + col) % len(dirt_colors)]
            
            # 填充道路
            draw.rectangle([x, y, x+TILE_SIZE-1, y+TILE_SIZE-1], fill=color + (255,))
            
            # 添加石子细节
            pixels = output.load()
            for _ in range(random.randint(15, 30)):
                px = x + random.randint(2, TILE_SIZE-3)
                py = y + random.randint(2, TILE_SIZE-3)
                stone_color = (
                    max(0, min(255, color[0] + 30)),
                    max(0, min(255, color[1] + 20)),
                    max(0, min(255, color[2] + 10)),
                    255
                )
                pixels[px, py] = stone_color
    
    return output

if __name__ == '__main__':
    main()
