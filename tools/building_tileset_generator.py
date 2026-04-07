#!/usr/bin/env python3
"""
建筑 TileSet 生成器
生成 64x64 像素的像素风格建筑瓦片集
"""

from PIL import Image, ImageDraw
import os

# 配置
TILE_SIZE = 64
OUTPUT_DIR = "code/assets/sprites/tilesets"
PALETTE = {
    'wood_dark': (101, 67, 33),         # 深木色
    'wood_mid': (139, 90, 43),          # 中木色
    'wood_light': (181, 137, 84),       # 浅木色
    'stone_gray': (128, 128, 128),      # 石头灰
    'stone_dark': (80, 80, 80),         # 深石头
    'roof_red': (165, 42, 42),          # 屋顶红
    'roof_brown': (101, 41, 25),        # 屋顶棕
    'window_yellow': (255, 215, 0),     # 窗户黄光
    'door_brown': (60, 40, 20),         # 门棕色
}

def create_wall_tile(variation=0):
    """创建墙壁瓦片"""
    img = Image.new('RGBA', (TILE_SIZE, TILE_SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 木板底色
    base_color = PALETTE['wood_mid']
    draw.rectangle([0, 0, TILE_SIZE-1, TILE_SIZE-1], fill=base_color)
    
    # 画木板纹理（横向）
    board_heights = [12, 14, 13, 12, 13]
    y_offset = 0
    for i, height in enumerate(board_heights):
        y = y_offset + i * 12
        # 木板主体
        draw.rectangle([0, y, TILE_SIZE-1, y+height-1], fill=base_color)
        # 木板缝隙
        draw.line([(0, y+height-1), (TILE_SIZE-1, y+height-1)], fill=PALETTE['wood_dark'], width=1)
        # 木纹
        for j in range(4):
            x = (variation * 17 + j * 20) % (TILE_SIZE - 10) + 5
            draw.line([(x, y+3), (x+15, y+3)], fill=PALETTE['wood_light'], width=1)
            draw.line([(x+5, y+8), (x+18, y+8)], fill=PALETTE['wood_light'], width=1)
    
    return img

def create_roof_tile(direction, corner=False):
    """
    创建屋顶瓦片
    direction: 0=上，1=右，2=下，3=左
    """
    img = Image.new('RGBA', (TILE_SIZE, TILE_SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    roof_color = PALETTE['roof_red'] if direction % 2 == 0 else PALETTE['roof_brown']
    roof_dark = tuple(max(0, c-40) for c in roof_color)
    
    # 画瓦片（横向排列）
    tile_height = 8
    for row in range(8):
        y = row * tile_height
        offset = 16 if row % 2 == 0 else 0
        for col in range(5):
            x = col * 16 - offset
            # 瓦片形状
            draw.polygon([
                (x, y),
                (x+16, y),
                (x+14, y+6),
                (x+2, y+6)
            ], fill=roof_color)
            # 瓦片阴影
            draw.line([(x+2, y+6), (x+14, y+6)], fill=roof_dark, width=1)
    
    return img

def create_door_tile():
    """创建门瓦片"""
    img = Image.new('RGBA', (TILE_SIZE, TILE_SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 墙壁背景
    draw.rectangle([0, 0, TILE_SIZE-1, TILE_SIZE-1], fill=PALETTE['wood_mid'])
    
    # 门框
    door_width = 32
    door_height = 48
    door_x = (TILE_SIZE - door_width) // 2
    door_y = TILE_SIZE - door_height - 4
    
    # 门
    draw.rectangle([door_x, door_y, door_x+door_width-1, door_y+door_height-1], 
                   fill=PALETTE['door_brown'])
    
    # 门框
    draw.rectangle([door_x-2, door_y-2, door_x+door_width+1, door_y+door_height+1], 
                   fill=PALETTE['wood_dark'], width=2)
    
    # 门把手
    handle_x = door_x+door_width-8
    handle_y = door_y+door_height//2
    draw.ellipse([handle_x-3, handle_y-3, handle_x+3, handle_y+3], fill=PALETTE['window_yellow'])
    
    # 门板纹理
    for i in range(2):
        x = door_x + 8 + i * 14
        draw.line([(x, door_y+4), (x, door_y+door_height-4)], 
                  fill=PALETTE['wood_light'], width=1)
    
    return img

def create_window_tile():
    """创建窗户瓦片"""
    img = Image.new('RGBA', (TILE_SIZE, TILE_SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 墙壁背景
    draw.rectangle([0, 0, TILE_SIZE-1, TILE_SIZE-1], fill=PALETTE['wood_mid'])
    
    # 窗户
    win_width = 28
    win_height = 24
    win_x = (TILE_SIZE - win_width) // 2
    win_y = (TILE_SIZE - win_height) // 2
    
    # 窗框
    draw.rectangle([win_x, win_y, win_x+win_width-1, win_y+win_height-1], 
                   fill=PALETTE['window_yellow'])
    
    # 窗格（田字形）
    draw.rectangle([win_x+2, win_y+2, win_x+win_width-3, win_y+win_height-3], 
                   fill=PALETTE['wood_dark'])
    
    # 十字窗格
    mid_x = win_x + win_width // 2
    mid_y = win_y + win_height // 2
    draw.line([(mid_x, win_y+2), (mid_x, win_y+win_height-2)], 
              fill=PALETTE['wood_mid'], width=2)
    draw.line([(win_x+2, mid_y), (win_x+win_width-2, mid_y)], 
              fill=PALETTE['wood_mid'], width=2)
    
    # 窗台
    draw.rectangle([win_x-4, win_y+win_height, win_x+win_width+3, win_y+win_height+4], 
                   fill=PALETTE['wood_dark'])
    
    return img

def create_corner_wall():
    """创建墙角瓦片"""
    img = Image.new('RGBA', (TILE_SIZE, TILE_SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 左墙（深色）
    draw.rectangle([0, 0, TILE_SIZE//2-1, TILE_SIZE-1], fill=PALETTE['wood_dark'])
    # 右墙（浅色）
    draw.rectangle([TILE_SIZE//2, 0, TILE_SIZE-1, TILE_SIZE-1], fill=PALETTE['wood_mid'])
    
    # 墙角线
    draw.line([(TILE_SIZE//2, 0), (TILE_SIZE//2, TILE_SIZE-1)], 
              fill=PALETTE['wood_light'], width=2)
    
    return img

def create_tiles():
    """创建所有建筑瓦片"""
    tiles = []
    
    # 4 个墙壁瓦片（不同变体）
    for i in range(4):
        tiles.append(('wall_%d' % i, create_wall_tile(i)))
    
    # 2 个屋顶瓦片
    tiles.append(('roof_horizontal', create_roof_tile(0)))
    tiles.append(('roof_diagonal', create_roof_tile(1)))
    
    # 门窗瓦片
    tiles.append(('door', create_door_tile()))
    tiles.append(('window', create_window_tile()))
    
    # 墙角
    tiles.append(('corner', create_corner_wall()))
    
    # 基础瓦片（地面/地基）
    base = Image.new('RGBA', (TILE_SIZE, TILE_SIZE), PALETTE['stone_gray'])
    draw = ImageDraw.Draw(base)
    for i in range(8):
        for j in range(8):
            shade = 10 if (i+j) % 2 == 0 else -10
            color = tuple(max(0, min(255, c+shade)) for c in PALETTE['stone_gray'])
            draw.rectangle([i*8, j*8, i*8+7, j*8+7], fill=color)
    tiles.append(('foundation', base))
    
    return tiles

def generate_tileset():
    """生成完整的建筑 TileSet 图集"""
    print("🏠 开始生成建筑 TileSet...")
    
    # 创建输出目录
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # 生成所有瓦片
    tiles = create_tiles()
    
    # 创建图集（排列成 4x4 网格）
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
    atlas_path = os.path.join(OUTPUT_DIR, 'buildings.png')
    atlas.save(atlas_path)
    print(f"\n✅ 建筑 TileSet 已保存到：{atlas_path}")
    print(f"   尺寸：{atlas_width}x{atlas_height} 像素")
    print(f"   瓦片数量：{len(tiles)} 个 ({cols}x{rows} 网格)")
    
    return atlas_path

if __name__ == '__main__':
    generate_tileset()
