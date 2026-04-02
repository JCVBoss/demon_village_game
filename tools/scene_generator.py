#!/usr/bin/env python3
"""
场景生成工具 - Demon Village Game
生成村庄场景、森林场景等背景美术资源
规格：1280x720 像素，像素风格
"""

from PIL import Image, ImageDraw
import os

# 输出目录
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '../code/assets/sprites/backgrounds')
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 画布尺寸
WIDTH, HEIGHT = 1280, 720

# 暮色村主题色板
SCENE_COLORS = {
    # 天空 - 白天
    'sky_day_top': (135, 206, 235),
    'sky_day_mid': (176, 224, 230),
    'sky_day_bottom': (210, 240, 245),
    
    # 天空 - 黄昏（主题色）
    'sky_twilight_top': (70, 50, 90),
    'sky_twilight_mid': (120, 80, 120),
    'sky_twilight_bottom': (180, 120, 140),
    'sunset_glow': (255, 180, 100),
    
    # 天空 - 夜晚
    'sky_night_top': (15, 10, 30),
    'sky_night_mid': (25, 20, 45),
    'sky_night_bottom': (40, 35, 65),
    'moon': (248, 248, 250),
    'star': (255, 255, 220),
    
    # 地面
    'grass_light': (120, 180, 80),
    'grass_mid': (100, 160, 65),
    'grass_dark': (80, 140, 50),
    'grass_shadow': (60, 110, 40),
    
    'dirt_light': (140, 110, 70),
    'dirt_mid': (120, 90, 55),
    'dirt_dark': (100, 75, 45),
    
    'stone_light': (160, 160, 165),
    'stone_mid': (130, 130, 135),
    'stone_dark': (100, 100, 105),
    
    # 树木
    'tree_trunk': (80, 55, 35),
    'tree_trunk_dark': (60, 40, 25),
    'tree_leaves_light': (60, 120, 50),
    'tree_leaves_mid': (45, 100, 35),
    'tree_leaves_dark': (30, 80, 25),
    
    # 建筑
    'wood_light': (180, 140, 100),
    'wood_mid': (150, 110, 70),
    'wood_dark': (120, 85, 50),
    'roof_thatch': (200, 180, 120),
    'roof_tile': (140, 60, 50),
    
    # 水
    'water_light': (100, 180, 220),
    'water_mid': (70, 150, 200),
    'water_dark': (50, 120, 170),
    
    # 光效
    'light_warm': (255, 230, 180),
    'light_cool': (200, 220, 255),
}


def create_gradient(draw, colors, vertical=True):
    """创建渐变背景"""
    if vertical:
        for y in range(HEIGHT):
            ratio = y / HEIGHT
            color_idx = int(ratio * (len(colors) - 1))
            color = colors[min(color_idx, len(colors) - 1)]
            draw.line([(0, y), (WIDTH, y)], fill=color)
    else:
        for x in range(WIDTH):
            ratio = x / WIDTH
            color_idx = int(ratio * (len(colors) - 1))
            color = colors[min(color_idx, len(colors) - 1)]
            draw.line([(x, 0), (x, HEIGHT)], fill=color)


def draw_ground(draw, ground_y):
    """绘制地面"""
    # 草地渐变
    for y in range(ground_y, HEIGHT):
        ratio = (y - ground_y) / (HEIGHT - ground_y)
        if ratio < 0.3:
            color = SCENE_COLORS['grass_light']
        elif ratio < 0.6:
            color = SCENE_COLORS['grass_mid']
        elif ratio < 0.8:
            color = SCENE_COLORS['grass_dark']
        else:
            color = SCENE_COLORS['grass_shadow']
        draw.line([(0, y), (WIDTH, y)], fill=color)


