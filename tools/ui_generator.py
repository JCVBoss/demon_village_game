#!/usr/bin/env python3
"""
UI 素材生成工具 - Demon Village Game
生成对话框、按钮、图标等 UI 元素
规格：PNG 格式，支持透明背景
"""

from PIL import Image, ImageDraw
import os

# 输出目录
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '../code/assets/sprites/ui')
os.makedirs(OUTPUT_DIR, exist_ok=True)

# UI 主题色板 - 暮色村风格（暗色调，中世纪奇幻）
UI_COLORS = {
    # 主色调
    'primary_dark': (45, 40, 55),
    'primary_mid': (65, 58, 75),
    'primary_light': (85, 76, 98),
    
    # 边框
    'border_gold': (200, 175, 100),
    'border_gold_light': (230, 210, 150),
    'border_dark': (35, 30, 45),
    
    # 文本
    'text_light': (250, 245, 240),
    'text_dim': (180, 175, 170),
    'text_highlight': (255, 220, 150),
    
    # 按钮
    'button_bg': (70, 65, 85),
    'button_hover': (95, 88, 115),
    'button_pressed': (55, 50, 70),
    'button_border': (140, 120, 90),
    
    # 进度条
    'progress_bg': (40, 35, 50),
    'progress_fill': (120, 180, 80),
    'progress_low': (180, 80, 60),
    'progress_mid': (200, 160, 60),
    'progress_high': (100, 180, 100),
    
    # 信任值
    'trust_low': (180, 80, 80),
    'trust_mid': (200, 160, 60),
    'trust_high': (80, 180, 100),
    
    # 背景
    'panel_bg': (50, 45, 65, 240),
    'panel_border': (90, 80, 110),
    
    # 图标
    'icon_gold': (220, 190, 100),
    'icon_silver': (180, 180, 190),
    'icon_bronze': (160, 120, 80),
}


def draw_rounded_rect(draw, bbox, radius, fill, outline=None, width=1):
    """绘制圆角矩形"""
    x1, y1, x2, y2 = bbox
    
    # 主体矩形
    draw.rectangle([x1 + radius, y1, x2 - radius, y2], fill=fill)
    draw.rectangle([x1, y1 + radius, x2, y2 - radius], fill=fill)
    
    # 四个圆角
    draw.pieslice([x1, y1, x1 + radius * 2, y1 + radius * 2], start=180, end=270, fill=fill)
    draw.pieslice([x2 - radius * 2, y1, x2, y1 + radius * 2], start=270, end=360, fill=fill)
    draw.pieslice([x1, y2 - radius * 2, x1 + radius * 2, y2], start=90, end=180, fill=fill)
    draw.pieslice([x2 - radius * 2, y2 - radius * 2, x2, y2], start=0, end=90, fill=fill)
    
    # 边框
    if outline:
        for i in range(width):
            inset = i
            draw.arc([x1 + inset, y1 + inset, x1 + radius * 2 - inset, y1 + radius * 2 - inset], start=180, end=270, fill=outline)
            draw.arc([x2 - radius * 2 + inset, y1 + inset, x2 - inset, y1 + radius * 2 - inset], start=270, end=360, fill=outline)
            draw.arc([x1 + inset, y2 - radius * 2 + inset, x1 + radius * 2 - inset, y2 - inset], start=90, end=180, fill=outline)
            draw.arc([x2 - radius * 2 + inset, y2 - radius * 2 + inset, x2 - inset, y2 - inset], start=0, end=90, fill=outline)
            draw.line([x1 + radius, y1 + inset, x2 - radius, y1 + inset], fill=outline)
            draw.line([x1 + radius, y2 - inset, x2 - radius, y2 - inset], fill=outline)
            draw.line([x1 + inset, y1 + radius, x1 + inset, y2 - radius], fill=outline)
            draw.line([x2 - inset, y1 + radius, x2 - inset, y2 - radius], fill=outline)


