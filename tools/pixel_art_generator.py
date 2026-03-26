#!/usr/bin/env python3
"""
像素画生成工具 - Demon Village Game
可以生成角色立绘、表情变体、场景元素等像素风格资源
"""

from PIL import Image, ImageDraw
import os

# 色板定义 - 暮色村主题（暗色调，中世纪奇幻风格）
COLOR_PALETTE = {
    # 皮肤色
    'skin_light': (255, 224, 189),
    'skin_medium': (234, 194, 155),
    'skin_dark': (210, 160, 120),
    
    # 头发颜色
    'hair_black': (30, 25, 20),
    'hair_brown': (80, 50, 30),
    'hair_blonde': (200, 170, 100),
    'hair_gray': (128, 128, 128),
    
    # 衣服颜色
    'cloth_white': (240, 240, 240),
    'cloth_blue': (60, 90, 140),
    'cloth_red': (140, 50, 50),
    'cloth_green': (60, 100, 60),
    'cloth_brown': (100, 70, 40),
    'cloth_black': (40, 35, 30),
    
    # 背景/环境
    'bg_dark': (30, 25, 35),
    'bg_twilight': (60, 50, 80),
    'highlight': (200, 180, 100),
    
    # 轮廓
    'outline': (20, 15, 25),
}

# 角色定义 - 陈默（主角）
CHENMO_DESIGN = {
    'name': '陈默',
    'description': '沉默寡言的年轻旅人，眼神中藏着秘密',
    'size': (64, 64),  # 像素尺寸
    'colors': {
        'hair': 'hair_black',
        'skin': 'skin_medium',
        'cloth': 'cloth_brown',
        'outline': 'outline',
    },
    'expressions': ['normal', 'happy', 'sad', 'surprised', 'angry'],
}

def create_pixel_canvas(size, color=(0, 0, 0, 0)):
    """创建透明画布"""
    return Image.new('RGBA', size, color)

def draw_pixel(draw, x, y, color, size=1):
    """绘制单个像素（可放大）"""
    draw.rectangle([x*size, y*size, (x+1)*size-1, (y+1)*size-1], fill=color)

def draw_chenmo_base(size=(64, 64), expression='normal'):
    """
    绘制陈默的基础像素立绘
    使用 16x16 的设计，然后放大到目标尺寸
    """
    scale = size[0] // 16  # 缩放比例
    
    # 16x16 像素设计网格（简化的正面立绘）
    # 每个元组：(x, y, color_key)
    pixels = [
        # 头发（顶部）
        (5, 2, 'hair_black'), (6, 2, 'hair_black'), (7, 2, 'hair_black'), (8, 2, 'hair_black'), (9, 2, 'hair_black'), (10, 2, 'hair_black'),
        (4, 3, 'hair_black'), (5, 3, 'hair_black'), (6, 3, 'hair_black'), (7, 3, 'hair_black'), (8, 3, 'hair_black'), (9, 3, 'hair_black'), (10, 3, 'hair_black'), (11, 3, 'hair_black'),
        
        # 脸
        (5, 4, 'skin_medium'), (6, 4, 'skin_medium'), (7, 4, 'skin_medium'), (8, 4, 'skin_medium'), (9, 4, 'skin_medium'), (10, 4, 'skin_medium'),
        (5, 5, 'skin_medium'), (6, 5, 'skin_medium'), (7, 5, 'skin_medium'), (8, 5, 'skin_medium'), (9, 5, 'skin_medium'), (10, 5, 'skin_medium'),
        (5, 6, 'skin_medium'), (6, 6, 'skin_medium'), (7, 6, 'skin_medium'), (8, 6, 'skin_medium'), (9, 6, 'skin_medium'), (10, 6, 'skin_medium'),
        
        # 眼睛
        (6, 5, 'hair_black'), (9, 5, 'hair_black'),
        
        # 嘴巴（根据表情变化）
        (7, 7, 'hair_black') if expression == 'normal' else None,
        (7, 7, 'cloth_red') if expression == 'happy' else None,  # 笑脸用红色表示
        (7, 8, 'hair_black') if expression == 'sad' else None,
        
        # 身体/衣服
        (4, 8, 'cloth_brown'), (5, 8, 'cloth_brown'), (6, 8, 'cloth_brown'), (7, 8, 'cloth_brown'), (8, 8, 'cloth_brown'), (9, 8, 'cloth_brown'), (10, 8, 'cloth_brown'), (11, 8, 'cloth_brown'),
        (4, 9, 'cloth_brown'), (5, 9, 'cloth_brown'), (6, 9, 'cloth_brown'), (7, 9, 'cloth_brown'), (8, 9, 'cloth_brown'), (9, 9, 'cloth_brown'), (10, 9, 'cloth_brown'), (11, 9, 'cloth_brown'),
        (4, 10, 'cloth_brown'), (5, 10, 'cloth_brown'), (6, 10, 'cloth_brown'), (7, 10, 'cloth_brown'), (8, 10, 'cloth_brown'), (9, 10, 'cloth_brown'), (10, 10, 'cloth_brown'), (11, 10, 'cloth_brown'),
        (4, 11, 'cloth_brown'), (5, 11, 'cloth_brown'), (6, 11, 'cloth_brown'), (7, 11, 'cloth_brown'), (8, 11, 'cloth_brown'), (9, 11, 'cloth_brown'), (10, 11, 'cloth_brown'), (11, 11, 'cloth_brown'),
    ]
    
    img = create_pixel_canvas(size)
    draw = ImageDraw.Draw(img)
    
    # 绘制像素
    for pixel in pixels:
        if pixel is None:
            continue
        x, y, color_key = pixel
        color = COLOR_PALETTE.get(color_key, COLOR_PALETTE['outline'])
        draw_pixel(draw, x, y, color, scale)
    
    return img

