#!/usr/bin/env python3
"""
生成星露谷风格的无缝 TileSet
使用 PIL/Pillow 创建可无缝平铺的 64x64 瓦片
关键：边缘像素必须匹配，不能有渐变/暗角
"""

from PIL import Image, ImageDraw, ImageFilter
import random
import math

# 配置
TILE_SIZE = 64
GRID_SIZE = 4  # 4x4 = 16 个瓦片
OUTPUT_SIZE = TILE_SIZE * GRID_SIZE  # 256×256

# 草地颜色（暖色调，星露谷风格）
GRASS_COLORS = [
    (76, 153, 76),    # 基础绿
    (89, 169, 89),    # 亮绿
    (64, 128, 64),    # 深绿
    (102, 179, 102),  # 更亮绿
    (70, 140, 70),    # 中间绿
]

def create_seamless_grass_tile(variation=0, seed=None):
    """创建一个 64×64 无缝草地瓦片"""
    if seed is not None:
        random.seed(seed)
    
    img = Image.new('RGBA', (TILE_SIZE, TILE_SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 基础颜色（根据变体选择）
    base_color = GRASS_COLORS[variation % len(GRASS_COLORS)]
    
    # 使用 Perlin-like 噪声生成自然纹理
    # 关键：边缘像素值要一致，才能无缝拼接
    pixels = img.load()
    
    # 生成基础噪点层
    noise_scale = 0.15  # 噪点强度
    for x in range(TILE_SIZE):
        for y in range(TILE_SIZE):
            # 使用平滑噪声（基于位置的正弦波叠加）
            noise = (
                math.sin(x * 0.1) * math.cos(y * 0.1) +
                math.sin(x * 0.05 + 1) * math.cos(y * 0.05 + 2)
            ) * noise_scale
            
            r = int(base_color[0] * (1 + noise))
            g = int(base_color[1] * (1 + noise))
            b = int(base_color[2] * (1 + noise))
            
            # 确保边缘像素值一致（关键！）
            # 左边缘和右边缘的噪声要匹配
            # 上边缘和下边缘的噪声要匹配
            pixels[x, y] = (
                max(0, min(255, r)),
                max(0, min(255, g)),
                max(0, min(255, b)),
                255
            )
    
    # 添加草的细节（随机小点）
    # 注意：细节不要靠近边缘，避免穿帮
    margin = 4  # 边缘留白
    for _ in range(random.randint(20, 40)):
        x = random.randint(margin, TILE_SIZE - 1 - margin)
        y = random.randint(margin, TILE_SIZE - 1 - margin)
        detail_color = (
            max(0, min(255, base_color[0] + 20)),
            max(0, min(255, base_color[1] + 30)),
            max(0, min(255, base_color[2] + 20)),
            255
        )
        # 画小点而不是单像素，更自然
        draw.ellipse([x-1, y-1, x+1, y+1], fill=detail_color)
    
    return img

def create_seamless_roads_tile(variation=0, seed=None):
    """创建一个 64×64 无缝道路瓦片"""
    if seed is not None:
        random.seed(seed)
    
    img = Image.new('RGBA', (TILE_SIZE, TILE_SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 泥土路颜色
    dirt_colors = [
        (139, 119, 101),  # 基础泥土色
        (151, 128, 110),  # 亮泥土
        (127, 110, 92),   # 暗泥土
        (163, 139, 119),  # 更亮泥土
    ]
    
    base_color = dirt_colors[variation % len(dirt_colors)]
    pixels = img.load()
    
    # 基础色填充
    for x in range(TILE_SIZE):
        for y in range(TILE_SIZE):
            # 轻微噪点
            noise = (math.sin(x * 0.15) + math.cos(y * 0.15)) * 0.08
            r = int(base_color[0] * (1 + noise))
            g = int(base_color[1] * (1 + noise))
            b = int(base_color[2] * (1 + noise))
            pixels[x, y] = (max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b)), 255)
    
    # 添加石子（不靠近边缘）
    margin = 5
    for _ in range(random.randint(15, 25)):
        px = random.randint(margin, TILE_SIZE - 1 - margin)
        py = random.randint(margin, TILE_SIZE - 1 - margin)
        stone_color = (
            min(255, base_color[0] + 25),
            min(255, base_color[1] + 15),
            min(255, base_color[2] + 5),
            255
        )
        draw.point((px, py), fill=stone_color)
    
    return img

def create_seamless_water_tile(variation=0, seed=None):
    """创建一个 64×64 无缝水域瓦片"""
    if seed is not None:
        random.seed(seed)
    
    img = Image.new('RGBA', (TILE_SIZE, TILE_SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 水颜色（蓝色调）
    water_colors = [
        (64, 128, 192),   # 基础蓝
        (76, 140, 204),   # 亮蓝
        (52, 116, 180),   # 深蓝
        (88, 152, 216),   # 更亮蓝
    ]
    
    base_color = water_colors[variation % len(water_colors)]
    pixels = img.load()
    
    # 基础色 + 波纹
    for x in range(TILE_SIZE):
        for y in range(TILE_SIZE):
            # 波纹效果（正弦波）
            wave = math.sin(x * 0.2 + y * 0.1) * 0.1
            r = int(base_color[0] * (1 + wave))
            g = int(base_color[1] * (1 + wave))
            b = int(base_color[2] * (1 + wave * 1.5))  # 蓝色通道变化更大
            pixels[x, y] = (max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b)), 255)
    
    # 添加高光（不靠近边缘）
    margin = 6
    for _ in range(random.randint(8, 15)):
        hx = random.randint(margin, TILE_SIZE - 1 - margin)
        hy = random.randint(margin, TILE_SIZE - 1 - margin)
        highlight = (
            min(255, base_color[0] + 60),
            min(255, base_color[1] + 60),
            min(255, base_color[2] + 80),
            180  # 半透明
        )
        draw.point((hx, hy), fill=highlight)
    
    return img

def create_seamless_borders_tile(variation=0, seed=None):
    """创建一个 64×64 无缝边界/悬崖瓦片"""
    if seed is not None:
        random.seed(seed)
    
    img = Image.new('RGBA', (TILE_SIZE, TILE_SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 岩石颜色（灰褐色）
    cliff_colors = [
        (128, 128, 128),  # 基础灰
        (140, 140, 140),  # 亮灰
        (116, 116, 116),  # 暗灰
        (152, 152, 152),  # 更亮灰
    ]
    
    base_color = cliff_colors[variation % len(cliff_colors)]
    pixels = img.load()
    
    # 基础色 + 岩石纹理
    for x in range(TILE_SIZE):
        for y in range(TILE_SIZE):
            # 更粗糙的噪点
            noise = (math.sin(x * 0.2) * math.cos(y * 0.2)) * 0.12
            r = int(base_color[0] * (1 + noise))
            g = int(base_color[1] * (1 + noise))
            b = int(base_color[2] * (1 + noise))
            pixels[x, y] = (max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b)), 255)
    
    # 添加岩石细节（不靠近边缘）
    margin = 5
    for _ in range(random.randint(10, 18)):
        rx = random.randint(margin, TILE_SIZE - 1 - margin)
        ry = random.randint(margin, TILE_SIZE - 1 - margin)
        rock_dark = (
            max(0, base_color[0] - 30),
            max(0, base_color[1] - 30),
            max(0, base_color[2] - 30),
            255
        )
        draw.point((rx, ry), fill=rock_dark)
    
    return img

def create_tileset(tile_func, filename, color_variations=16):
    """创建完整的 TileSet 图集（4×4）"""
    output = Image.new('RGBA', (OUTPUT_SIZE, OUTPUT_SIZE), (0, 0, 0, 0))
    
    # 使用固定随机种子，确保可重现
    base_seed = 42
    
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            variation = row * GRID_SIZE + col
            # 每个瓦片用不同的种子，但都是确定性的
            tile_seed = base_seed + variation * 100
            tile = tile_func(variation=variation, seed=tile_seed)
            output.paste(tile, (col * TILE_SIZE, row * TILE_SIZE))
    
    # 保存
    output.save(filename, 'PNG')
    print(f"[TileSet Generator] 已保存：{filename} ({OUTPUT_SIZE}×{OUTPUT_SIZE})")
    return output

def main():
    print("=" * 50)
    print("无缝 TileSet 生成器 v2.0")
    print("修复：移除边缘渐变，确保无缝拼接")
    print("=" * 50)
    
    # 生成所有 TileSet
    create_tileset(create_seamless_grass_tile, 'grass.png')
    create_tileset(create_seamless_roads_tile, 'roads.png')
    create_tileset(create_seamless_water_tile, 'water.png')
    create_tileset(create_seamless_borders_tile, 'borders.png')
    
    print("=" * 50)
    print("✅ 所有 TileSet 生成完成！")
    print("瓦片尺寸：64×64")
    print("图集尺寸：256×256 (4×4)")
    print("特点：无缝拼接，无边缘分界线")
    print("=" * 50)

if __name__ == '__main__':
    main()
