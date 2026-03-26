#!/usr/bin/env python3
"""
像素画生成工具 - Demon Village Game
可以生成角色立绘、表情变体、场景元素等像素风格资源

10 位村民角色：
1. 陈默（逃兵/万能工）- 黑发，棕色衣，沉默
2. 雷叔（铁匠）- 灰发，围裙，断臂义肢
3. 金铃（商人）- 金发，华丽红衣，精明
4. 白芷（医生）- 棕发，白衣，温柔
5. 老约翰（神父）- 白发，黑袍，神秘
6. 大熊（酒馆老板）- 棕发，壮硕，围裙
7. 影（神秘人）- 黑发，黑斗篷，孤僻
8. 小安（孩子）- 棕发，明亮衣服，可爱
9. 阿虎（守卫）- 黑发，盔甲，热血
10. 夜鸦（观察者）- 黑发，学者装，冷静
"""

from PIL import Image, ImageDraw
import os

# 色板定义 - 暮色村主题（暗色调，中世纪奇幻风格）
COLOR_PALETTE = {
    # 皮肤色
    'skin_light': (255, 224, 189),
    'skin_medium': (234, 194, 155),
    'skin_dark': (210, 160, 120),
    'skin_pale': (245, 230, 200),
    
    # 头发颜色
    'hair_black': (30, 25, 20),
    'hair_dark_brown': (60, 40, 25),
    'hair_brown': (80, 50, 30),
    'hair_light_brown': (120, 80, 50),
    'hair_blonde': (200, 170, 100),
    'hair_gold': (220, 180, 80),
    'hair_gray': (128, 128, 128),
    'hair_white': (230, 230, 230),
    'hair_silver': (180, 180, 190),
    
    # 衣服颜色
    'cloth_white': (240, 240, 240),
    'cloth_cream': (245, 240, 230),
    'cloth_blue': (60, 90, 140),
    'cloth_dark_blue': (40, 50, 90),
    'cloth_red': (140, 50, 50),
    'cloth_dark_red': (100, 30, 30),
    'cloth_green': (60, 100, 60),
    'cloth_dark_green': (40, 70, 40),
    'cloth_brown': (100, 70, 40),
    'cloth_dark_brown': (70, 45, 25),
    'cloth_black': (40, 35, 30),
    'cloth_purple': (80, 50, 90),
    'cloth_gold': (180, 140, 60),
    'cloth_orange': (180, 100, 40),
    
    # 特殊
    'metal_silver': (180, 180, 190),
    'metal_gold': (200, 170, 80),
    'leather': (120, 80, 50),
    'apron': (140, 100, 60),
    
    # 背景/环境
    'bg_dark': (30, 25, 35),
    'bg_twilight': (60, 50, 80),
    'highlight': (200, 180, 100),
    
    # 轮廓
    'outline': (20, 15, 25),
    'outline_soft': (60, 50, 55),
}

