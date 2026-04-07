#!/usr/bin/env python3
"""
地图边界装饰 TileSet 生成器
生成 64x64 像素的地图边缘过渡和装饰瓦片
"""

from PIL import Image, ImageDraw
import os

# 配置
TILE_SIZE = 64
OUTPUT_DIR = "code/assets/sprites/tilesets"
PALETTE = {
    'grass_dark': (34, 139, 34),        # 深绿草地
    'grass_mid': (60, 179, 60),         # 中绿草地
    'grass_light': (107, 221, 107),     # 浅绿草地
    'dirt': (101, 67, 33),              # 泥土
    'fog_light': (200, 200, 200, 180),  # 薄雾
    'fog_heavy': (150, 150, 150, 200),  # 浓雾
    'hill_dark': (60, 80, 60),          # 远山深色
    'hill_mid': (80, 100, 80),          # 远山中色
    'tree_silhouette': (40, 60, 40),    # 树林剪影
}

def create_fog_edge_tile(direction):
    """
    创建迷雾边缘瓦片
    direction: 0=上，1=右，2=下，3=左
    """
    img = Image.new('RGBA', (TILE_SIZE, TILE_SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 草地基底
    draw.rectangle([0, 0, TILE_SIZE-1, TILE_SIZE-1], fill=PALETTE['grass_mid'])
    
    # 迷雾渐变
    if direction == 0:  # 上边缘迷雾
        for i in range(32):
            alpha = int(200 * (1 - i/32))
            fog_color = (200, 200, 200, alpha)
            y = i * 2
            draw.rectangle([0, y, TILE_SIZE-1, y+1], fill=fog_color)
    
    elif direction == 2:  # 下边缘迷雾
        for i in range(32):
            alpha = int(200 * (1 - i/32))
            fog_color = (200, 200, 200, alpha)
            y = TILE_SIZE - i * 2 - 1
            draw.rectangle([0, y, TILE_SIZE-1, y+1], fill=fog_color)
    
    elif direction == 1:  # 右边缘迷雾
        for i in range(32):
            alpha = int(200 * (1 - i/32))
            fog_color = (200, 200, 200, alpha)
            x = TILE_SIZE - i * 2 - 1
            draw.rectangle([x, 0, x+1, TILE_SIZE-1], fill=fog_color)
    
    elif direction == 3:  # 左边缘迷雾
        for i in range(32):
            alpha = int(200 * (1 - i/32))
            fog_color = (200, 200, 200, alpha)
            x = i * 2
            draw.rectangle([x, 0, x+1, TILE_SIZE-1], fill=fog_color)
    
    return img

def create_hill_border_tile():
    """创建远山边界瓦片"""
    img = Image.new('RGBA', (TILE_SIZE, TILE_SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 草地基底
    draw.rectangle([0, 0, TILE_SIZE-1, TILE_SIZE-1], fill=PALETTE['grass_mid'])
    
    # 远山剪影（上半部分）
    # 画多个山峰
    peaks = [
        (8, 24), (24, 16), (40, 28), (56, 20)
    ]
    
    for i, (px, py) in enumerate(peaks):
        # 山峰
        draw.polygon([
            (px-12, 32),
            (px, py),
            (px+12, 32)
        ], fill=PALETTE['hill_dark'])
        
        # 第二层山
        draw.polygon([
            (px-8, 32),
            (px, py+8),
            (px+8, 32)
        ], fill=PALETTE['hill_mid'])
    
    return img

def create_tree_border_tile():
    """创建树林边界瓦片"""
    img = Image.new('RGBA', (TILE_SIZE, TILE_SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 草地基底
    draw.rectangle([0, 0, TILE_SIZE-1, TILE_SIZE-1], fill=PALETTE['grass_mid'])
    
    # 树林剪影（底部）
    for i in range(8):
        tx = i * 8
        ty = TILE_SIZE - 16 - (i % 3) * 4
        # 树干
        draw.rectangle([tx+2, ty+8, tx+6, TILE_SIZE-8], fill=PALETTE['tree_silhouette'])
        # 树冠
        draw.polygon([
            (tx, ty+8),
            (tx+4, ty),
            (tx+8, ty+8)
        ], fill=PALETTE['tree_silhouette'])
    
    return img

def create_gradient_border_tile(direction):
    """
    创建渐变过渡边界瓦片
    direction: 0=上，1=右，2=下，3=左
    """
    img = Image.new('RGBA', (TILE_SIZE, TILE_SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 从草地到透明的渐变
    if direction == 0:  # 上边缘渐变
        for i in range(TILE_SIZE):
            alpha = int(255 * (i / TILE_SIZE))
            y = i
            grass_color = (*PALETTE['grass_mid'], alpha)
            draw.rectangle([0, y, TILE_SIZE-1, y+1], fill=grass_color)
    
    elif direction == 2:  # 下边缘渐变
        for i in range(TILE_SIZE):
            alpha = int(255 * ((TILE_SIZE-i) / TILE_SIZE))
            y = i
            grass_color = (*PALETTE['grass_mid'], alpha)
            draw.rectangle([0, y, TILE_SIZE-1, y+1], fill=grass_color)
    
    elif direction == 1:  # 右边缘渐变
        for i in range(TILE_SIZE):
            alpha = int(255 * ((TILE_SIZE-i) / TILE_SIZE))
            x = i
            grass_color = (*PALETTE['grass_mid'], alpha)
            draw.rectangle([x, 0, x+1, TILE_SIZE-1], fill=grass_color)
    
    elif direction == 3:  # 左边缘渐变
        for i in range(TILE_SIZE):
            alpha = int(255 * (i / TILE_SIZE))
            x = i
            grass_color = (*PALETTE['grass_mid'], alpha)
            draw.rectangle([x, 0, x+1, TILE_SIZE-1], fill=grass_color)
    
    return img

def create_corner_transition_tile(corner_type):
    """
    创建角落过渡瓦片
    corner_type: 0=左上，1=右上，2=左下，3=右下
    """
    img = Image.new('RGBA', (TILE_SIZE, TILE_SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 草地基底
    draw.rectangle([0, 0, TILE_SIZE-1, TILE_SIZE-1], fill=PALETTE['grass_mid'])
    
    # 角落迷雾
    if corner_type == 0:  # 左上角
        for i in range(32):
            alpha = int(180 * (1 - i/32))
            fog_color = (200, 200, 200, alpha)
            for j in range(i//2):
                if i*i + j*j < 32*32:
                    draw.point((j, i), fill=fog_color)
    
    elif corner_type == 1:  # 右上角
        for i in range(32):
            alpha = int(180 * (1 - i/32))
            fog_color = (200, 200, 200, alpha)
            for j in range(i//2):
                if i*i + j*j < 32*32:
                    draw.point((TILE_SIZE-1-j, i), fill=fog_color)
    
    elif corner_type == 2:  # 左下角
        for i in range(32):
            alpha = int(180 * (1 - i/32))
            fog_color = (200, 200, 200, alpha)
            for j in range(i//2):
                if i*i + j*j < 32*32:
                    draw.point((j, TILE_SIZE-1-i), fill=fog_color)
    
    elif corner_type == 3:  # 右下角
        for i in range(32):
            alpha = int(180 * (1 - i/32))
            fog_color = (200, 200, 200, alpha)
            for j in range(i//2):
                if i*i + j*j < 32*32:
                    draw.point((TILE_SIZE-1-j, TILE_SIZE-1-i), fill=fog_color)
    
    return img

def create_border_tiles():
    """创建所有边界装饰瓦片"""
    tiles = []
    
    # 迷雾边缘（4 个方向）
    directions = ['top', 'right', 'bottom', 'left']
    for i, dir_name in enumerate(directions):
        tiles.append((f'fog_edge_{dir_name}', create_fog_edge_tile(i)))
    
    # 远山边界
    tiles.append(('hill_border', create_hill_border_tile()))
    
    # 树林边界
    tiles.append(('tree_border', create_tree_border_tile()))
    
    # 渐变边缘（4 个方向）
    for i, dir_name in enumerate(directions):
        tiles.append((f'gradient_edge_{dir_name}', create_gradient_border_tile(i)))
    
    # 角落过渡（4 个）
    corners = ['topleft', 'topright', 'bottomleft', 'bottomright']
    for i, corner_name in enumerate(corners):
        tiles.append((f'corner_fog_{corner_name}', create_corner_transition_tile(i)))
    
    return tiles

def generate_tileset():
    """生成完整的边界装饰 TileSet 图集"""
    print("🗺️ 开始生成地图边界装饰 TileSet...")
    
    # 创建输出目录
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # 生成所有瓦片
    tiles = create_border_tiles()
    
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
    atlas_path = os.path.join(OUTPUT_DIR, 'borders.png')
    atlas.save(atlas_path)
    print(f"\n✅ 地图边界装饰 TileSet 已保存到：{atlas_path}")
    print(f"   尺寸：{atlas_width}x{atlas_height} 像素")
    print(f"   瓦片数量：{len(tiles)} 个 ({cols}x{rows} 网格)")
    
    return atlas_path

if __name__ == '__main__':
    generate_tileset()