def generate_dialogue_box():
    """生成对话框背景"""
    print("  → 生成对话框...")
    
    # 主对话框（大）
    width, height = 800, 180
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 背景
    draw_rounded_rect(draw, [2, 2, width - 2, height - 2], 15, UI_COLORS['panel_bg'])
    
    # 边框
    draw_rounded_rect(draw, [0, 0, width, height], 15, None, outline=UI_COLORS['border_gold'], width=2)
    draw_rounded_rect(draw, [3, 3, width - 3, height - 3], 13, None, outline=UI_COLORS['border_dark'], width=1)
    
    # 装饰角
    corner_size = 20
    # 左上角
    draw.pieslice([0, 0, corner_size, corner_size], start=180, end=270, fill=UI_COLORS['border_gold'])
    # 右上角
    draw.pieslice([width - corner_size, 0, width, corner_size], start=270, end=360, fill=UI_COLORS['border_gold'])
    # 左下角
    draw.pieslice([0, height - corner_size, corner_size, height], start=90, end=180, fill=UI_COLORS['border_gold'])
    # 右下角
    draw.pieslice([width - corner_size, height - corner_size, width, height], start=0, end=90, fill=UI_COLORS['border_gold'])
    
    img.save(os.path.join(OUTPUT_DIR, 'dialogue_box.png'))
    
    # 小对话框（用于 NPC 对话）
    width, height = 500, 120
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    draw_rounded_rect(draw, [2, 2, width - 2, height - 2], 12, UI_COLORS['panel_bg'])
    draw_rounded_rect(draw, [0, 0, width, height], 12, None, outline=UI_COLORS['border_gold'], width=2)
    
    img.save(os.path.join(OUTPUT_DIR, 'dialogue_box_small.png'))
    
    print("    ✓ dialogue_box.png (800x180)")
    print("    ✓ dialogue_box_small.png (500x120)")


def generate_buttons():
    """生成按钮"""
    print("  → 生成按钮...")
    
    button_sizes = [
        ('button_large', 200, 50),
        ('button_medium', 150, 45),
        ('button_small', 100, 40),
    ]
    
    for name, width, height in button_sizes:
        # 正常状态
        img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        draw_rounded_rect(draw, [0, 0, width, height], 8, UI_COLORS['button_bg'])
        draw_rounded_rect(draw, [1, 1, width - 1, height - 1], 7, None, outline=UI_COLORS['button_border'], width=1)
        
        img.save(os.path.join(OUTPUT_DIR, f'{name}.png'))
        
        # 悬停状态
        img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        draw_rounded_rect(draw, [0, 0, width, height], 8, UI_COLORS['button_hover'])
        draw_rounded_rect(draw, [1, 1, width - 1, height - 1], 7, None, outline=UI_COLORS['border_gold_light'], width=1)
        
        img.save(os.path.join(OUTPUT_DIR, f'{name}_hover.png'))
        
        # 按下状态
        img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        draw_rounded_rect(draw, [0, 0, width, height], 8, UI_COLORS['button_pressed'])
        draw_rounded_rect(draw, [1, 1, width - 1, height - 1], 7, None, outline=UI_COLORS['button_border'], width=1)
        
        img.save(os.path.join(OUTPUT_DIR, f'{name}_pressed.png'))
        
        print(f"    ✓ {name}.png ({width}x{height}) - 3 states")


def generate_progress_bars():
    """生成进度条"""
    print("  → 生成进度条...")
    
    width, height = 200, 20
    
    # 空进度条背景
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    draw_rounded_rect(draw, [0, 0, width, height], 10, UI_COLORS['progress_bg'])
    draw_rounded_rect(draw, [0, 0, width, height], 10, None, outline=UI_COLORS['border_dark'], width=1)
    
    img.save(os.path.join(OUTPUT_DIR, 'progress_bar_bg.png'))
    
    # 进度条填充（不同状态）
    fills = [
        ('progress_fill_low', UI_COLORS['progress_low'], 30),
        ('progress_fill_mid', UI_COLORS['progress_mid'], 60),
        ('progress_fill_high', UI_COLORS['progress_high'], 100),
    ]
    
    for name, color, fill_width in fills:
        img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        actual_width = int(width * fill_width / 100) - 4
        draw_rounded_rect(draw, [2, 2, 2 + actual_width, height - 2], 8, color)
        
        img.save(os.path.join(OUTPUT_DIR, f'{name}.png'))
        print(f"    ✓ {name}.png ({actual_width}x{height})")