# 所有角色定义
ALL_CHARACTERS = [
    {
        'id': 'chenmo',
        'name': '陈默',
        'title': '逃兵/万能工',
        'description': '沉默寡言的年轻旅人，眼神中藏着秘密',
        'size': (64, 64),
        'colors': {
            'hair': 'hair_black',
            'skin': 'skin_medium',
            'cloth': 'cloth_brown',
            'outline': 'outline',
        },
        'features': ['simple_hair', 'neutral_eyes'],
        'expressions': ['normal', 'happy', 'sad', 'surprised', 'angry'],
    },
    {
        'id': 'leishu',
        'name': '雷叔',
        'title': '铁匠',
        'description': '断臂的老匠人，暴躁外表下藏着温柔',
        'size': (64, 64),
        'colors': {
            'hair': 'hair_gray',
            'skin': 'skin_dark',
            'cloth': 'cloth_dark_brown',
            'apron': 'apron',
            'outline': 'outline',
        },
        'features': ['gray_hair', 'beard', 'apron', 'strong_build'],
        'expressions': ['normal', 'angry', 'happy', 'tired'],
    },
    {
        'id': 'jinling',
        'name': '金铃',
        'title': '商人',
        'description': '精明的女商人，爱财但守底线',
        'size': (64, 64),
        'colors': {
            'hair': 'hair_gold',
            'skin': 'skin_light',
            'cloth': 'cloth_red',
            'accent': 'cloth_gold',
            'outline': 'outline',
        },
        'features': ['long_hair', 'elegant_clothes', 'accessories'],
        'expressions': ['normal', 'smile', 'calculating', 'surprised'],
    },
    {
        'id': 'baizhi',
        'name': '白芷',
        'title': '医生',
        'description': '温柔的女医师，洞察力强',
        'size': (64, 64),
        'colors': {
            'hair': 'hair_brown',
            'skin': 'skin_light',
            'cloth': 'cloth_white',
            'accent': 'cloth_green',
            'outline': 'outline_soft',
        },
        'features': ['gentle_hair', 'kind_eyes', 'white_coat'],
        'expressions': ['normal', 'gentle_smile', 'concerned', 'sad'],
    },
    {
        'id': 'laojohn',
        'name': '老约翰',
        'title': '神父',
        'description': '神秘的祭司，说话爱打机锋',
        'size': (64, 64),
        'colors': {
            'hair': 'hair_white',
            'skin': 'skin_pale',
            'cloth': 'cloth_black',
            'accent': 'cloth_purple',
            'outline': 'outline',
        },
        'features': ['white_robe', 'long_beard', 'mysterious'],
        'expressions': ['normal', 'wise', 'mysterious', 'serious'],
    },
    {
        'id': 'daxiong',
        'name': '大熊',
        'title': '酒馆老板',
        'description': '豪爽的酒馆主人，善于倾听',
        'size': (64, 64),
        'colors': {
            'hair': 'hair_dark_brown',
            'skin': 'skin_dark',
            'cloth': 'cloth_dark_red',
            'apron': 'apron',
            'outline': 'outline',
        },
        'features': ['big_build', 'beard', 'apron', 'friendly'],
        'expressions': ['normal', 'laugh', 'serious', 'listening'],
    },
    {
        'id': 'ying',
        'name': '影',
        'title': '神秘人',
        'description': '独居的怪人，说话半真半假',
        'size': (64, 64),
        'colors': {
            'hair': 'hair_black',
            'skin': 'skin_pale',
            'cloth': 'cloth_black',
            'cloak': 'cloth_dark_blue',
            'outline': 'outline',
        },
        'features': ['hood', 'cloak', 'mysterious', 'hidden_face'],
        'expressions': ['normal', 'cold', 'thinking', 'warning'],
    },
    {
        'id': 'xiaoan',
        'name': '小安',
        'title': '孩子',
        'description': '8 岁的可爱孩子，队长的遗孤',
        'size': (64, 64),
        'colors': {
            'hair': 'hair_light_brown',
            'skin': 'skin_light',
            'cloth': 'cloth_blue',
            'accent': 'cloth_white',
            'outline': 'outline_soft',
        },
        'features': ['small_body', 'big_eyes', 'childlike', 'innocent'],
        'expressions': ['normal', 'happy', 'curious', 'sad', 'excited'],
    },
    {
        'id': 'xiaohu',
        'name': '阿虎',
        'title': '守卫',
        'description': '年轻的村守卫队长，热血有责任感',
        'size': (64, 64),
        'colors': {
            'hair': 'hair_black',
            'skin': 'skin_medium',
            'cloth': 'cloth_dark_blue',
            'armor': 'metal_silver',
            'outline': 'outline',
        },
        'features': ['short_hair', 'armor', 'confident', 'young'],
        'expressions': ['normal', 'determined', 'excited', 'serious'],
    },
    {
        'id': 'yeya',
        'name': '夜鸦',
        'title': '观察者',
        'description': '图书管理员/魔王卧底，冷静理性',
        'size': (64, 64),
        'colors': {
            'hair': 'hair_black',
            'skin': 'skin_pale',
            'cloth': 'cloth_dark_green',
            'accent': 'cloth_brown',
            'outline': 'outline',
        },
        'features': ['glasses', 'scholar', 'calm', 'neat_hair'],
        'expressions': ['normal', 'calm', 'thinking', 'conflicted'],
    },
]