def draw_tree(draw, x, y, size=1.0):
    """绘制像素风格树木"""
    trunk_width = int(20 * size)
    trunk_height = int(60 * size)
    leaves_radius = int(50 * size)
    
    # 树干
    trunk_color = SCENE_COLORS['tree_trunk']
    trunk_dark = SCENE_COLORS['tree_trunk_dark']
    draw.rectangle([x - trunk_width//2, y, x + trunk_width//2, y + trunk_height], fill=trunk_color)
    # 树干阴影
    draw.rectangle([x + trunk_width//4, y, x + trunk_width//2, y + trunk_height], fill=trunk_dark)
    
    # 树叶（圆形分层）
    leaves_colors = [
        SCENE_COLORS['tree_leaves_light'],
        SCENE_COLORS['tree_leaves_mid'],
        SCENE_COLORS['tree_leaves_dark']
    ]
    
    for i, color in enumerate(leaves_colors):
        offset = i * 8
        draw.ellipse([
            x - leaves_radius + offset,
            y - leaves_radius - trunk_height//2 + offset,
            x + leaves_radius + offset,
            y + leaves_radius - trunk_height//2 + offset
        ], fill=color)


def draw_house(draw, x, y, width=120, height=80):
    """绘制像素风格房屋"""
    # 墙体
    wall_light = SCENE_COLORS['wood_light']
    wall_mid = SCENE_COLORS['wood_mid']
    wall_dark = SCENE_COLORS['wood_dark']
    
    # 墙体主体
    draw.rectangle([x, y, x + width, y + height], fill=wall_mid)
    # 墙体木板纹理
    for i in range(0, height, 15):
        draw.line([(x, y + i), (x + width, y + i)], fill=wall_dark)
        # 木板阴影
        draw.line([(x, y + i + 1), (x + width, y + i + 1)], fill=wall_dark)
    
    # 屋顶（三角形）
    roof_color = SCENE_COLORS['roof_thatch']
    roof_dark = SCENE_COLORS['roof_tile']
    roof_points = [
        (x - 10, y),
        (x + width + 10, y),
        (x + width // 2, y - 50)
    ]
    draw.polygon(roof_points, fill=roof_color)
    # 屋顶纹理
    for i in range(0, 50, 10):
        y_line = y - i
        x_left = x - 10 + i // 5
        x_right = x + width + 10 - i // 5
        draw.line([(x_left, y_line), (x_right, y_line)], fill=roof_dark)
    
    # 门
    door_color = SCENE_COLORS['wood_dark']
    door_width = width // 4
    door_height = height // 2
    draw.rectangle([
        x + width // 2 - door_width // 2,
        y + height - door_height,
        x + width // 2 + door_width // 2,
        y + height
    ], fill=door_color)
    
    # 窗户
    window_color = (180, 200, 255)  # 玻璃色
    window_size = 20
    window_y = y + height // 3
    # 左窗
    draw.rectangle([
        x + 15, window_y,
        x + 15 + window_size, window_y + window_size
    ], fill=window_color)
    # 右窗
    draw.rectangle([
        x + width - 15 - window_size, window_y,
        x + width - 15, window_y + window_size
    ], fill=window_color)


def draw_village_scene(variant='day'):
    """绘制村庄场景"""
    img = Image.new('RGB', (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(img)
    
    # 1. 绘制天空
    if variant == 'day':
        sky_colors = [
            SCENE_COLORS['sky_day_top'],
            SCENE_COLORS['sky_day_mid'],
            SCENE_COLORS['sky_day_bottom']
        ]
    elif variant == 'twilight':
        sky_colors = [
            SCENE_COLORS['sky_twilight_top'],
            SCENE_COLORS['sky_twilight_mid'],
            SCENE_COLORS['sky_twilight_bottom']
        ]
    else:  # night
        sky_colors = [
            SCENE_COLORS['sky_night_top'],
            SCENE_COLORS['sky_night_mid'],
            SCENE_COLORS['sky_night_bottom']
        ]
    
    create_gradient(draw, sky_colors, vertical=True)
    
    # 2. 绘制太阳/月亮
    if variant == 'day':
        # 太阳
        sun_color = (255, 240, 180)
        draw.ellipse([WIDTH - 150, 80, WIDTH - 50, 180], fill=sun_color)
    elif variant == 'twilight':
        # 夕阳
        sunset_color = SCENE_COLORS['sunset_glow']
        draw.ellipse([WIDTH // 2 - 80, HEIGHT // 2 - 100, WIDTH // 2 + 80, HEIGHT // 2 + 20], fill=sunset_color)
        # 晚霞
        for i in range(5):
            alpha = 100 - i * 15
            glow_color = (255, 180 - i * 10, 100 - i * 5)
            draw.ellipse([
                WIDTH // 2 - 100 - i * 20,
                HEIGHT // 2 - 120 - i * 10,
                WIDTH // 2 + 100 + i * 20,
                HEIGHT // 2 + 40 + i * 5
            ], fill=glow_color)
    else:  # night
        # 月亮
        moon_color = SCENE_COLORS['moon']
        draw.ellipse([WIDTH - 180, 60, WIDTH - 100, 140], fill=moon_color)
        # 星星
        import random
        random.seed(42)  # 固定种子保证一致性
        for _ in range(50):
            star_x = random.randint(0, WIDTH)
            star_y = random.randint(0, HEIGHT // 2)
            star_size = random.randint(2, 4)
            draw.rectangle([
                star_x, star_y,
                star_x + star_size, star_y + star_size
            ], fill=SCENE_COLORS['star'])
    
    # 3. 绘制地面
    ground_y = HEIGHT * 2 // 3
    draw_ground(draw, ground_y)
    
    # 4. 绘制村庄建筑
    house_positions = [
        (100, ground_y - 60),
        (300, ground_y - 80),
        (550, ground_y - 70),
        (800, ground_y - 90),
        (1050, ground_y - 65),
    ]
    
    for hx, hy in house_positions:
        draw_house(draw, hx, hy)
    
    # 5. 绘制树木
    tree_positions = [
        (50, ground_y - 20, 1.2),
        (250, ground_y - 30, 0.9),
        (480, ground_y - 25, 1.1),
        (720, ground_y - 35, 1.0),
        (950, ground_y - 20, 1.3),
        (1200, ground_y - 30, 0.8),
    ]
    
    for tx, ty, size in tree_positions:
        draw_tree(draw, tx, ty, size)
    
    # 6. 绘制道路
    road_y = ground_y + 20
    road_color = SCENE_COLORS['dirt_mid']
    road_dark = SCENE_COLORS['dirt_dark']
    draw.rectangle([0, road_y, WIDTH, road_y + 60], fill=road_color)
    # 道路纹理
    for i in range(0, WIDTH, 40):
        draw.rectangle([i, road_y + 10, i + 20, road_y + 50], fill=road_dark)
    
    # 7. 特殊效果
    if variant == 'twilight':
        # 黄昏光晕
        for i in range(20):
            alpha = 30 - i
            glow_color = (255, 200 - i * 3, 150 - i * 2)
            draw.ellipse([
                WIDTH // 2 - 200 - i * 10,
                HEIGHT // 2 - 150 - i * 5,
                WIDTH // 2 + 200 + i * 10,
                HEIGHT // 2 + 100 + i * 3
            ], fill=glow_color)
    elif variant == 'night':
        # 房屋灯光
        for hx, hy in house_positions:
            # 窗户透光
            window_y = hy + 25
            light_color = SCENE_COLORS['light_warm']
            draw.rectangle([hx + 15, window_y, hx + 35, window_y + 20], fill=light_color)
            draw.rectangle([hx + 85, window_y, hx + 105, window_y + 20], fill=light_color)
    
    # 保存
    filename = f"village_{variant}.png"
    filepath = os.path.join(OUTPUT_DIR, filename)
    img.save(filepath)
    print(f"✅ 已生成：{filepath}")
    return filepath


def generate_all_village_scenes():
    """生成所有村庄场景变体"""
    print("🎨 开始生成村庄场景...")
    print(f"📁 输出目录：{OUTPUT_DIR}")
    print(f"📐 尺寸：{WIDTH}x{HEIGHT}")
    print()
    
    scenes = ['day', 'twilight', 'night']
    for variant in scenes:
        draw_village_scene(variant)
    
    print()
    print("✅ 村庄场景生成完成！")


if __name__ == '__main__':
    generate_all_village_scenes()
