#!/usr/bin/env python3
"""
草地 TileSet 生成器
生成 64x64 像素的像素风格草地瓦片集
"""

from PIL import Image, ImageDraw
import os

# 配置
TILE_SIZE = 64
OUTPUT_DIR = "code/assets/sprites/tilesets"
PALETTE = {
    'grass_dark': (34, 139, 34),      # 深绿色
    'grass_mid': (60, 179, 60),       # 中绿色
    'grass_light': (107, 221, 107),   # 浅绿色
    'grass_yellow': (154, 205, 50),   # 黄绿色
    'dirt': (101, 67, 33),            # 泥土色
    'dirt_light': (139, 90, 43),      # 浅泥土
}

def create_base_grass_tile(variation=0):
    """创建基础草地瓦片（内部瓦片）"""
    img = Image.new('RGBA', (TILE_SIZE, TILE_SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 选择基色
    colors = [
        PALETTE['grass_dark'],
        PALETTE['grass_mid'],
        PALETTE['grass_light'],
        PALETTE['grass_yellow']
    ]
    base_color = colors[variation % len(colors)]
    
    # 填充基色
    draw.rectangle([0, 0, TILE_SIZE-1, TILE_SIZE-1], fill=base_color)
    
    # 添加像素风格的纹理噪点
    for _ in range(40):
        x = (variation * 17 + _) % TILE_SIZE
        y = (variation * 23 + _ * 7) % TILE_SIZE
        size = 2 + (_ % 3)
        shade = 15 if _ % 2 == 0 else -15
        color = tuple(max(0, min(255, c + shade)) for c in base_color)
        draw.rectangle([x, y, x+size, y+size], fill=color)
    
    # 添加小草装饰
    for i in range(8):
        gx = (variation * 13 + i * 11) % (TILE_SIZE - 8) + 4
        gy = (variation * 19 + i * 13) % (TILE_SIZE - 8) + 4
        grass_color = colors[(variation + 1) % len(colors)]
        # 画小草
        draw.line([(gx, gy+4), (gx, gy)], fill=grass_color, width=1)
        if i % 2 == 0:
            draw.line([(gx, gy+3), (gx-2, gy-1)], fill=grass_color, width=1)
        else:
            draw.line([(gx, gy+3), (gx+2, gy-1)], fill=grass_color, width=1)
    
    return img

def create_edge_tile(direction, corner=False):
    """
    创建边缘瓦片
    direction: 0=上，1=右，2=下，3=左
    corner: True=角落瓦片，False=边缘瓦片
    """
    img = Image.new('RGBA', (TILE_SIZE, TILE_SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 上半部分草地，下半部分泥土（以下边缘为例）
    grass_color = PALETTE['grass_mid']
    dirt_color = PALETTE['dirt']
    dirt_light = PALETTE['dirt_light']
    
    # 根据方向调整草地和泥土的位置
    if direction == 0:  # 上边缘 - 草地在下方
        grass_start = TILE_SIZE // 2
    elif direction == 1:  # 右边缘 - 草地在左方
        grass_start = 0
    elif direction == 2:  # 下边缘 - 草地在上方
        grass_start = 0
    else:  # 左边缘 - 草地在右方
        grass_start = TILE_SIZE // 2
    
    # 填充草地部分
    if direction == 0:  # 上边缘
        draw.rectangle([0, grass_start, TILE_SIZE-1, TILE_SIZE-1], fill=grass_color)
        # 草地纹理
        for _ in range(30):
            x = (_ * 17) % TILE_SIZE
            y = grass_start + (_ * 13) % (TILE_SIZE - grass_start - 4)
            shade = 15 if _ % 2 == 0 else -15
            color = tuple(max(0, min(255, c + shade)) for c in grass_color)
            draw.rectangle([x, y, x+2, y+2], fill=color)
        # 草地边缘装饰
        for i in range(16):
            ex = i * 4 + 2
            ey = grass_start - 2 + (i % 3)
            draw.rectangle([ex, ey, ex+2, grass_start+1], fill=grass_color)
    elif direction == 2:  # 下边缘
        draw.rectangle([0, 0, TILE_SIZE-1, TILE_SIZE//2], fill=grass_color)
        draw.rectangle([0, TILE_SIZE//2+4, TILE_SIZE-1, TILE_SIZE-1], fill=dirt_color)
        # 过渡带
        for i in range(TILE_SIZE//4):
            draw.rectangle([i*4, TILE_SIZE//2, i*4+3, TILE_SIZE//2+3], fill=dirt_light)
        # 草地纹理
        for _ in range(30):
            x = (_ * 17) % TILE_SIZE
            y = (_ * 13) % (TILE_SIZE//2 - 4)
            shade = 15 if _ % 2 == 0 else -15
            color = tuple(max(0, min(255, c + shade)) for c in grass_color)
            draw.rectangle([x, y, x+2, y+2], fill=color)
    elif direction == 1:  # 右边缘
        draw.rectangle([0, 0, TILE_SIZE//2, TILE_SIZE-1], fill=grass_color)
        draw.rectangle([TILE_SIZE//2+4, 0, TILE_SIZE-1, TILE_SIZE-1], fill=dirt_color)
        # 过渡带
        for i in range(TILE_SIZE//4):
            draw.rectangle([TILE_SIZE//2, i*4, TILE_SIZE//2+3, i*4+3], fill=dirt_light)
    elif direction == 3:  # 左边缘
        draw.rectangle([TILE_SIZE//2, 0, TILE_SIZE-1, TILE_SIZE-1], fill=grass_color)
        draw.rectangle([0, 0, TILE_SIZE//2-4, TILE_SIZE-1], fill=dirt_color)
        # 过渡带
        for i in range(TILE_SIZE//4):
            draw.rectangle([TILE_SIZE//2-3, i*4, TILE_SIZE//2, i*4+3], fill=dirt_light)
    
    return img

def create_corner_tile(corner_type):
    """
    创建角落瓦片
    corner_type: 0=左上，1=右上，2=左下，3=右下
    """
    img = Image.new('RGBA', (TILE_SIZE, TILE_SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    grass_color = PALETTE['grass_mid']
    dirt_color = PALETTE['dirt']
    
    # 根据角落类型填充
    if corner_type == 0:  # 左上角
        draw.rectangle([TILE_SIZE//2, TILE_SIZE//2, TILE_SIZE-1, TILE_SIZE-1], fill=grass_color)
        draw.rectangle([0, 0, TILE_SIZE//2-1, TILE_SIZE-1], fill=dirt_color)
        draw.rectangle([0, 0, TILE_SIZE-1, TILE_SIZE//2-1], fill=dirt_color)
    elif corner_type == 1:  # 右上角
        draw.rectangle([0, TILE_SIZE//2, TILE_SIZE//2-1, TILE_SIZE-1], fill=grass_color)
        draw.rectangle([TILE_SIZE//2, 0, TILE_SIZE-1, TILE_SIZE-1], fill=dirt_color)
        draw.rectangle([0, 0, TILE_SIZE-1, TILE_SIZE//2-1], fill=dirt_color)
    elif corner_type == 2:  # 左下角
        draw.rectangle([TILE_SIZE//2, 0, TILE_SIZE-1, TILE_SIZE//2-1], fill=grass_color)
        draw.rectangle([0, 0, TILE_SIZE-1, TILE_SIZE//2], fill=dirt_color)
        draw.rectangle([0, TILE_SIZE//2, TILE_SIZE//2-1, TILE_SIZE-1], fill=dirt_color)
    elif corner_type == 3:  # 右下角
        draw.rectangle([0, 0, TILE_SIZE//2-1, TILE_SIZE//2-1], fill=grass_color)
        draw.rectangle([0, 0, TILE_SIZE-1, TILE_SIZE//2], fill=dirt_color)
        draw.rectangle([TILE_SIZE//2, 0, TILE_SIZE-1, TILE_SIZE-1], fill=dirt_color)
    
    return img

def create_transition_tiles():
    """创建过渡瓦片（草地到泥土）"""
    tiles = []
    
    # 4 个基础内部瓦片（不同变体）
    for i in range(4):
        tiles.append(('grass_base_%d' % i, create_base_grass_tile(i)))
    
    # 4 个边缘瓦片
    directions = ['top', 'right', 'bottom', 'left']
    for i, dir_name in enumerate(directions):
        tiles.append(('grass_edge_%s' % dir_name, create_edge_tile(i)))
    
    # 4 个角落瓦片
    corners = ['topleft', 'topright', 'bottomleft', 'bottomright']
    for i, corner_name in enumerate(corners):
        tiles.append(('grass_corner_%s' % corner_name, create_corner_tile(i)))
    
    return tiles

def generate_tileset():
    """生成完整的 TileSet 图集"""
    print("🎨 开始生成草地 TileSet...")
    
    # 创建输出目录
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # 生成所有瓦片
    tiles = create_transition_tiles()
    
    # 创建图集（排列成网格）
    # 4x4 网格 = 16 个瓦片
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
    atlas_path = os.path.join(OUTPUT_DIR, 'grass.png')
    atlas.save(atlas_path)
    print(f"\n✅ 草地 TileSet 已保存到：{atlas_path}")
    print(f"   尺寸：{atlas_width}x{atlas_height} 像素")
    print(f"   瓦片数量：{len(tiles)} 个 ({cols}x{rows} 网格)")
    
    return atlas_path

if __name__ == '__main__':
    generate_tileset()