def create_pixel_canvas(size, color=(0, 0, 0, 0)):
    """创建透明画布"""
    return Image.new('RGBA', size, color)

def draw_pixel(draw, x, y, color, size=1):
    """绘制单个像素（可放大）"""
    draw.rectangle([x*size, y*size, (x+1)*size-1, (y+1)*size-1], fill=color)

def draw_character_base(character, size=(64, 64), expression='normal'):
    """
    绘制角色的基础像素立绘
    使用 16x16 的设计，然后放大到目标尺寸
    """
    scale = size[0] // 16  # 缩放比例
    colors = character['colors']
    features = character.get('features', [])
    
    # 基础像素设计（16x16 网格）
    pixels = []
    
    # === 头发设计 ===
    if 'gray_hair' in features or 'white_hair' in features:
        # 老年角色发型
        pixels.extend([
            (5, 2, colors['hair']), (6, 2, colors['hair']), (7, 2, colors['hair']), 
            (8, 2, colors['hair']), (9, 2, colors['hair']), (10, 2, colors['hair']),
            (4, 3, colors['hair']), (5, 3, colors['hair']), (6, 3, colors['hair']), 
            (7, 3, colors['hair']), (8, 3, colors['hair']), (9, 3, colors['hair']), 
            (10, 3, colors['hair']), (11, 3, colors['hair']),
            (4, 4, colors['hair']), (11, 4, colors['hair']),  # 两侧白发
        ])
    elif 'long_hair' in features:
        # 长发（金铃）
        pixels.extend([
            (5, 2, colors['hair']), (6, 2, colors['hair']), (7, 2, colors['hair']), 
            (8, 2, colors['hair']), (9, 2, colors['hair']), (10, 2, colors['hair']),
            (4, 3, colors['hair']), (5, 3, colors['hair']), (6, 3, colors['hair']), 
            (7, 3, colors['hair']), (8, 3, colors['hair']), (9, 3, colors['hair']), 
            (10, 3, colors['hair']), (11, 3, colors['hair']),
            (4, 4, colors['hair']), (4, 5, colors['hair']), (4, 6, colors['hair']),  # 左侧长发
            (11, 4, colors['hair']), (11, 5, colors['hair']), (11, 6, colors['hair']),  # 右侧长发
        ])
    elif 'hood' in features:
        # 兜帽（影）
        pixels.extend([
            (4, 2, colors['cloak']), (5, 2, colors['cloak']), (6, 2, colors['cloak']), 
            (7, 2, colors['cloak']), (8, 2, colors['cloak']), (9, 2, colors['cloak']), 
            (10, 2, colors['cloak']), (11, 2, colors['cloak']),
            (3, 3, colors['cloak']), (4, 3, colors['cloak']), (11, 3, colors['cloak']), (12, 3, colors['cloak']),
            (3, 4, colors['cloak']), (12, 4, colors['cloak']),
        ])
    elif 'small_body' in features:
        # 儿童发型（小安）
        pixels.extend([
            (5, 2, colors['hair']), (6, 2, colors['hair']), (7, 2, colors['hair']), 
            (8, 2, colors['hair']), (9, 2, colors['hair']), (10, 2, colors['hair']),
            (4, 3, colors['hair']), (5, 3, colors['hair']), (6, 3, colors['hair']), 
            (7, 3, colors['hair']), (8, 3, colors['hair']), (9, 3, colors['hair']), 
            (10, 3, colors['hair']), (11, 3, colors['hair']),
        ])
    else:
        # 标准发型
        pixels.extend([
            (5, 2, colors['hair']), (6, 2, colors['hair']), (7, 2, colors['hair']), 
            (8, 2, colors['hair']), (9, 2, colors['hair']), (10, 2, colors['hair']),
            (4, 3, colors['hair']), (5, 3, colors['hair']), (6, 3, colors['hair']), 
            (7, 3, colors['hair']), (8, 3, colors['hair']), (9, 3, colors['hair']), 
            (10, 3, colors['hair']), (11, 3, colors['hair']),
        ])
    
    # === 脸部 ===
    if 'small_body' in features:
        # 儿童小脸
        pixels.extend([
            (6, 4, colors['skin']), (7, 4, colors['skin']), (8, 4, colors['skin']), (9, 4, colors['skin']),
            (6, 5, colors['skin']), (7, 5, colors['skin']), (8, 5, colors['skin']), (9, 5, colors['skin']),
            (6, 6, colors['skin']), (7, 6, colors['skin']), (8, 6, colors['skin']), (9, 6, colors['skin']),
        ])
    else:
        # 标准脸型
        pixels.extend([
            (5, 4, colors['skin']), (6, 4, colors['skin']), (7, 4, colors['skin']), 
            (8, 4, colors['skin']), (9, 4, colors['skin']), (10, 4, colors['skin']),
            (5, 5, colors['skin']), (6, 5, colors['skin']), (7, 5, colors['skin']), 
            (8, 5, colors['skin']), (9, 5, colors['skin']), (10, 5, colors['skin']),
            (5, 6, colors['skin']), (6, 6, colors['skin']), (7, 6, colors['skin']), 
            (8, 6, colors['skin']), (9, 6, colors['skin']), (10, 6, colors['skin']),
        ])
    
    # === 眼睛 ===
    if 'big_eyes' in features:
        # 儿童大眼睛
        pixels.extend([
            (6, 5, 'hair_black'), (7, 5, 'hair_black'),
            (9, 5, 'hair_black'), (10, 5, 'hair_black'),
        ])
    elif 'glasses' in features:
        # 眼镜（夜鸦）
        pixels.extend([
            (6, 5, 'hair_black'), (7, 5, colors['skin']), (8, 5, 'hair_black'),  # 眼镜框
            (6, 6, 'hair_black'), (7, 6, colors['skin']), (8, 6, 'hair_black'),
            (9, 5, 'hair_black'), (10, 5, colors['skin']), (11, 5, 'hair_black'),
            (9, 6, 'hair_black'), (10, 6, colors['skin']), (11, 6, 'hair_black'),
        ])
    elif 'kind_eyes' in features:
        # 温柔眼睛（白芷）
        pixels.extend([
            (6, 5, colors['hair']), (9, 5, colors['hair']),
        ])
    elif 'hidden_face' in features:
        # 隐藏脸部（影）- 只有眼睛可见
        pixels.extend([
            (6, 5, 'hair_black'), (10, 5, 'hair_black'),
        ])
    else:
        # 标准眼睛
        pixels.extend([
            (6, 5, 'hair_black'), (9, 5, 'hair_black'),
        ])
    
    # === 胡子/胡须 ===
    if 'beard' in features:
        pixels.extend([
            (6, 7, colors['hair']), (7, 7, colors['hair']), (8, 7, colors['hair']), (9, 7, colors['hair']),
            (6, 8, colors['hair']), (7, 8, colors['hair']), (8, 8, colors['hair']), (9, 8, colors['hair']),
        ])
    if 'long_beard' in features:
        pixels.extend([
            (6, 7, colors['hair']), (7, 7, colors['hair']), (8, 7, colors['hair']), (9, 7, colors['hair']),
            (6, 8, colors['hair']), (7, 8, colors['hair']), (8, 8, colors['hair']), (9, 8, colors['hair']),
            (7, 9, colors['hair']), (8, 9, colors['hair']),
        ])
    
    # === 嘴巴（根据表情） ===
    mouth_pixels = []
    if expression == 'normal':
        mouth_pixels = [(7, 7, colors.get('cloth', colors['hair']))]
    elif expression == 'happy' or expression == 'smile' or expression == 'gentle_smile' or expression == 'laugh':
        mouth_pixels = [(7, 7, 'cloth_red'), (6, 8, 'cloth_red'), (8, 8, 'cloth_red')]
    elif expression == 'sad' or expression == 'concerned':
        mouth_pixels = [(7, 8, colors['hair'])]
    elif expression == 'angry':
        mouth_pixels = [(7, 7, 'cloth_dark_red')]
    elif expression == 'surprised' or expression == 'excited':
        mouth_pixels = [(7, 7, 'cloth_black')]
    elif expression == 'calculating':
        mouth_pixels = [(7, 7, 'cloth_red')]
    elif expression == 'serious' or expression == 'determined':
        mouth_pixels = [(7, 7, colors['hair'])]
    elif expression == 'mysterious' or expression == 'wise':
        mouth_pixels = [(7, 7, colors.get('accent', colors['hair']))]
    elif expression == 'cold':
        mouth_pixels = [(7, 8, colors['hair'])]
    elif expression == 'thinking' or expression == 'conflicted':
        mouth_pixels = [(7, 7, colors['hair'])]
    elif expression == 'curious':
        mouth_pixels = [(7, 7, 'cloth_red')]
    elif expression == 'warning':
        mouth_pixels = [(7, 7, 'cloth_dark_red')]
    elif expression == 'tired':
        mouth_pixels = [(7, 8, colors['hair'])]
    elif expression == 'listening':
        mouth_pixels = [(7, 7, colors.get('cloth', colors['hair']))]
    
    pixels.extend([p for p in mouth_pixels if p])
    
    # === 身体/衣服 ===
    if 'small_body' in features:
        # 儿童小身体
        pixels.extend([
            (5, 8, colors['cloth']), (6, 8, colors['cloth']), (7, 8, colors['cloth']), 
            (8, 8, colors['cloth']), (9, 8, colors['cloth']), (10, 8, colors['cloth']),
            (5, 9, colors['cloth']), (6, 9, colors['cloth']), (7, 9, colors['cloth']), 
            (8, 9, colors['cloth']), (9, 9, colors['cloth']), (10, 9, colors['cloth']),
            (5, 10, colors['cloth']), (6, 10, colors['cloth']), (7, 10, colors['cloth']), 
            (8, 10, colors['cloth']), (9, 10, colors['cloth']), (10, 10, colors['cloth']),
        ])
    elif 'big_build' in features:
        # 强壮体型（大熊）
        pixels.extend([
            (3, 8, colors['cloth']), (4, 8, colors['cloth']), (5, 8, colors['cloth']), 
            (6, 8, colors['cloth']), (7, 8, colors['cloth']), (8, 8, colors['cloth']), 
            (9, 8, colors['cloth']), (10, 8, colors['cloth']), (11, 8, colors['cloth']), (12, 8, colors['cloth']),
            (3, 9, colors['cloth']), (4, 9, colors['cloth']), (5, 9, colors['cloth']), 
            (6, 9, colors['cloth']), (7, 9, colors['cloth']), (8, 9, colors['cloth']), 
            (9, 9, colors['cloth']), (10, 9, colors['cloth']), (11, 9, colors['cloth']), (12, 9, colors['cloth']),
        ])
    elif 'apron' in features:
        # 围裙（雷叔、大熊）
        pixels.extend([
            (4, 8, colors['cloth']), (5, 8, colors['cloth']), (6, 8, colors['cloth']), 
            (7, 8, colors['cloth']), (8, 8, colors['cloth']), (9, 8, colors['cloth']), 
            (10, 8, colors['cloth']), (11, 8, colors['cloth']),
            (4, 9, colors['apron']), (5, 9, colors['apron']), (6, 9, colors['apron']), 
            (7, 9, colors['apron']), (8, 9, colors['apron']), (9, 9, colors['apron']), 
            (10, 9, colors['apron']), (11, 9, colors['apron']),
            (4, 10, colors['apron']), (5, 10, colors['apron']), (6, 10, colors['apron']), 
            (7, 10, colors['apron']), (8, 10, colors['apron']), (9, 10, colors['apron']), 
            (10, 10, colors['apron']), (11, 10, colors['apron']),
        ])
    elif 'armor' in features:
        # 盔甲（阿虎）
        pixels.extend([
            (4, 8, colors['armor']), (5, 8, colors['armor']), (6, 8, colors['armor']), 
            (7, 8, colors['armor']), (8, 8, colors['armor']), (9, 8, colors['armor']), 
            (10, 8, colors['armor']), (11, 8, colors['armor']),
            (4, 9, colors['cloth']), (5, 9, colors['cloth']), (6, 9, colors['cloth']), 
            (7, 9, colors['cloth']), (8, 9, colors['cloth']), (9, 9, colors['cloth']), 
            (10, 9, colors['cloth']), (11, 9, colors['cloth']),
            (4, 10, colors['cloth']), (5, 10, colors['cloth']), (6, 10, colors['cloth']), 
            (7, 10, colors['cloth']), (8, 10, colors['cloth']), (9, 10, colors['cloth']), 
            (10, 10, colors['cloth']), (11, 10, colors['cloth']),
        ])
    elif 'cloak' in features:
        # 斗篷（影）
        pixels.extend([
            (3, 8, colors['cloak']), (4, 8, colors['cloak']), (5, 8, colors['cloak']), 
            (6, 8, colors['cloak']), (7, 8, colors['cloak']), (8, 8, colors['cloak']), 
            (9, 8, colors['cloak']), (10, 8, colors['cloak']), (11, 8, colors['cloak']), (12, 8, colors['cloak']),
            (3, 9, colors['cloak']), (4, 9, colors['cloak']), (5, 9, colors['cloth']), 
            (6, 9, colors['cloth']), (7, 9, colors['cloth']), (8, 9, colors['cloth']), 
            (9, 9, colors['cloth']), (10, 9, colors['cloak']), (11, 9, colors['cloak']), (12, 9, colors['cloak']),
        ])
    elif 'white_coat' in features:
        # 白大褂（白芷）
        pixels.extend([
            (4, 8, colors['cloth']), (5, 8, colors['cloth']), (6, 8, colors['cloth']), 
            (7, 8, colors['cloth']), (8, 8, colors['cloth']), (9, 8, colors['cloth']), 
            (10, 8, colors['cloth']), (11, 8, colors['cloth']),
            (4, 9, colors['cloth']), (5, 9, colors['cloth']), (6, 9, colors['accent']), 
            (7, 9, colors['cloth']), (8, 9, colors['cloth']), (9, 9, colors['accent']), 
            (10, 9, colors['cloth']), (11, 9, colors['cloth']),
        ])
    else:
        # 标准身体
        pixels.extend([
            (4, 8, colors['cloth']), (5, 8, colors['cloth']), (6, 8, colors['cloth']), 
            (7, 8, colors['cloth']), (8, 8, colors['cloth']), (9, 8, colors['cloth']), 
            (10, 8, colors['cloth']), (11, 8, colors['cloth']),
            (4, 9, colors['cloth']), (5, 9, colors['cloth']), (6, 9, colors['cloth']), 
            (7, 9, colors['cloth']), (8, 9, colors['cloth']), (9, 9, colors['cloth']), 
            (10, 9, colors['cloth']), (11, 9, colors['cloth']),
        ])
    
    # 创建图像并绘制
    img = create_pixel_canvas(size)
    draw = ImageDraw.Draw(img)
    
    for pixel in pixels:
        if pixel is None:
            continue
        x, y, color_key = pixel
        color = COLOR_PALETTE.get(color_key, color_key if isinstance(color_key, tuple) else COLOR_PALETTE['outline'])
        draw_pixel(draw, x, y, color, scale)
    
    return img