def generate_trust_indicator():
    """生成信任值指示器"""
    print("  → 生成信任值指示器...")
    
    # 心形图标
    size = 32
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 绘制心形
    center_x, center_y = size // 2, size // 2
    
    # 心形路径
    heart_color = UI_COLORS['trust_high']
    points = []
    for angle in range(0, 360, 5):
        import math
        rad = math.radians(angle)
        # 心形公式
        x = 16 * (math.sin(rad) ** 3)
        y = -(13 * math.cos(rad) - 5 * math.cos(2 * rad) - 2 * math.cos(3 * rad) - math.cos(4 * rad))
        points.append((center_x + x, center_y + y + 2))
    
    draw.polygon(points, fill=heart_color)
    draw.polygon(points, outline=UI_COLORS['border_dark'], width=1)
    
    img.save(os.path.join(OUTPUT_DIR, 'trust_heart.png'))
    print(f"    ✓ trust_heart.png ({size}x{size})")
    
    # 信任条
    width, height = 100, 12
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 背景
    draw_rounded_rect(draw, [0, 0, width, height], 6, UI_COLORS['progress_bg'])
    
    # 填充（渐变）
    for x in range(width - 2):
        ratio = x / (width - 2)
        if ratio < 0.33:
            color = UI_COLORS['trust_low']
        elif ratio < 0.66:
            color = UI_COLORS['trust_mid']
        else:
            color = UI_COLORS['trust_high']
        draw.line([(x + 1, 1), (x + 1, height - 1)], fill=color)
    
    img.save(os.path.join(OUTPUT_DIR, 'trust_bar.png'))
    print(f"    ✓ trust_bar.png ({width}x{height})")


def generate_icons():
    """生成图标"""
    print("  → 生成图标...")
    
    size = 32
    
    # 设置图标
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    # 齿轮形状
    draw.ellipse([8, 8, 24, 24], fill=UI_COLORS['icon_gold'])
    draw.ellipse([12, 12, 20, 20], fill=UI_COLORS['panel_bg'])
    img.save(os.path.join(OUTPUT_DIR, 'icon_settings.png'))
    
    # 保存图标
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rectangle([10, 10, 22, 24], fill=UI_COLORS['icon_bronze'])
    draw.polygon([(16, 6), (10, 12), (22, 12)], fill=UI_COLORS['icon_bronze'])
    img.save(os.path.join(OUTPUT_DIR, 'icon_save.png'))
    
    # 加载图标
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.arc([8, 8, 24, 24], start=0, end=270, fill=UI_COLORS['icon_silver'], width=3)
    draw.polygon([(16, 10), (12, 16), (16, 14), (20, 18), (18, 16), (16, 12)], fill=UI_COLORS['icon_silver'])
    img.save(os.path.join(OUTPUT_DIR, 'icon_load.png'))
    
    # 对话图标
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse([6, 8, 26, 24], fill=UI_COLORS['icon_gold'])
    draw.polygon([(14, 22), (10, 28), (18, 24)], fill=UI_COLORS['icon_gold'])
    img.save(os.path.join(OUTPUT_DIR, 'icon_dialogue.png'))
    
    # 地图图标
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.polygon([(8, 10), (16, 6), (24, 10), (24, 24), (16, 20), (8, 24)], fill=UI_COLORS['icon_bronze'])
    img.save(os.path.join(OUTPUT_DIR, 'icon_map.png'))
    
    print(f"    ✓ icon_settings.png ({size}x{size})")
    print(f"    ✓ icon_save.png ({size}x{size})")
    print(f"    ✓ icon_load.png ({size}x{size})")
    print(f"    ✓ icon_dialogue.png ({size}x{size})")
    print(f"    ✓ icon_map.png ({size}x{size})")


def generate_menu_panel():
    """生成菜单面板"""
    print("  → 生成菜单面板...")
    
    width, height = 400, 300
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 背景
    draw_rounded_rect(draw, [0, 0, width, height], 20, UI_COLORS['panel_bg'])
    
    # 边框
    draw_rounded_rect(draw, [2, 2, width - 2, height - 2], 18, None, outline=UI_COLORS['border_gold'], width=2)
    draw_rounded_rect(draw, [5, 5, width - 5, height - 5], 16, None, outline=UI_COLORS['border_dark'], width=1)
    
    # 装饰
    # 顶部装饰线
    draw.line([(20, 35), (width - 20, 35)], fill=UI_COLORS['border_gold'])
    
    img.save(os.path.join(OUTPUT_DIR, 'menu_panel.png'))
    print(f"    ✓ menu_panel.png ({width}x{height})")


def generate_all_ui():
    """生成所有 UI 素材"""
    print("🎨 开始生成 UI 素材包...")
    print(f"📁 输出目录：{OUTPUT_DIR}")
    print()
    
    generate_dialogue_box()
    print()
    generate_buttons()
    print()
    generate_progress_bars()
    print()
    generate_trust_indicator()
    print()
    generate_icons()
    print()
    generate_menu_panel()
    print()
    
    print("✅ UI 素材包生成完成！")


if __name__ == '__main__':
    generate_all_ui()
