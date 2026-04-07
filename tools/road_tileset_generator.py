#!/usr/bin/env python3
"""
道路 TileSet 生成器
生成 64x64 像素的像素风格道路瓦片集
"""

from PIL import Image, ImageDraw
import os

# 配置
TILE_SIZE = 64
OUTPUT_DIR = "code/assets/sprites/tilesets"
PALETTE = {
    'dirt_dark': (80, 50, 30),        # 深泥土
    'dirt_mid': (101, 67, 33),        # 中泥土
    'dirt_light': (139, 90, 43),      # 浅泥土
    'stone_gray': (128, 128, 128),    # 石板灰
    'grass_mid': (60, 179, 60),       # 草地绿（边缘用）
}

def create_base_road_tile(variation=0):
    """创建基础道路瓦片（内部瓦片）"""
    img = Image.new('RGBA', (TILE_SIZE, TILE_SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 填充泥土底色
    base_color = PALETTE['dirt_mid']
    draw.rectangle([0, 0, TILE_SIZE-1, TILE_SIZE-1], fill=base_color)
    
    # 添加石子装饰
    for i in range(12):
        sx = (variation * 17 + i * 13) % (TILE_SIZE - 6) + 3
        sy = (variation * 23 + i * 11) % (TILE_SIZE - 6) + 3
        stone_size = 2 + (i % 3)
        stone_color = PALETTE['dirt_light'] if i % 2 == 0 else PALETTE['dirt_dark']
        draw.ellipse([sx, sy, sx+stone_size, sy+stone_size], fill=stone_color)
    
    # 添加车辙痕迹
    for offset in [16, 40]:
        for i in range(TILE_SIZE // 4):
            tx = offset + (i % 4) - 2
            ty = i * 4
            if 0 <= tx < TILE_SIZE and 0 <= ty < TILE_SIZE:
                draw.point((tx, ty), fill=PALETTE['dirt_dark'])
    
    return img

def create_road_edge_tile(direction):
    """
    创建道路边缘瓦片
    direction: 0=上，1=右，2=下，3=左
    """
    img = Image.new('RGBA', (TILE_SIZE, TILE_SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    dirt_color = PALETTE['dirt_mid']
    grass_color = PALETTE['grass_mid']
    
    if direction == 0:  # 上边缘 - 道路在下方
        # 上半部分草地
        draw.rectangle([0, 0, TILE_SIZE-1, TILE_SIZE//2-4], fill=grass_color)
        # 下半部分道路
        draw.rectangle([0, TILE_SIZE//2, TILE_SIZE-1, TILE_SIZE-1], fill=dirt_color)
        # 过渡带 - 草地边缘
        for i in range(16):
            ex = i * 4
            ey = TILE_SIZE//2 - 4 + (i % 3)
            draw.rectangle([ex, ey, ex+3, ey+2], fill=grass_color)
        # 道路石子
        for i in range(8):
            sx = (i * 17) % TILE_SIZE
            sy = TILE_SIZE//2 + 8 + (i % 4) * 4
            draw.ellipse([sx, sy, sx+2, sy+2], fill=PALETTE['dirt_light'])
    
    elif direction == 2:  # 下边缘 - 道路在上方
        # 上半部分道路
        draw.rectangle([0, 0, TILE_SIZE-1, TILE_SIZE//2-4], fill=dirt_color)
        # 下半部分草地
        draw.rectangle([0, TILE_SIZE//2, TILE_SIZE-1, TILE_SIZE-1], fill=grass_color)
        # 过渡带 - 草地边缘
        for i in range(16):
            ex = i * 4
            ey = TILE_SIZE//2 - 2 + (i % 3)
            draw.rectangle([ex, ey, ex+3, ey+2], fill=grass_color)
        # 道路石子
        for i in range(8):
            sx = (i * 17) % TILE_SIZE
            sy = 8 + (i % 4) * 4
            draw.ellipse([sx, sy, sx+2, sy+2], fill=PALETTE['dirt_light'])
    
    elif direction == 1:  # 右边缘 - 道路在左方
        # 左半部分道路
        draw.rectangle([0, 0, TILE_SIZE//2-4, TILE_SIZE-1], fill=dirt_color)
        # 右半部分草地
        draw.rectangle([TILE_SIZE//2, 0, TILE_SIZE-1, TILE_SIZE-1], fill=grass_color)
        # 过渡带
        for i in range(16):
            ex = TILE_SIZE//2 - 4 + (i % 3)
            ey = i * 4
            draw.rectangle([ex, ey, ex+2, ey+3], fill=grass_color)
    
    elif direction == 3:  # 左边缘 - 道路在右方
        # 左半部分草地
        draw.rectangle([0, 0, TILE_SIZE//2-4, TILE_SIZE-1], fill=grass_color)
        # 右半部分道路
        draw.rectangle([TILE_SIZE//2, 0, TILE_SIZE-1, TILE_SIZE-1], fill=dirt_color)
        # 过渡带
        for i in range(16):
            ex = TILE_SIZE//2 - 2 + (i % 3)
            ey = i * 4
            draw.rectangle([ex, ey, ex+2, ey+3], fill=grass_color)
    
    return img

def create_road_corner_tile(corner_type):
    """
    创建道路角落瓦片
    corner_type: 0=左上，1=右上，2=左下，3=右下
    """
    img = Image.new('RGBA', (TILE_SIZE, TILE_SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    dirt_color = PALETTE['dirt_mid']
    grass_color = PALETTE['grass_mid']
    
    if corner_type == 0:  # 左上角是草地
        draw.rectangle([0, 0, TILE_SIZE//2-1, TILE_SIZE//2-1], fill=grass_color)
        draw.rectangle([TILE_SIZE//2, 0, TILE_SIZE-1, TILE_SIZE-1], fill=dirt_color)
        draw.rectangle([0, TILE_SIZE//2, TILE_SIZE-1, TILE_SIZE-1], fill=dirt_color)
    elif corner_type == 1:  # 右上角是草地
        draw.rectangle([TILE_SIZE//2, 0, TILE_SIZE-1, TILE_SIZE//2-1], fill=grass_color)
        draw.rectangle([0, 0, TILE_SIZE//2-1, TILE_SIZE-1], fill=dirt_color)
        draw.rectangle([0, TILE_SIZE//2, TILE_SIZE-1, TILE_SIZE-1], fill=dirt_color)
    elif corner_type == 2:  # 左下角是草地
        draw.rectangle([0, TILE_SIZE//2, TILE_SIZE//2-1, TILE_SIZE-1], fill=grass_color)
        draw.rectangle([0, 0, TILE_SIZE-1, TILE_SIZE//2-1], fill=dirt_color)
        draw.rectangle([TILE_SIZE//2, 0, TILE_SIZE-1, TILE_SIZE-1], fill=dirt_color)
    elif corner_type == 3:  # 右下角是草地
        draw.rectangle([TILE_SIZE//2, TILE_SIZE//2, TILE_SIZE-1, TILE_SIZE-1], fill=grass_color)
        draw.rectangle([0, 0, TILE_SIZE-1, TILE_SIZE//2-1], fill=dirt_color)
        draw.rectangle([0, TILE_SIZE//2, TILE_SIZE//2-1, TILE_SIZE-1], fill=dirt_color)
    
    return img

def create_intersection_tiles():
    """创建交叉口瓦片"""
    tiles = []
    
    # 4 个基础内部瓦片（不同变体）
    for i in range(4):
        tiles.append(('road_base_%d' % i, create_base_road_tile(i)))
    
    # 4 个边缘瓦片
    directions = ['top', 'right', 'bottom', 'left']
    for i, dir_name in enumerate(directions):
        tiles.append(('road_edge_%s' % dir_name, create_road_edge_tile(i)))
    
    # 4 个角落瓦片
    corners = ['topleft', 'topright', 'bottomleft', 'bottomright']
    for i, corner_name in enumerate(corners):
        tiles.append(('road_corner_%s' % corner_name, create_road_corner_tile(i)))
    
    return tiles

def generate_tileset():
    """生成完整的道路 TileSet 图集"""
    print("🛣️ 开始生成道路 TileSet...")
    
    # 创建输出目录
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # 生成所有瓦片
    tiles = create_intersection_tiles()
    
    # 创建图集（排列成网格）
    cols = 4
    rows = 4
    atlas_width = cols * TILE_SIZE
    atlas_height = rows * TILE_SIZE
    
    atlas = Image.new('RGBA', (atlas_width, atlas_height), (0, 0, 0, 0))
    
    for idx, (name, tile) in enumerate(tiles):
        col = idx % cols
        row = idx // cols
        atlas.paste(tile, (col * TILE_SIZE, row * TILE_SIZE))
        print(f"  ✓ {name}")
    
    # 保存图集
    atlas_path = os.path.join(OUTPUT_DIR, 'roads.png')
    atlas.save(atlas_path)
    print(f"\n✅ 道路 TileSet 已保存到：{atlas_path}")
    print(f"   尺寸：{atlas_width}x{atlas_height} 像素")
    print(f"   瓦片数量：{len(tiles)} 个 ({cols}x{rows} 网格)")
    
    return atlas_path

if __name__ == '__main__':
    generate_tileset()