def generate_character_sprites(character, output_dir):
    """生成角色的所有表情变体"""
    os.makedirs(output_dir, exist_ok=True)
    
    char_id = character['id']
    expressions = character.get('expressions', ['normal', 'happy', 'sad', 'surprised', 'angry'])
    size = character.get('size', (64, 64))
    
    print(f"\n🎭 生成 {character['name']} ({character['title']}) 的立绘...")
    
    for expr in expressions:
        sprite = draw_character_base(character, size=size, expression=expr)
        filename = f"{char_id}_{expr}.png"
        filepath = os.path.join(output_dir, filename)
        sprite.save(filepath, 'PNG')
        print(f"   ✅ {filename}")
    
    # 生成 sprite sheet（所有表情合集）
    sprite_sheet = Image.new('RGBA', (size[0] * len(expressions), size[1]), (0, 0, 0, 0))
    for i, expr in enumerate(expressions):
        sprite = draw_character_base(character, size=size, expression=expr)
        sprite_sheet.paste(sprite, (i * size[0], 0))
    
    sprite_sheet.save(os.path.join(output_dir, f"{char_id}_spritesheet.png"), 'PNG')
    print(f"   ✅ {char_id}_spritesheet.png")

def generate_all_characters():
    """生成所有 10 位村民的立绘"""
    output_base = '/root/.openclaw/workspace/demon_village_game/code/assets/sprites/characters/'
    os.makedirs(output_base, exist_ok=True)
    
    print("🎨 Demon Village Game - 10 位村民立绘生成")
    print("=" * 60)
    
    # 生成色卡
    print("\n📋 生成色卡...")
    generate_pixel_test_pattern(output_base)
    
    # 生成所有角色
    for character in ALL_CHARACTERS:
        generate_character_sprites(character, output_base)
    
    print("\n" + "=" * 60)
    print("✅ 所有角色立绘生成完成！")
    print(f"📁 输出目录：{output_base}")
    
    # 生成资源清单
    generate_resource_manifest(output_base)

