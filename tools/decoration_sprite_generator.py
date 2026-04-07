#!/usr/bin/env python3
"""
装饰物 Sprite 生成器
生成像素风格的树木、石头、花草等装饰物
"""

from PIL import Image, ImageDraw
import os

# 配置
SPRITE_SIZE = 64
OUTPUT_DIR = "code/assets/sprites/decorations"
PALETTE = {
    'tree_trunk': (101, 67, 33),        # 树干棕色
    'tree_trunk_dark': (80, 50, 20),    # 树干深色
    'leaves': (34, 139, 34),            # 树叶绿
    'leaves_dark': (20, 100, 20),       # 树叶深绿
    'leaves_light': (60, 179, 60),      # 树叶浅绿
    'rock_gray': (128, 128, 128),       # 石头灰
    'rock_dark': (80, 80, 80),          # 石头深灰
    'rock_light': (160, 160, 160),      # 石头浅灰
    'flower_red': (220, 20, 60),        # 红花
    'flower_yellow': (255, 215, 0),     # 黄花
    'flower_blue': (30, 144, 255),      # 蓝花
    'grass': (60, 179, 60),             # 草丛绿
    'bush': (40, 120, 40),              # 灌木绿
}

def create_tree_sprite(variation=0):
    """创建树木 Sprite"""
    img = Image.new('RGBA', (SPRITE_SIZE, SPRITE_SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 树干
    trunk_width = 12 + variation * 2
    trunk_x = (SPRITE_SIZE - trunk_width) // 2
    draw.rectangle([trunk_x, 32, trunk_x+trunk_width, SPRITE_SIZE-8], 
                   fill=PALETTE['tree_trunk'])
    # 树干纹理
    for i in range(4):
        tx = trunk_x + 2 + i * 3
        draw.line([(tx, 36), (tx, SPRITE_SIZE-12)], 
                  fill=PALETTE['tree_trunk_dark'], width=1)
    
    # 树冠（圆形）
    crown_center = SPRITE_SIZE // 2 - 4
    crown_radius = 20 + variation * 2
    
    # 外层深绿
    draw.ellipse([crown_center-crown_radius, crown_center-crown_radius,
                  crown_center+crown_radius, crown_center+crown_radius],
                 fill=PALETTE['leaves_dark'])
    
    # 中层绿
    draw.ellipse([crown_center-crown_radius+4, crown_center-crown_radius+4,
                  crown_center+crown_radius-4, crown_center+crown_radius-4],
                 fill=PALETTE['leaves'])
    
    # 内层浅绿（高光）
    draw.ellipse([crown_center-crown_radius+8, crown_center-crown_radius+8,
                  crown_center+crown_radius-8, crown_center+crown_radius-8],
                 fill=PALETTE['leaves_light'])
    
    return img

def create_rock_sprite(size='medium'):
    """创建石头 Sprite"""
    img = Image.new('RGBA', (SPRITE_SIZE, SPRITE_SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    if size == 'small':
        rock_size = 16
        offset = (SPRITE_SIZE - rock_size) // 2
        points = [(offset+4, offset+8), (offset+12, offset+4),
                  (offset+14, offset+12), (offset+8, offset+14),
                  (offset+2, offset+12)]
    elif size == 'large':
        rock_size = 32
        offset = (SPRITE_SIZE - rock_size) // 2
        points = [(offset+8, offset+4), (offset+24, offset+8),
                  (offset+28, offset+20), (offset+20, offset+28),
                  (offset+8, offset+26), (offset+4, offset+16)]
    else:  # medium
        rock_size = 24
        offset = (SPRITE_SIZE - rock_size) // 2
        points = [(offset+6, offset+4), (offset+20, offset+6),
                  (offset+22, offset+16), (offset+16, offset+20),
                  (offset+6, offset+18), (offset+4, offset+10)]
    
    # 石头主体
    draw.polygon(points, fill=PALETTE['rock_gray'])
    
    # 石头阴影
    shadow_points = [(x+2, y+2) for x, y in points]
    draw.polygon(shadow_points, fill=PALETTE['rock_dark'])
    
    # 石头高光
    highlight_points = [(x-2, y-2) for x, y in points[:3]]
    draw.polygon(highlight_points, fill=PALETTE['rock_light'])
    
    return img

def create_flower_sprite(color='red'):
    """创建花朵 Sprite"""
    img = Image.new('RGBA', (SPRITE_SIZE, SPRITE_SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 选择颜色
    if color == 'yellow':
        petal_color = PALETTE['flower_yellow']
    elif color == 'blue':
        petal_color = PALETTE['flower_blue']
    else:
        petal_color = PALETTE['flower_red']
    
    # 花茎
    stem_x = SPRITE_SIZE // 2
    draw.line([(stem_x, 40), (stem_x, SPRITE_SIZE-8)], 
              fill=PALETTE['grass'], width=2)
    
    # 叶子
    draw.polygon([(stem_x, 48), (stem_x+10, 44), (stem_x+8, 50)],
                 fill=PALETTE['grass'])
    draw.polygon([(stem_x, 54), (stem_x-10, 50), (stem_x-8, 56)],
                 fill=PALETTE['grass'])
    
    # 花瓣（5 片）
    center = (SPRITE_SIZE // 2, 32)
    petal_size = 8
    for i in range(5):
        angle = i * 72
        import math
        px = int(center[0] + math.cos(math.radians(angle)) * petal_size)
        py = int(center[1] + math.sin(math.radians(angle)) * petal_size)
        draw.ellipse([px-petal_size//2, py-petal_size//2,
                      px+petal_size//2, py+petal_size//2],
                     fill=petal_color)
    
    # 花心
    draw.ellipse([center[0]-4, center[1]-4, center[0]+4, center[1]+4],
                 fill=PALETTE['flower_yellow'])
    
    return img

def create_grass_patch():
    """创建草丛 Sprite"""
    img = Image.new('RGBA', (SPRITE_SIZE, SPRITE_SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 画多根草
    for i in range(8):
        gx = 8 + i * 7
        gy = SPRITE_SIZE - 8
        # 草叶
        draw.line([(gx, gy), (gx-3, gy-20)], fill=PALETTE['grass'], width=2)
        draw.line([(gx+2, gy), (gx+4, gy-16)], fill=PALETTE['grass'], width=2)
        draw.line([(gx-2, gy), (gx-6, gy-14)], fill=PALETTE['grass'], width=2)
    
    return img

def create_bush_sprite():
    """创建灌木丛 Sprite"""
    img = Image.new('RGBA', (SPRITE_SIZE, SPRITE_SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 灌木主体（多个圆形组合）
    centers = [
        (24, 40), (40, 40), (32, 32), (28, 48), (36, 48)
    ]
    
    for cx, cy in centers:
        # 外层深绿
        draw.ellipse([cx-10, cy-10, cx+10, cy+10], fill=PALETTE['bush'])
        # 内层浅绿
        draw.ellipse([cx-6, cy-6, cx+6, cy+6], fill=PALETTE['grass'])
    
    return img

def create_decorations():
    """创建所有装饰物 Sprite"""
    sprites = []
    
    # 树木（3 种变体）
    for i in range(3):
        sprites.append((f'tree_{i+1}', create_tree_sprite(i)))
    
    # 石头（3 种尺寸）
    for size in ['small', 'medium', 'large']:
        sprites.append((f'rock_{size}', create_rock_sprite(size)))
    
    # 花朵（3 种颜色）
    for color in ['red', 'yellow', 'blue']:
        sprites.append((f'flower_{color}', create_flower_sprite(color)))
    
    # 草丛
    sprites.append(('grass_patch', create_grass_patch()))
    
    # 灌木丛
    sprites.append(('bush', create_bush_sprite()))
    
    return sprites

def generate_spritesheet():
    """生成装饰物 Sprite 图集"""
    print("🌳 开始生成装饰物 Sprite...")
    
    # 创建输出目录
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # 生成所有装饰物
    sprites = create_decorations()
    
    # 保存单个文件
    for name, sprite in sprites:
        sprite_path = os.path.join(OUTPUT_DIR, f'{name}.png')
        sprite.save(sprite_path)
        print(f"  ✓ {name}")
    
    # 创建图集（4x4 网格）
    cols = 4
    rows = 4
    atlas_width = cols * SPRITE_SIZE
    atlas_height = rows * SPRITE_SIZE
    
    atlas = Image.new('RGBA', (atlas_width, atlas_height), (0, 0, 0, 0))
    
    for idx, (name, sprite) in enumerate(sprites):
        col = idx % cols
        row = idx // cols
        atlas.paste(sprite, (col * SPRITE_SIZE, row * SPRITE_SIZE))
    
    # 保存图集
    atlas_path = os.path.join(OUTPUT_DIR, 'decorations_atlas.png')
    atlas.save(atlas_path)
    
    print(f"\n✅ 装饰物 Sprite 已保存到：{OUTPUT_DIR}/")
    print(f"   图集：{atlas_path}")
    print(f"   装饰物数量：{len(sprites)} 个")
    
    return atlas_path

if __name__ == '__main__':
    generate_spritesheet()