def generate_character_sprites(character_name, output_dir):
    """生成角色的所有表情变体"""
    os.makedirs(output_dir, exist_ok=True)
    
    expressions = ['normal', 'happy', 'sad', 'surprised', 'angry']
    
    for expr in expressions:
        sprite = draw_chenmo_base(size=(64, 64), expression=expr)
        filename = f"{character_name}_{expr}.png"
        filepath = os.path.join(output_dir, filename)
        sprite.save(filepath, 'PNG')
        print(f"✅ 已生成：{filename}")
    
    # 生成 sprite sheet（所有表情合集）
    sprite_sheet = Image.new('RGBA', (64 * len(expressions), 64), (0, 0, 0, 0))
    for i, expr in enumerate(expressions):
        sprite = draw_chenmo_base(size=(64, 64), expression=expr)
        sprite_sheet.paste(sprite, (i * 64, 0))
    
    sprite_sheet.save(os.path.join(output_dir, f"{character_name}_spritesheet.png"), 'PNG')
    print(f"✅ 已生成：{character_name}_spritesheet.png")

def generate_pixel_test_pattern(output_dir):
    """生成像素测试图案（色卡和网格）"""
    os.makedirs(output_dir, exist_ok=True)
    
    # 色卡
    color_card = Image.new('RGBA', (320, 200), (50, 50, 50))
    draw = ImageDraw.Draw(color_card)
    
    x, y = 10, 10
    for name, color in COLOR_PALETTE.items():
        draw.rectangle([x, y, x+30, y+30], fill=color)
        draw.rectangle([x, y, x+30, y+30], outline=(255, 255, 255), width=1)
        x += 40
        if x > 280:
            x = 10
            y += 40
    
    color_card.save(os.path.join(output_dir, 'color_palette.png'), 'PNG')
    print(f"✅ 已生成：color_palette.png")

if __name__ == '__main__':
    output_base = '/root/.openclaw/workspace/demon_village_game/code/assets/sprites/characters/'
    
    print("🎨 Demon Village Game 像素画生成工具")
    print("=" * 50)
    
    # 生成色卡
    print("\n📋 生成色卡...")
    generate_pixel_test_pattern(output_base)
    
    # 生成陈默的立绘
    print("\n🎭 生成陈默的立绘...")
    generate_character_sprites('chenmo', output_base)
    
    print("\n" + "=" * 50)
    print("✅ 所有资源生成完成！")
    print(f"📁 输出目录：{output_base}")