def generate_pixel_test_pattern(output_dir):
    """生成像素测试图案（色卡和网格）"""
    os.makedirs(output_dir, exist_ok=True)
    
    # 色卡
    color_card = Image.new('RGBA', (400, 280), (50, 50, 50))
    draw = ImageDraw.Draw(color_card)
    
    x, y = 10, 10
    for name, color in COLOR_PALETTE.items():
        draw.rectangle([x, y, x+30, y+30], fill=color)
        draw.rectangle([x, y, x+30, y+30], outline=(255, 255, 255), width=1)
        x += 40
        if x > 360:
            x = 10
            y += 40
    
    color_card.save(os.path.join(output_dir, 'color_palette.png'), 'PNG')

def generate_resource_manifest(output_dir):
    """生成资源清单文件"""
    manifest_path = os.path.join(output_dir, 'CHARACTERS_MANIFEST.md')
    
    with open(manifest_path, 'w', encoding='utf-8') as f:
        f.write("# 🎭 角色立绘资源清单\n\n")
        f.write("*自动生成 - Demon Village Game 美术资源*\n\n")
        f.write("---\n\n")
        
        f.write("## 📊 总览\n\n")
        f.write(f"- **角色数量**: {len(ALL_CHARACTERS)}\n")
        f.write(f"- **立绘尺寸**: 64x64 像素\n")
        f.write(f"- **表情数量**: 每个角色 3-5 个表情\n")
        f.write(f"- **格式**: PNG (透明背景)\n\n")
        
        f.write("## 👥 角色列表\n\n")
        
        for char in ALL_CHARACTERS:
            f.write(f"### {char['name']} - {char['title']}\n\n")
            f.write(f"- **ID**: `{char['id']}`\n")
            f.write(f"- **描述**: {char['description']}\n")
            f.write(f"- **表情**: {', '.join(char.get('expressions', []))}\n")
            f.write(f"- **特征**: {', '.join(char.get('features', []))}\n\n")
            f.write("**生成文件**:\n")
            for expr in char.get('expressions', []):
                f.write(f"- `{char['id']}_{expr}.png`\n")
            f.write(f"- `{char['id']}_spritesheet.png` (表情合集)\n\n")
            f.write("---\n\n")
        
        f.write("## 📁 文件结构\n\n")
        f.write("```\n")
        f.write("sprites/characters/\n")
        f.write("├── color_palette.png          # 色卡\n")
        f.write("├── CHARACTERS_MANIFEST.md     # 本清单\n")
        for char in ALL_CHARACTERS:
            f.write(f"├── {char['id']}_normal.png\n")
            f.write(f"├── {char['id']}_spritesheet.png\n")
        f.write("```\n\n")
        
        f.write("## 🎨 色板说明\n\n")
        f.write("| 类别 | 颜色名称 | RGB 值 |\n")
        f.write("|------|----------|--------|\n")
        for name, color in COLOR_PALETTE.items():
            f.write(f"| {name} | `{color}` |\n")
    
    print(f"📋 已生成资源清单：CHARACTERS_MANIFEST.md")

if __name__ == '__main__':
    generate_all_characters()
