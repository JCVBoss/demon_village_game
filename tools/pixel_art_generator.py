#!/usr/bin/env python3
"""
像素画生成工具 v2 - Demon Village Game
星露谷物语级别精细度 (32x32 基础设计)
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
# 增加更多渐变色以实现更精细的阴影和高光
COLOR_PALETTE = {
    # 皮肤色（3 阶渐变）
    'skin_light': (255, 235, 210),
    'skin_light_mid': (245, 215, 190),
    'skin_light_shadow': (230, 190, 165),
    'skin_medium': (240, 205, 175),
    'skin_medium_mid': (225, 185, 155),
    'skin_medium_shadow': (205, 160, 130),
    'skin_dark': (210, 170, 140),
    'skin_dark_mid': (190, 150, 120),
    'skin_dark_shadow': (170, 130, 100),
    'skin_pale': (250, 235, 215),
    'skin_pale_mid': (235, 215, 195),
    'skin_pale_shadow': (220, 195, 175),
    'skin_cheek': (245, 195, 185),  # 腮红
    
    # 头发颜色（3 阶渐变 + 高光）
    'hair_black': (35, 30, 25),
    'hair_black_mid': (50, 42, 35),
    'hair_black_light': (70, 60, 50),
    'hair_black_highlight': (95, 85, 70),
    'hair_dark_brown': (65, 45, 30),
    'hair_dark_brown_mid': (85, 60, 42),
    'hair_dark_brown_light': (110, 80, 58),
    'hair_dark_brown_highlight': (140, 105, 75),
    'hair_brown': (95, 60, 35),
    'hair_brown_mid': (120, 80, 52),
    'hair_brown_light': (150, 105, 72),
    'hair_brown_highlight': (180, 135, 95),
    'hair_light_brown': (140, 100, 65),
    'hair_light_brown_mid': (165, 125, 90),
    'hair_light_brown_light': (190, 150, 115),
    'hair_light_brown_highlight': (215, 180, 145),
    'hair_blonde': (210, 180, 110),
    'hair_blonde_mid': (225, 200, 140),
    'hair_blonde_light': (240, 220, 170),
    'hair_blonde_highlight': (250, 238, 200),
    'hair_gold': (220, 185, 85),
    'hair_gold_mid': (235, 205, 115),
    'hair_gold_light': (245, 225, 150),
    'hair_gold_highlight': (252, 240, 185),
    'hair_gray': (140, 140, 145),
    'hair_gray_mid': (165, 165, 170),
    'hair_gray_light': (190, 190, 195),
    'hair_gray_highlight': (215, 215, 220),
    'hair_white': (240, 240, 245),
    'hair_white_mid': (248, 248, 250),
    'hair_white_highlight': (252, 252, 255),
    'hair_silver': (185, 185, 195),
    'hair_silver_mid': (205, 205, 215),
    'hair_silver_light': (225, 225, 235),
    'hair_silver_highlight': (240, 240, 248),
    
    # 眼睛颜色
    'eye_black': (25, 20, 18),
    'eye_brown': (85, 55, 35),
    'eye_brown_light': (115, 75, 50),
    'eye_blue': (65, 110, 160),
    'eye_blue_light': (95, 140, 190),
    'eye_green': (70, 120, 85),
    'eye_green_light': (100, 155, 115),
    'eye_hazel': (105, 85, 55),
    'eye_hazel_light': (135, 110, 80),
    'eye_gray': (120, 125, 130),
    'eye_gray_light': (150, 155, 160),
    'eye_purple': (95, 70, 120),
    'eye_purple_light': (125, 95, 155),
    
    # 衣服颜色（3 阶渐变）
    'cloth_white': (248, 245, 240),
    'cloth_white_mid': (230, 225, 218),
    'cloth_white_shadow': (210, 203, 195),
    'cloth_cream': (245, 240, 228),
    'cloth_cream_mid': (228, 222, 208),
    'cloth_cream_shadow': (208, 200, 185),
    'cloth_blue': (70, 100, 155),
    'cloth_blue_mid': (95, 125, 175),
    'cloth_blue_light': (125, 155, 195),
    'cloth_dark_blue': (45, 55, 95),
    'cloth_dark_blue_mid': (65, 75, 120),
    'cloth_dark_blue_light': (90, 100, 150),
    'cloth_red': (155, 55, 55),
    'cloth_red_mid': (180, 75, 75),
    'cloth_red_light': (205, 100, 100),
    'cloth_dark_red': (115, 35, 35),
    'cloth_dark_red_mid': (140, 50, 50),
    'cloth_dark_red_light': (165, 70, 70),
    'cloth_green': (70, 115, 70),
    'cloth_green_mid': (95, 140, 95),
    'cloth_green_light': (125, 165, 125),
    'cloth_dark_green': (45, 80, 45),
    'cloth_dark_green_mid': (65, 105, 65),
    'cloth_dark_green_light': (90, 130, 90),
    'cloth_brown': (115, 80, 50),
    'cloth_brown_mid': (140, 100, 68),
    'cloth_brown_light': (165, 125, 90),
    'cloth_dark_brown': (80, 52, 30),
    'cloth_dark_brown_mid': (105, 72, 45),
    'cloth_dark_brown_light': (135, 97, 65),
    'cloth_black': (45, 40, 38),
    'cloth_black_mid': (65, 58, 55),
    'cloth_black_light': (90, 80, 75),
    'cloth_purple': (90, 60, 105),
    'cloth_purple_mid': (115, 80, 135),
    'cloth_purple_light': (145, 105, 165),
    'cloth_gold': (190, 150, 65),
    'cloth_gold_mid': (210, 175, 95),
    'cloth_gold_light': (230, 200, 130),
    'cloth_orange': (195, 110, 50),
    'cloth_orange_mid': (215, 135, 75),
    'cloth_orange_light': (235, 165, 105),
    'cloth_teal': (55, 115, 115),
    'cloth_teal_mid': (80, 140, 140),
    'cloth_teal_light': (110, 165, 165),
    
    # 特殊材质
    'apron': (150, 110, 70),
    'apron_mid': (170, 130, 90),
    'apron_light': (190, 155, 115),
    'leather': (130, 90, 55),
    'leather_mid': (155, 110, 75),
    'leather_light': (180, 135, 100),
    'metal_silver': (185, 185, 195),
    'metal_silver_mid': (205, 205, 215),
    'metal_silver_highlight': (230, 230, 240),
    'metal_gold': (210, 180, 90),
    'metal_gold_mid': (230, 205, 120),
    'metal_gold_highlight': (245, 230, 160),
    'wood': (135, 95, 60),
    'wood_mid': (160, 115, 78),
    'wood_light': (185, 140, 100),
    
    # 背景/环境
    'bg_dark': (35, 30, 40),
    'bg_twilight': (65, 55, 85),
    'highlight': (210, 190, 110),
    
    # 轮廓（软边）
    'outline': (25, 20, 30),
    'outline_soft': (65, 55, 65),
    'outline_light': (95, 85, 95),
}

# 所有角色定义（32x32 精细设计）
ALL_CHARACTERS = [
    {
        'id': 'chenmo',
        'name': '陈默',
        'title': '逃兵/万能工',
        'description': '沉默寡言的年轻旅人，眼神中藏着秘密',
        'base_size': (32, 32),
        'output_size': (128, 128),
        'colors': {
            'hair_base': 'hair_black',
            'hair_mid': 'hair_black_mid',
            'hair_light': 'hair_black_light',
            'hair_highlight': 'hair_black_highlight',
            'skin_base': 'skin_medium',
            'skin_mid': 'skin_medium_mid',
            'skin_shadow': 'skin_medium_shadow',
            'skin_cheek': 'skin_cheek',
            'cloth_base': 'cloth_brown',
            'cloth_mid': 'cloth_brown_mid',
            'cloth_shadow': 'cloth_brown_shadow' if 'cloth_brown_shadow' in COLOR_PALETTE else 'cloth_dark_brown',
            'eye': 'eye_brown',
            'outline': 'outline',
        },
        'features': ['simple_hair', 'neutral_eyes', 'slim_build'],
        'expressions': ['normal', 'happy', 'sad', 'surprised', 'angry'],
    },
    {
        'id': 'leishu',
        'name': '雷叔',
        'title': '铁匠',
        'description': '断臂的老匠人，暴躁外表下藏着温柔',
        'base_size': (32, 32),
        'output_size': (128, 128),
        'colors': {
            'hair_base': 'hair_gray',
            'hair_mid': 'hair_gray_mid',
            'hair_light': 'hair_gray_light',
            'hair_highlight': 'hair_gray_highlight',
            'skin_base': 'skin_dark',
            'skin_mid': 'skin_dark_mid',
            'skin_shadow': 'skin_dark_shadow',
            'cloth_base': 'cloth_dark_brown',
            'cloth_mid': 'cloth_dark_brown_mid',
            'apron_base': 'apron',
            'apron_mid': 'apron_mid',
            'eye': 'eye_hazel',
            'outline': 'outline',
        },
        'features': ['gray_hair', 'full_beard', 'apron', 'strong_build', 'wrinkles'],
        'expressions': ['normal', 'angry', 'happy', 'tired'],
    },
    {
        'id': 'jinling',
        'name': '金铃',
        'title': '商人',
        'description': '精明的女商人，爱财但守底线',
        'base_size': (32, 32),
        'output_size': (128, 128),
        'colors': {
            'hair_base': 'hair_gold',
            'hair_mid': 'hair_gold_mid',
            'hair_light': 'hair_gold_light',
            'hair_highlight': 'hair_gold_highlight',
            'skin_base': 'skin_light',
            'skin_mid': 'skin_light_mid',
            'skin_shadow': 'skin_light_shadow',
            'skin_cheek': 'skin_cheek',
            'cloth_base': 'cloth_red',
            'cloth_mid': 'cloth_red_mid',
            'cloth_accent': 'cloth_gold',
            'eye': 'eye_hazel',
            'outline': 'outline',
        },
        'features': ['long_flowy_hair', 'elegant_clothes', 'gold_accessories', 'slim_build'],
        'expressions': ['normal', 'smile', 'calculating', 'surprised'],
    },
    {
        'id': 'baizhi',
        'name': '白芷',
        'title': '医生',
        'description': '温柔的女医师，洞察力强',
        'base_size': (32, 32),
        'output_size': (128, 128),
        'colors': {
            'hair_base': 'hair_brown',
            'hair_mid': 'hair_brown_mid',
            'hair_light': 'hair_brown_light',
            'hair_highlight': 'hair_brown_highlight',
            'skin_base': 'skin_light',
            'skin_mid': 'skin_light_mid',
            'skin_shadow': 'skin_light_shadow',
            'skin_cheek': 'skin_cheek',
            'cloth_base': 'cloth_white',
            'cloth_mid': 'cloth_white_mid',
            'cloth_accent': 'cloth_green',
            'eye': 'eye_green',
            'outline': 'outline_soft',
        },
        'features': ['gentle_hair', 'kind_eyes', 'white_coat', 'slim_build', 'ponytail'],
        'expressions': ['normal', 'gentle_smile', 'concerned', 'sad'],
    },
    {
        'id': 'laojohn',
        'name': '老约翰',
        'title': '神父',
        'description': '神秘的祭司，说话爱打机锋',
        'base_size': (32, 32),
        'output_size': (128, 128),
        'colors': {
            'hair_base': 'hair_white',
            'hair_mid': 'hair_white_mid',
            'hair_light': 'hair_white_highlight',
            'skin_base': 'skin_pale',
            'skin_mid': 'skin_pale_mid',
            'skin_shadow': 'skin_pale_shadow',
            'cloth_base': 'cloth_black',
            'cloth_mid': 'cloth_black_mid',
            'cloth_accent': 'cloth_purple',
            'eye': 'eye_gray',
            'outline': 'outline',
        },
        'features': ['white_hair', 'long_beard', 'hood', 'robe', 'wrinkles', 'wise_eyes'],
        'expressions': ['normal', 'wise', 'mysterious', 'serious'],
    },
    {
        'id': 'daxiong',
        'name': '大熊',
        'title': '酒馆老板',
        'description': '豪爽的酒馆主人，善于倾听',
        'base_size': (32, 32),
        'output_size': (128, 128),
        'colors': {
            'hair_base': 'hair_dark_brown',
            'hair_mid': 'hair_dark_brown_mid',
            'hair_light': 'hair_dark_brown_light',
            'skin_base': 'skin_dark',
            'skin_mid': 'skin_dark_mid',
            'skin_shadow': 'skin_dark_shadow',
            'cloth_base': 'cloth_dark_red',
            'cloth_mid': 'cloth_dark_red_mid',
            'apron_base': 'apron',
            'apron_mid': 'apron_mid',
            'eye': 'eye_brown',
            'outline': 'outline',
        },
        'features': ['short_hair', 'full_beard', 'apron', 'very_strong_build', 'friendly'],
        'expressions': ['normal', 'laugh', 'serious', 'listening'],
    },
    {
        'id': 'ying',
        'name': '影',
        'title': '神秘人',
        'description': '独居的怪人，说话半真半假',
        'base_size': (32, 32),
        'output_size': (128, 128),
        'colors': {
            'hair_base': 'hair_black',
            'hair_mid': 'hair_black_mid',
            'skin_base': 'skin_pale',
            'skin_mid': 'skin_pale_mid',
            'skin_shadow': 'skin_pale_shadow',
            'cloth_base': 'cloth_black',
            'cloth_mid': 'cloth_black_mid',
            'cloak_base': 'cloth_dark_blue',
            'cloak_mid': 'cloth_dark_blue_mid',
            'eye': 'eye_gray',
            'outline': 'outline',
        },
        'features': ['hood', 'cloak', 'mysterious', 'hidden_face', 'slim_build'],
        'expressions': ['normal', 'cold', 'thinking', 'warning'],
    },
    {
        'id': 'xiaoan',
        'name': '小安',
        'title': '孩子',
        'description': '8 岁的可爱孩子，队长的遗孤',
        'base_size': (32, 32),
        'output_size': (128, 128),
        'colors': {
            'hair_base': 'hair_light_brown',
            'hair_mid': 'hair_light_brown_mid',
            'hair_light': 'hair_light_brown_light',
            'hair_highlight': 'hair_light_brown_highlight',
            'skin_base': 'skin_light',
            'skin_mid': 'skin_light_mid',
            'skin_shadow': 'skin_light_shadow',
            'skin_cheek': 'skin_cheek',
            'cloth_base': 'cloth_blue',
            'cloth_mid': 'cloth_blue_mid',
            'cloth_accent': 'cloth_white',
            'eye': 'eye_blue',
            'outline': 'outline_soft',
        },
        'features': ['small_body', 'big_eyes', 'childlike', 'innocent', 'messy_hair'],
        'expressions': ['normal', 'happy', 'curious', 'sad', 'excited'],
    },
    {
        'id': 'xiaohu',
        'name': '阿虎',
        'title': '守卫',
        'description': '年轻的村守卫队长，热血有责任感',
        'base_size': (32, 32),
        'output_size': (128, 128),
        'colors': {
            'hair_base': 'hair_black',
            'hair_mid': 'hair_black_mid',
            'hair_light': 'hair_black_light',
            'skin_base': 'skin_medium',
            'skin_mid': 'skin_medium_mid',
            'skin_shadow': 'skin_medium_shadow',
            'cloth_base': 'cloth_dark_blue',
            'cloth_mid': 'cloth_dark_blue_mid',
            'armor_base': 'metal_silver',
            'armor_mid': 'metal_silver_mid',
            'armor_highlight': 'metal_silver_highlight',
            'eye': 'eye_brown',
            'outline': 'outline',
        },
        'features': ['short_hair', 'armor', 'confident', 'young', 'strong_build'],
        'expressions': ['normal', 'determined', 'excited', 'serious'],
    },
    {
        'id': 'yeya',
        'name': '夜鸦',
        'title': '观察者',
        'description': '图书管理员/魔王卧底，冷静理性',
        'base_size': (32, 32),
        'output_size': (128, 128),
        'colors': {
            'hair_base': 'hair_black',
            'hair_mid': 'hair_black_mid',
            'hair_light': 'hair_black_light',
            'skin_base': 'skin_pale',
            'skin_mid': 'skin_pale_mid',
            'skin_shadow': 'skin_pale_shadow',
            'cloth_base': 'cloth_dark_green',
            'cloth_mid': 'cloth_dark_green_mid',
            'cloth_accent': 'cloth_brown',
            'eye': 'eye_purple',
            'outline': 'outline',
        },
        'features': ['glasses', 'scholar', 'calm', 'neat_hair', 'slim_build'],
        'expressions': ['normal', 'calm', 'thinking', 'conflicted'],
    },
]


def create_pixel_canvas(size, color=(0, 0, 0, 0)):
    """创建透明画布"""
    return Image.new('RGBA', size, color)


def draw_pixel(draw, x, y, color, size=1):
    """绘制单个像素（可放大）"""
    if isinstance(color, str):
        color = COLOR_PALETTE.get(color, COLOR_PALETTE['outline'])
    draw.rectangle([x*size, y*size, (x+1)*size-1, (y+1)*size-1], fill=color)


def draw_character_base(character, size=(128, 128), expression='normal'):
    """
    绘制角色的基础像素立绘 - 星露谷物语级别精细度
    使用 32x32 的设计网格，然后放大到目标尺寸
    """
    base_size = character.get('base_size', (32, 32))
    scale = size[0] // base_size[0]  # 缩放比例
    colors = character['colors']
    features = character.get('features', [])
    
    # 32x32 像素设计网格
    pixels = []
    
    # ========== 头发绘制（更精细的分层）==========
    
    # 头发顶层（高光）
    if 'long_flowy_hair' in features:
        # 长发飘逸（金铃）
        pixels.extend([
            # 顶部高光
            (14, 4, colors.get('hair_highlight')), (15, 4, colors.get('hair_highlight')),
            (16, 4, colors.get('hair_highlight')), (17, 4, colors.get('hair_highlight')),
            (14, 5, colors.get('hair_light')), (15, 5, colors.get('hair_light')),
            (16, 5, colors.get('hair_light')), (17, 5, colors.get('hair_light')),
        ])
    elif 'hood' in features:
        # 兜帽（影、老约翰）
        pixels.extend([
            (12, 3, colors.get('cloth_base')), (13, 3, colors.get('cloth_base')),
            (14, 3, colors.get('cloth_base')), (15, 3, colors.get('cloth_base')),
            (16, 3, colors.get('cloth_base')), (17, 3, colors.get('cloth_base')),
            (18, 3, colors.get('cloth_base')), (19, 3, colors.get('cloth_base')),
            (11, 4, colors.get('cloth_base')), (12, 4, colors.get('cloth_mid')),
            (13, 4, colors.get('cloth_mid')), (14, 4, colors.get('cloth_mid')),
            (15, 4, colors.get('cloth_mid')), (16, 4, colors.get('cloth_mid')),
            (17, 4, colors.get('cloth_mid')), (18, 4, colors.get('cloth_mid')),
            (19, 4, colors.get('cloth_mid')), (20, 4, colors.get('cloth_base')),
        ])
    elif 'gray_hair' in features or 'white_hair' in features:
        # 老年角色白发/灰发
        pixels.extend([
            (12, 4, colors.get('hair_light')), (13, 4, colors.get('hair_light')),
            (14, 4, colors.get('hair_light')), (15, 4, colors.get('hair_light')),
            (16, 4, colors.get('hair_light')), (17, 4, colors.get('hair_light')),
            (18, 4, colors.get('hair_light')), (19, 4, colors.get('hair_light')),
            (11, 5, colors.get('hair_mid')), (12, 5, colors.get('hair_mid')),
            (13, 5, colors.get('hair_mid')), (14, 5, colors.get('hair_mid')),
            (15, 5, colors.get('hair_mid')), (16, 5, colors.get('hair_mid')),
            (17, 5, colors.get('hair_mid')), (18, 5, colors.get('hair_mid')),
            (19, 5, colors.get('hair_mid')), (20, 5, colors.get('hair_mid')),
        ])
    elif 'messy_hair' in features:
        # 凌乱头发（小安）
        pixels.extend([
            (13, 4, colors.get('hair_light')), (14, 4, colors.get('hair_light')),
            (15, 4, colors.get('hair_light')), (16, 4, colors.get('hair_light')),
            (17, 4, colors.get('hair_light')), (18, 4, colors.get('hair_light')),
            (12, 5, colors.get('hair_mid')), (13, 5, colors.get('hair_mid')),
            (14, 5, colors.get('hair_mid')), (15, 5, colors.get('hair_mid')),
            (16, 5, colors.get('hair_mid')), (17, 5, colors.get('hair_mid')),
            (18, 5, colors.get('hair_mid')), (19, 5, colors.get('hair_mid')),
        ])
    else:
        # 标准发型
        pixels.extend([
            # 头发顶层
            (13, 4, colors.get('hair_light')), (14, 4, colors.get('hair_light')),
            (15, 4, colors.get('hair_light')), (16, 4, colors.get('hair_light')),
            (17, 4, colors.get('hair_light')), (18, 4, colors.get('hair_light')),
            # 头发中层
            (12, 5, colors.get('hair_mid')), (13, 5, colors.get('hair_mid')),
            (14, 5, colors.get('hair_mid')), (15, 5, colors.get('hair_mid')),
            (16, 5, colors.get('hair_mid')), (17, 5, colors.get('hair_mid')),
            (18, 5, colors.get('hair_mid')), (19, 5, colors.get('hair_mid')),
        ])
    
    # 头发两侧
    if 'ponytail' in features:
        # 马尾（白芷）
        pixels.extend([
            (11, 6, colors.get('hair_mid')), (11, 7, colors.get('hair_mid')),
            (11, 8, colors.get('hair_mid')), (11, 9, colors.get('hair_base')),
            (20, 6, colors.get('hair_mid')), (20, 7, colors.get('hair_mid')),
            (20, 8, colors.get('hair_mid')), (20, 9, colors.get('hair_base')),
        ])
    elif 'long_flowy_hair' in features:
        # 长发（金铃）
        pixels.extend([
            (11, 6, colors.get('hair_mid')), (11, 7, colors.get('hair_mid')),
            (11, 8, colors.get('hair_base')), (11, 9, colors.get('hair_base')),
            (11, 10, colors.get('hair_base')), (11, 11, colors.get('hair_base')),
            (20, 6, colors.get('hair_mid')), (20, 7, colors.get('hair_mid')),
            (20, 8, colors.get('hair_base')), (20, 9, colors.get('hair_base')),
            (20, 10, colors.get('hair_base')), (20, 11, colors.get('hair_base')),
        ])
    else:
        # 短发两侧
        pixels.extend([
            (11, 6, colors.get('hair_base')), (11, 7, colors.get('hair_base')),
            (11, 8, colors.get('hair_base')),
            (20, 6, colors.get('hair_base')), (20, 7, colors.get('hair_base')),
            (20, 8, colors.get('hair_base')),
        ])
    
    # ========== 脸部绘制 ==========
    
    # 脸型轮廓
    if 'small_body' in features:
        # 儿童小脸
        face_pixels = [
            (13, 7), (14, 7), (15, 7), (16, 7), (17, 7), (18, 7),
            (13, 8), (14, 8), (15, 8), (16, 8), (17, 8), (18, 8),
            (13, 9), (14, 9), (15, 9), (16, 9), (17, 9), (18, 9),
            (13, 10), (14, 10), (15, 10), (16, 10), (17, 10), (18, 10),
        ]
    else:
        # 标准脸型
        face_pixels = [
            (12, 7), (13, 7), (14, 7), (15, 7), (16, 7), (17, 7), (18, 7), (19, 7),
            (12, 8), (13, 8), (14, 8), (15, 8), (16, 8), (17, 8), (18, 8), (19, 8),
            (12, 9), (13, 9), (14, 9), (15, 9), (16, 9), (17, 9), (18, 9), (19, 9),
            (12, 10), (13, 10), (14, 10), (15, 10), (16, 10), (17, 10), (18, 10), (19, 10),
        ]
    
    for x, y in face_pixels:
        pixels.append((x, y, colors.get('skin_base')))
    
    # 脸颊红晕
    if 'skin_cheek' in colors:
        pixels.extend([
            (13, 9, colors.get('skin_cheek')), (14, 9, colors.get('skin_cheek')),
            (17, 9, colors.get('skin_cheek')), (18, 9, colors.get('skin_cheek')),
        ])
    
    # ========== 眼睛绘制（更精细）==========
    
    if 'big_eyes' in features:
        # 儿童大眼睛
        pixels.extend([
            # 左眼
            (13, 8, colors.get('outline')), (14, 8, colors.get('outline')),
            (15, 8, colors.get('outline')),
            (13, 9, colors.get('eye')), (14, 9, colors.get('eye')), (15, 9, colors.get('eye')),
            (14, 9, colors.get('eye_light') if 'eye_light' in colors else colors.get('skin_base')),  # 高光
            # 右眼
            (16, 8, colors.get('outline')), (17, 8, colors.get('outline')),
            (18, 8, colors.get('outline')),
            (16, 9, colors.get('eye')), (17, 9, colors.get('eye')), (18, 9, colors.get('eye')),
            (17, 9, colors.get('eye_light') if 'eye_light' in colors else colors.get('skin_base')),  # 高光
        ])
    elif 'glasses' in features:
        # 眼镜（夜鸦）
        pixels.extend([
            # 左眼镜框
            (13, 8, colors.get('outline')), (14, 8, colors.get('outline')),
            (15, 8, colors.get('outline')),
            (13, 9, colors.get('outline')), (13, 10, colors.get('outline')),
            (15, 9, colors.get('outline')), (15, 10, colors.get('outline')),
            (13, 10, colors.get('eye')), (14, 10, colors.get('eye')), (15, 10, colors.get('eye')),
            # 右眼镜框
            (16, 8, colors.get('outline')), (17, 8, colors.get('outline')),
            (18, 8, colors.get('outline')),
            (16, 9, colors.get('outline')), (16, 10, colors.get('outline')),
            (18, 9, colors.get('outline')), (18, 10, colors.get('outline')),
            (16, 10, colors.get('eye')), (17, 10, colors.get('eye')), (18, 10, colors.get('eye')),
            # 鼻梁
            (15, 9, colors.get('outline')), (16, 9, colors.get('outline')),
        ])
    elif 'wise_eyes' in features:
        # 智慧眼睛（老约翰）
        pixels.extend([
            (13, 8, colors.get('outline')), (14, 8, colors.get('outline')),
            (15, 8, colors.get('outline')),
            (13, 9, colors.get('eye')), (14, 9, colors.get('skin_base')), (15, 9, colors.get('eye')),
            (16, 8, colors.get('outline')), (17, 8, colors.get('outline')),
            (18, 8, colors.get('outline')),
            (16, 9, colors.get('eye')), (17, 9, colors.get('skin_base')), (18, 9, colors.get('eye')),
        ])
    elif 'hidden_face' in features:
        # 隐藏脸部（影）- 只有眼睛可见
        pixels.extend([
            (13, 9, colors.get('outline')), (14, 9, colors.get('outline')),
            (17, 9, colors.get('outline')), (18, 9, colors.get('outline')),
        ])
    else:
        # 标准眼睛
        pixels.extend([
            # 左眼
            (13, 8, colors.get('outline')), (14, 8, colors.get('outline')),
            (13, 9, colors.get('eye')), (14, 9, colors.get('eye')),
            # 右眼
            (17, 8, colors.get('outline')), (18, 8, colors.get('outline')),
            (17, 9, colors.get('eye')), (18, 9, colors.get('eye')),
        ])
    
    # ========== 眉毛 ==========
    if expression == 'angry' or expression == 'serious' or expression == 'determined':
        # 皱眉
        pixels.extend([
            (13, 7, colors.get('hair_base')), (14, 7, colors.get('hair_base')),
            (17, 7, colors.get('hair_base')), (18, 7, colors.get('hair_base')),
        ])
    elif expression == 'sad' or expression == 'concerned' or expression == 'conflicted':
        # 悲伤眉
        pixels.extend([
            (13, 7, colors.get('hair_base')),
            (18, 7, colors.get('hair_base')),
        ])
    elif expression == 'surprised' or expression == 'excited':
        # 惊讶眉（抬高）
        pixels.extend([
            (13, 6, colors.get('hair_base')), (14, 6, colors.get('hair_base')),
            (17, 6, colors.get('hair_base')), (18, 6, colors.get('hair_base')),
        ])
    
    # ========== 鼻子 ==========
    pixels.extend([
        (15, 9, colors.get('skin_shadow')),
        (15, 10, colors.get('skin_shadow')),
    ])
    
    # ========== 嘴巴（根据表情变化）==========
    mouth_pixels = []
    if expression == 'normal':
        mouth_pixels = [(15, 11, colors.get('skin_shadow'))]
    elif expression == 'happy' or expression == 'smile' or expression == 'gentle_smile':
        mouth_pixels = [
            (14, 11, 'cloth_red'), (15, 11, 'cloth_red'), (16, 11, 'cloth_red'),
            (13, 12, 'cloth_red'), (17, 12, 'cloth_red'),
        ]
    elif expression == 'laugh':
        mouth_pixels = [
            (13, 11, 'cloth_dark_red'), (14, 11, 'cloth_dark_red'),
            (15, 11, 'cloth_dark_red'), (16, 11, 'cloth_dark_red'), (17, 11, 'cloth_dark_red'),
            (14, 12, 'cloth_dark_red'), (15, 12, 'cloth_dark_red'), (16, 12, 'cloth_dark_red'),
        ]
    elif expression == 'sad' or expression == 'concerned':
        mouth_pixels = [(15, 12, colors.get('skin_shadow'))]
    elif expression == 'angry':
        mouth_pixels = [
            (14, 11, 'cloth_dark_red'), (15, 11, 'cloth_dark_red'), (16, 11, 'cloth_dark_red'),
        ]
    elif expression == 'surprised' or expression == 'excited':
        mouth_pixels = [(15, 11, 'cloth_black'), (14, 12, 'cloth_black'), (16, 12, 'cloth_black')]
    elif expression == 'calculating':
        mouth_pixels = [(15, 11, 'cloth_red')]
    elif expression == 'mysterious' or expression == 'wise':
        mouth_pixels = [(15, 11, colors.get('cloth_accent', colors.get('skin_shadow')))]
    elif expression == 'cold':
        mouth_pixels = [(15, 12, colors.get('skin_shadow'))]
    elif expression == 'thinking' or expression == 'conflicted':
        mouth_pixels = [(15, 11, colors.get('skin_shadow'))]
    elif expression == 'curious':
        mouth_pixels = [(15, 11, 'cloth_red')]
    elif expression == 'warning':
        mouth_pixels = [(14, 11, 'cloth_dark_red'), (15, 11, 'cloth_dark_red'), (16, 11, 'cloth_dark_red')]
    elif expression == 'tired':
        mouth_pixels = [(15, 12, colors.get('skin_shadow'))]
    elif expression == 'listening':
        mouth_pixels = [(15, 11, colors.get('skin_shadow'))]
    elif expression == 'determined':
        mouth_pixels = [(14, 11, colors.get('skin_shadow')), (15, 11, colors.get('skin_shadow')), (16, 11, colors.get('skin_shadow'))]
    
    pixels.extend([p for p in mouth_pixels if p])
    
    # ========== 胡须/胡子 ==========
    if 'full_beard' in features:
        pixels.extend([
            (12, 11, colors.get('hair_mid')), (13, 11, colors.get('hair_mid')),
            (14, 11, colors.get('hair_mid')), (15, 11, colors.get('hair_mid')),
            (16, 11, colors.get('hair_mid')), (17, 11, colors.get('hair_mid')),
            (18, 11, colors.get('hair_mid')), (19, 11, colors.get('hair_mid')),
            (12, 12, colors.get('hair_base')), (13, 12, colors.get('hair_base')),
            (14, 12, colors.get('hair_base')), (15, 12, colors.get('hair_base')),
            (16, 12, colors.get('hair_base')), (17, 12, colors.get('hair_base')),
            (18, 12, colors.get('hair_base')), (19, 12, colors.get('hair_base')),
        ])
    elif 'long_beard' in features:
        pixels.extend([
            (12, 11, colors.get('hair_mid')), (13, 11, colors.get('hair_mid')),
            (14, 11, colors.get('hair_mid')), (15, 11, colors.get('hair_mid')),
            (16, 11, colors.get('hair_mid')), (17, 11, colors.get('hair_mid')),
            (18, 11, colors.get('hair_mid')), (19, 11, colors.get('hair_mid')),
            (13, 12, colors.get('hair_base')), (14, 12, colors.get('hair_base')),
            (15, 12, colors.get('hair_base')), (16, 12, colors.get('hair_base')),
            (17, 12, colors.get('hair_base')), (18, 12, colors.get('hair_base')),
            (14, 13, colors.get('hair_base')), (15, 13, colors.get('hair_base')),
            (16, 13, colors.get('hair_base')), (17, 13, colors.get('hair_base')),
        ])
    
    # ========== 皱纹（老年角色）==========
    if 'wrinkles' in features:
        pixels.extend([
            (13, 7, colors.get('skin_shadow')), (18, 7, colors.get('skin_shadow')),
            (14, 10, colors.get('skin_shadow')), (17, 10, colors.get('skin_shadow')),
        ])
    
    # ========== 身体/衣服绘制 ==========
    
    if 'small_body' in features:
        # 儿童小身体
        pixels.extend([
            (12, 13, colors.get('cloth_base')), (13, 13, colors.get('cloth_base')),
            (14, 13, colors.get('cloth_base')), (15, 13, colors.get('cloth_base')),
            (16, 13, colors.get('cloth_base')), (17, 13, colors.get('cloth_base')),
            (18, 13, colors.get('cloth_base')), (19, 13, colors.get('cloth_base')),
            (12, 14, colors.get('cloth_base')), (13, 14, colors.get('cloth_base')),
            (14, 14, colors.get('cloth_base')), (15, 14, colors.get('cloth_base')),
            (16, 14, colors.get('cloth_base')), (17, 14, colors.get('cloth_base')),
            (18, 14, colors.get('cloth_base')), (19, 14, colors.get('cloth_base')),
            (12, 15, colors.get('cloth_base')), (13, 15, colors.get('cloth_base')),
            (14, 15, colors.get('cloth_base')), (15, 15, colors.get('cloth_base')),
            (16, 15, colors.get('cloth_base')), (17, 15, colors.get('cloth_base')),
            (18, 15, colors.get('cloth_base')), (19, 15, colors.get('cloth_base')),
        ])
    elif 'very_strong_build' in features:
        # 非常强壮体型（大熊）
        pixels.extend([
            (10, 13, colors.get('cloth_base')), (11, 13, colors.get('cloth_base')),
            (12, 13, colors.get('cloth_base')), (13, 13, colors.get('cloth_base')),
            (14, 13, colors.get('cloth_base')), (15, 13, colors.get('cloth_base')),
            (16, 13, colors.get('cloth_base')), (17, 13, colors.get('cloth_base')),
            (18, 13, colors.get('cloth_base')), (19, 13, colors.get('cloth_base')),
            (20, 13, colors.get('cloth_base')), (21, 13, colors.get('cloth_base')),
            (10, 14, colors.get('cloth_base')), (11, 14, colors.get('cloth_base')),
            (12, 14, colors.get('cloth_base')), (13, 14, colors.get('cloth_base')),
            (14, 14, colors.get('cloth_base')), (15, 14, colors.get('cloth_base')),
            (16, 14, colors.get('cloth_base')), (17, 14, colors.get('cloth_base')),
            (18, 14, colors.get('cloth_base')), (19, 14, colors.get('cloth_base')),
            (20, 14, colors.get('cloth_base')), (21, 14, colors.get('cloth_base')),
        ])
    elif 'apron' in features:
        # 围裙（雷叔、大熊）
        pixels.extend([
            (11, 13, colors.get('cloth_base')), (12, 13, colors.get('cloth_base')),
            (13, 13, colors.get('cloth_base')), (14, 13, colors.get('cloth_base')),
            (15, 13, colors.get('cloth_base')), (16, 13, colors.get('cloth_base')),
            (17, 13, colors.get('cloth_base')), (18, 13, colors.get('cloth_base')),
            (19, 13, colors.get('cloth_base')), (20, 13, colors.get('cloth_base')),
            (11, 14, colors.get('apron_base')), (12, 14, colors.get('apron_base')),
            (13, 14, colors.get('apron_base')), (14, 14, colors.get('apron_base')),
            (15, 14, colors.get('apron_base')), (16, 14, colors.get('apron_base')),
            (17, 14, colors.get('apron_base')), (18, 14, colors.get('apron_base')),
            (19, 14, colors.get('apron_base')), (20, 14, colors.get('apron_base')),
            (11, 15, colors.get('apron_base')), (12, 15, colors.get('apron_base')),
            (13, 15, colors.get('apron_base')), (14, 15, colors.get('apron_base')),
            (15, 15, colors.get('apron_base')), (16, 15, colors.get('apron_base')),
            (17, 15, colors.get('apron_base')), (18, 15, colors.get('apron_base')),
            (19, 15, colors.get('apron_base')), (20, 15, colors.get('apron_base')),
        ])
    elif 'armor' in features:
        # 盔甲（阿虎）
        pixels.extend([
            (11, 13, colors.get('armor_base')), (12, 13, colors.get('armor_base')),
            (13, 13, colors.get('armor_base')), (14, 13, colors.get('armor_base')),
            (15, 13, colors.get('armor_base')), (16, 13, colors.get('armor_base')),
            (17, 13, colors.get('armor_base')), (18, 13, colors.get('armor_base')),
            (19, 13, colors.get('armor_base')), (20, 13, colors.get('armor_base')),
            (11, 14, colors.get('armor_mid')), (12, 14, colors.get('armor_mid')),
            (13, 14, colors.get('cloth_base')), (14, 14, colors.get('cloth_base')),
            (15, 14, colors.get('cloth_base')), (16, 14, colors.get('cloth_base')),
            (17, 14, colors.get('cloth_base')), (18, 14, colors.get('cloth_base')),
            (19, 14, colors.get('armor_mid')), (20, 14, colors.get('armor_mid')),
        ])
    elif 'cloak' in features:
        # 斗篷（影）
        pixels.extend([
            (9, 13, colors.get('cloak_base')), (10, 13, colors.get('cloak_base')),
            (11, 13, colors.get('cloak_base')), (12, 13, colors.get('cloak_base')),
            (13, 13, colors.get('cloak_base')), (14, 13, colors.get('cloak_base')),
            (15, 13, colors.get('cloak_base')), (16, 13, colors.get('cloak_base')),
            (17, 13, colors.get('cloak_base')), (18, 13, colors.get('cloak_base')),
            (19, 13, colors.get('cloak_base')), (20, 13, colors.get('cloak_base')),
            (21, 13, colors.get('cloak_base')), (22, 13, colors.get('cloak_base')),
            (9, 14, colors.get('cloak_base')), (10, 14, colors.get('cloak_base')),
            (11, 14, colors.get('cloth_base')), (12, 14, colors.get('cloth_base')),
            (13, 14, colors.get('cloth_base')), (14, 14, colors.get('cloth_base')),
            (15, 14, colors.get('cloth_base')), (16, 14, colors.get('cloth_base')),
            (17, 14, colors.get('cloth_base')), (18, 14, colors.get('cloth_base')),
            (19, 14, colors.get('cloth_base')), (20, 14, colors.get('cloth_base')),
            (21, 14, colors.get('cloak_base')), (22, 14, colors.get('cloak_base')),
        ])
    elif 'white_coat' in features:
        # 白大褂（白芷）
        pixels.extend([
            (11, 13, colors.get('cloth_base')), (12, 13, colors.get('cloth_base')),
            (13, 13, colors.get('cloth_base')), (14, 13, colors.get('cloth_base')),
            (15, 13, colors.get('cloth_base')), (16, 13, colors.get('cloth_base')),
            (17, 13, colors.get('cloth_base')), (18, 13, colors.get('cloth_base')),
            (19, 13, colors.get('cloth_base')), (20, 13, colors.get('cloth_base')),
            (11, 14, colors.get('cloth_base')), (12, 14, colors.get('cloth_base')),
            (13, 14, colors.get('cloth_accent')), (14, 14, colors.get('cloth_base')),
            (15, 14, colors.get('cloth_base')), (16, 14, colors.get('cloth_base')),
            (17, 14, colors.get('cloth_accent')), (18, 14, colors.get('cloth_base')),
            (19, 14, colors.get('cloth_base')), (20, 14, colors.get('cloth_base')),
        ])
    else:
        # 标准身体
        pixels.extend([
            (11, 13, colors.get('cloth_base')), (12, 13, colors.get('cloth_base')),
            (13, 13, colors.get('cloth_base')), (14, 13, colors.get('cloth_base')),
            (15, 13, colors.get('cloth_base')), (16, 13, colors.get('cloth_base')),
            (17, 13, colors.get('cloth_base')), (18, 13, colors.get('cloth_base')),
            (19, 13, colors.get('cloth_base')), (20, 13, colors.get('cloth_base')),
            (11, 14, colors.get('cloth_base')), (12, 14, colors.get('cloth_base')),
            (13, 14, colors.get('cloth_base')), (14, 14, colors.get('cloth_base')),
            (15, 14, colors.get('cloth_base')), (16, 14, colors.get('cloth_base')),
            (17, 14, colors.get('cloth_base')), (18, 14, colors.get('cloth_base')),
            (19, 14, colors.get('cloth_base')), (20, 14, colors.get('cloth_base')),
        ])
    
    # 创建图像并绘制
    img = create_pixel_canvas(size)
    draw = ImageDraw.Draw(img)
    
    for pixel in pixels:
        if pixel is None:
            continue
        x, y, color_key = pixel
        # 处理颜色键
        if isinstance(color_key, tuple):
            color = color_key
        else:
            color = COLOR_PALETTE.get(color_key, COLOR_PALETTE['outline'])
        draw_pixel(draw, x, y, color, scale)
    
    return img


def generate_character_sprites(character, output_dir):
    """生成角色的所有表情变体"""
    os.makedirs(output_dir, exist_ok=True)
    
    char_id = character['id']
    expressions = character.get('expressions', ['normal', 'happy', 'sad', 'surprised', 'angry'])
    size = character.get('output_size', (128, 128))
    
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
    
    print("🎨 Demon Village Game - 10 位村民立绘生成 v2（星露谷物语级别）")
    print("=" * 70)
    
    # 生成色卡
    print("\n📋 生成色卡...")
    generate_pixel_test_pattern(output_base)
    
    # 生成所有角色
    for character in ALL_CHARACTERS:
        generate_character_sprites(character, output_base)
    
    print("\n" + "=" * 70)
    print("✅ 所有角色立绘生成完成！")
    print(f"📁 输出目录：{output_base}")
    
    # 生成资源清单
    generate_resource_manifest(output_base)


def generate_pixel_test_pattern(output_dir):
    """生成像素测试图案（色卡和网格）"""
    os.makedirs(output_dir, exist_ok=True)
    
    # 色卡 - 分组显示
    color_card = Image.new('RGBA', (500, 400), (50, 50, 50))
    draw = ImageDraw.Draw(color_card)
    
    # 绘制色板分组
    groups = [
        ('皮肤色', [k for k in COLOR_PALETTE.keys() if k.startswith('skin_')]),
        ('头发色', [k for k in COLOR_PALETTE.keys() if k.startswith('hair_')]),
        ('衣服色', [k for k in COLOR_PALETTE.keys() if k.startswith('cloth_')]),
        ('特殊材质', [k for k in COLOR_PALETTE.keys() if k.startswith(('metal_', 'leather', 'apron'))]),
        ('眼睛色', [k for k in COLOR_PALETTE.keys() if k.startswith('eye_')]),
    ]
    
    y_offset = 10
    for group_name, color_keys in groups:
        # 绘制组名
        draw.text((10, y_offset), group_name, fill=(255, 255, 255))
        y_offset += 20
        
        x, y = 10, y_offset
        for key in color_keys[:12]:  # 每组最多显示 12 个颜色
            color = COLOR_PALETTE.get(key, (128, 128, 128))
            draw.rectangle([x, y, x+25, y+25], fill=color)
            draw.rectangle([x, y, x+25, y+25], outline=(255, 255, 255), width=1)
            x += 30
            if x > 460:
                x = 10
                y += 30
        
        y_offset = y + 40
    
    color_card.save(os.path.join(output_dir, 'color_palette.png'), 'PNG')


def generate_resource_manifest(output_dir):
    """生成资源清单文件"""
    manifest_path = os.path.join(output_dir, 'CHARACTERS_MANIFEST.md')
    
    with open(manifest_path, 'w', encoding='utf-8') as f:
        f.write("# 🎭 角色立绘资源清单 v2\n\n")
        f.write("*星露谷物语级别精细度 - Demon Village Game 美术资源*\n\n")
        f.write("---\n\n")
        
        f.write("## 📊 总览\n\n")
        f.write(f"- **角色数量**: {len(ALL_CHARACTERS)}\n")
        f.write(f"- **基础设计**: 32x32 像素\n")
        f.write(f"- **输出尺寸**: 128x128 像素\n")
        f.write(f"- **表情数量**: 每个角色 3-5 个表情\n")
        f.write(f"- **格式**: PNG (透明背景)\n")
        f.write(f"- **色板颜色**: {len(COLOR_PALETTE)} 种（含渐变）\n\n")
        
        f.write("## 🎨 精细度对比\n\n")
        f.write("| 版本 | 基础网格 | 输出尺寸 | 细节程度 |\n")
        f.write("|------|----------|----------|----------|\n")
        f.write("| v1 | 16x16 | 64x64 | 基础（我的世界级别） |\n")
        f.write("| v2 | 32x32 | 128x128 | 精细（星露谷物语级别） |\n\n")
        
        f.write("## 👥 角色列表\n\n")
        
        for char in ALL_CHARACTERS:
            f.write(f"### {char['name']} - {char['title']}\n\n")
            f.write(f"- **ID**: `{char['id']}`\n")
            f.write(f"- **描述**: {char['description']}\n")
            f.write(f"- **表情**: {', '.join(char.get('expressions', []))}\n")
            f.write(f"- **特征**: {', '.join(char.get('features', []))}\n")
            f.write(f"- **尺寸**: {char.get('output_size', (128, 128))}\n\n")
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
            f.write(f"├── {char['id']}_{char['expressions'][0]}.png\n")
            f.write(f"├── {char['id']}_spritesheet.png\n")
        f.write("```\n\n")
        
        f.write("## 🎨 色板分类\n\n")
        f.write("| 类别 | 颜色数量 | 说明 |\n")
        f.write("|------|----------|------|\n")
        f.write("| 皮肤色 | 13 | 3 阶渐变 + 腮红 |\n")
        f.write("| 头发色 | 24 | 4 阶渐变（基础/中/浅/高光） |\n")
        f.write("| 衣服色 | 36 | 3 阶渐变 |\n")
        f.write("| 眼睛色 | 12 | 基础 + 浅色 |\n")
        f.write("| 特殊材质 | 12 | 金属/皮革/围裙等 |\n")
    
    print(f"📋 已生成资源清单：CHARACTERS_MANIFEST.md")


if __name__ == '__main__':
    generate_all_characters()
