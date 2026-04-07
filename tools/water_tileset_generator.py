#!/usr/bin/env python3
"""
水体 TileSet 生成器
生成 64x64 像素的像素风格水体瓦片集（带动画）
"""

from PIL import Image, ImageDraw
import os

# 配置
TILE_SIZE = 64
OUTPUT_DIR = "code/assets/sprites/tilesets"
ANIMATION_FRAMES = 4
PALETTE = {
    'water_deep': (30, 100, 160),       # 深水蓝
    'water_mid': (50, 140, 200),        # 中水蓝
    'water_light': (80, 180, 230),      # 浅水蓝
    'water_shallow': (120, 210, 240),   # 浅水
    'water_shore': (200, 180, 140),     # 岸边沙色
    'water_foam': (240, 240, 255),      # 水花白
}

def create_water_frame(frame=0):
    """创建单帧水面瓦片（用于动画）"""
    img = Image.new('RGBA', (TILE_SIZE, TILE_SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 填充水底色
    draw.rectangle([0, 0, TILE_SIZE-1, TILE_SIZE-1], fill=PALETTE['water_mid'])
    
    # 水波纹（根据帧偏移）
    wave_offset = frame * 4
    for row in range(4):
        y = 12 + row * 14
        for col in range(5):
            x = (col * 16 + wave_offset) % TILE_SIZE
            # 波纹高光
            draw.arc([x, y, x+12, y+6], 0, 180, fill=PALETTE['water_light'], width=2)
    
    # 闪光点
    for i in range(6):
        fx = (frame * 11 + i * 17) % (TILE_SIZE - 8) + 4
        fy = (frame * 13 + i * 19) % (TILE_SIZE - 8) + 4
        draw.point((fx, fy), fill=PALETTE['water_foam'])
        draw.point((fx+1, fy), fill=PALETTE['water_foam'])
    
    return img

def create_water_edge_tile(direction, frame=0):
    """
    创建水边缘瓦片（水与陆地过渡）
    direction: 0=上，1=右，2=下，3=左
    """
    img = Image.new('RGBA', (TILE_SIZE, TILE_SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    water_color = PALETTE['water_mid']
    shore_color = PALETTE['water_shore']
    foam_color = PALETTE['water_foam']
    
    if direction == 0:  # 上边缘 - 水在下方
        # 上方陆地（沙色）
        draw.rectangle([0, 0, TILE_SIZE-1, TILE_SIZE//2-8], fill=shore_color)
        # 下方水
        draw.rectangle([0, TILE_SIZE//2-4, TILE_SIZE-1, TILE_SIZE-1], fill=water_color)
        # 过渡带 - 水花
        for i in range(16):
            ex = i * 4
            ey = TILE_SIZE//2 - 6 + (i % 3)
            draw.rectangle([ex, ey, ex+3, ey+2], fill=foam_color)
        # 水波纹
        for row in range(2):
            y = TILE_SIZE//2 + 8 + row * 12
            for col in range(4):
                x = col * 16 + frame * 2
                draw.arc([x, y, x+12, y+4], 0, 180, fill=PALETTE['water_light'], width=1)
    
    elif direction == 2:  # 下边缘 - 水在上方
        # 上方水
        draw.rectangle([0, 0, TILE_SIZE-1, TILE_SIZE//2+4], fill=water_color)
        # 下方陆地（沙色）
        draw.rectangle([0, TILE_SIZE//2+8, TILE_SIZE-1, TILE_SIZE-1], fill=shore_color)
        # 过渡带 - 水花
        for i in range(16):
            ex = i * 4
            ey = TILE_SIZE//2 + 2 + (i % 3)
            draw.rectangle([ex, ey, ex+3, ey+2], fill=foam_color)
        # 水波纹
        for row in range(2):
            y = 8 + row * 12
            for col in range(4):
                x = col * 16 + frame * 2
                draw.arc([x, y, x+12, y+4], 0, 180, fill=PALETTE['water_light'], width=1)
    
    elif direction == 1:  # 右边缘 - 水在左方
        # 左方水
        draw.rectangle([0, 0, TILE_SIZE//2+4, TILE_SIZE-1], fill=water_color)
        # 右方陆地
        draw.rectangle([TILE_SIZE//2+8, 0, TILE_SIZE-1, TILE_SIZE-1], fill=shore_color)
        # 过渡带
        for i in range(16):
            ex = TILE_SIZE//2 + 2 + (i % 3)
            ey = i * 4
            draw.rectangle([ex, ey, ex+2, ey+3], fill=foam_color)
    
    elif direction == 3:  # 左边缘 - 水在右方
        # 左方陆地
        draw.rectangle([0, 0, TILE_SIZE//2-8, TILE_SIZE-1], fill=shore_color)
        # 右方水
        draw.rectangle([TILE_SIZE//2-4, 0, TILE_SIZE-1, TILE_SIZE-1], fill=water_color)
        # 过渡带
        for i in range(16):
            ex = TILE_SIZE//2 - 6 + (i % 3)
            ey = i * 4
            draw.rectangle([ex, ey, ex+2, ey+3], fill=foam_color)
    
    return img

def create_water_corner_tile(corner_type, frame=0):
    """
    创建水角落瓦片
    corner_type: 0=左上，1=右上，2=左下，3=右下
    """
    img = Image.new('RGBA', (TILE_SIZE, TILE_SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    water_color = PALETTE['water_mid']
    shore_color = PALETTE['water_shore']
    
    if corner_type == 0:  # 左上角是陆地
        draw.rectangle([0, 0, TILE_SIZE//2-1, TILE_SIZE//2-1], fill=shore_color)
        draw.rectangle([TILE_SIZE//2, 0, TILE_SIZE-1, TILE_SIZE-1], fill=water_color)
        draw.rectangle([0, TILE_SIZE//2, TILE_SIZE-1, TILE_SIZE-1], fill=water_color)
    elif corner_type == 1:  # 右上角是陆地
        draw.rectangle([TILE_SIZE//2, 0, TILE_SIZE-1, TILE_SIZE//2-1], fill=shore_color)
        draw.rectangle([0, 0, TILE_SIZE//2-1, TILE_SIZE-1], fill=water_color)
        draw.rectangle([0, TILE_SIZE//2, TILE_SIZE-1, TILE_SIZE-1], fill=water_color)
    elif corner_type == 2:  # 左下角是陆地
        draw.rectangle([0, TILE_SIZE//2, TILE_SIZE//2-1, TILE_SIZE-1], fill=shore_color)
        draw.rectangle([0, 0, TILE_SIZE-1, TILE_SIZE//2-1], fill=water_color)
        draw.rectangle([TILE_SIZE//2, 0, TILE_SIZE-1, TILE_SIZE-1], fill=water_color)
    elif corner_type == 3:  # 右下角是陆地
        draw.rectangle([TILE_SIZE//2, TILE_SIZE//2, TILE_SIZE-1, TILE_SIZE-1], fill=shore_color)
        draw.rectangle([0, 0, TILE_SIZE-1, TILE_SIZE//2-1], fill=water_color)
        draw.rectangle([0, TILE_SIZE//2, TILE_SIZE//2-1, TILE_SIZE-1], fill=water_color)
    
    return img

def create_tiles():
    """创建所有水体瓦片"""
    tiles = []
    
    # 4 个基础水面瓦片（动画帧）
    for i in range(ANIMATION_FRAMES):
        tiles.append((f'water_base_frame{i}', create_water_frame(i)))
    
    # 4 个边缘瓦片（使用第 0 帧）
    directions = ['top', 'right', 'bottom', 'left']
    for i, dir_name in enumerate(directions):
        tiles.append((f'water_edge_{dir_name}', create_water_edge_tile(i, 0)))
    
    # 4 个角落瓦片
    corners = ['topleft', 'topright', 'bottomleft', 'bottomright']
    for i, corner_name in enumerate(corners):
        tiles.append((f'water_corner_{corner_name}', create_water_corner_tile(i, 0)))
    
    return tiles

def generate_tileset():
    """生成完整的水体 TileSet 图集"""
    print("💧 开始生成水体 TileSet...")
    
    # 创建输出目录
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # 生成所有瓦片
    tiles = create_tiles()
    
    # 创建图集（4x4 网格）
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
    atlas_path = os.path.join(OUTPUT_DIR, 'water.png')
    atlas.save(atlas_path)
    print(f"\n✅ 水体 TileSet 已保存到：{atlas_path}")
    print(f"   尺寸：{atlas_width}x{atlas_height} 像素")
    print(f"   瓦片数量：{len(tiles)} 个 ({cols}x{rows} 网格)")
    print(f"   动画帧数：{ANIMATION_FRAMES} 帧")
    
    return atlas_path

if __name__ == '__main__':
    generate_tileset()
