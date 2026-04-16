#!/usr/bin/env python3
"""
生成星露谷风格的建筑和装饰物 Sprite
采用伪 3D 斜角视角（45°俯视）
"""

from PIL import Image, ImageDraw
import math

# ==================== 建筑生成 ====================

def create_isometric_building(width, height, roof_height, wall_color, roof_color, 
                               has_chimney=False, has_steeple=False, has_sign=False):
    """
    创建伪 3D 斜角视角的建筑
    
    参数:
    - width: 建筑正面宽度
    - height: 建筑总高度（含屋顶）
    - roof_height: 屋顶高度
    - wall_color: 墙壁颜色 (R,G,B)
    - roof_color: 屋顶颜色 (R,G,B)
    - has_chimney: 是否有烟囱
    - has_steeple: 是否有尖塔
    - has_sign: 是否有招牌
    """
    
    # 创建透明背景
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 计算透视偏移（45°斜角）
    depth_offset = width // 4  # 深度偏移量
    
    # ==================== 墙壁（正面） ====================
    wall_top = roof_height
    wall_bottom = height
    
    # 正面墙壁
    front_wall_points = [
        (0, wall_top),
        (width, wall_top),
        (width, wall_bottom),
        (0, wall_bottom)
    ]
    
    # 墙壁侧面（右侧，呈现立体感）
    side_wall_points = [
        (width, wall_top),
        (width + depth_offset, wall_top - depth_offset // 2),
        (width + depth_offset, wall_bottom - depth_offset // 2),
        (width, wall_bottom)
    ]
    
    # 墙壁顶部（可见部分）
    top_wall_points = [
        (0, wall_top),
        (width, wall_top),
        (width + depth_offset, wall_top - depth_offset // 2),
        (depth_offset, wall_top - depth_offset // 2)
    ]
    
    # 绘制墙壁（侧面暗一些）
    side_color = tuple(max(0, c - 40) for c in wall_color)
    top_color = tuple(max(0, c - 20) for c in wall_color)
    
    draw.polygon(side_wall_points, fill=side_color + (255,))
    draw.polygon(top_wall_points, fill=top_color + (255,))
    draw.polygon(front_wall_points, fill=wall_color + (255,))
    
    # ==================== 门 ====================
    door_width = width // 5
    door_height = height // 3
    door_x = width // 2 - door_width // 2
    door_y = height - door_height
    
    door_color = (min(255, wall_color[0] + 60), min(255, wall_color[1] + 40), min(255, wall_color[2] + 20))
    draw.rectangle([door_x, door_y, door_x + door_width, door_y + door_height], fill=door_color + (255,))
    
    # 门框
    draw.rectangle([door_x, door_y, door_x + door_width, door_y + door_height], outline=(50, 30, 20), width=2)
    
    # ==================== 窗户 ====================
    window_size = width // 8
    window_y = wall_top + (wall_bottom - wall_top) // 3
    
    # 左侧窗户
    window_x_left = width // 6
    draw.rectangle([window_x_left, window_y, window_x_left + window_size, window_y + window_size], 
                   fill=(135, 206, 235) + (200,))  # 天蓝色
    draw.rectangle([window_x_left, window_y, window_x_left + window_size, window_y + window_size], 
                   outline=(50, 30, 20), width=2)
    
    # 右侧窗户
    window_x_right = width - width // 6 - window_size
    draw.rectangle([window_x_right, window_y, window_x_right + window_size, window_y + window_size], 
                   fill=(135, 206, 235) + (200,))
    draw.rectangle([window_x_right, window_y, window_x_right + window_size, window_y + window_size], 
                   outline=(50, 30, 20), width=2)
    
    # ==================== 屋顶（斜面） ====================
    # 屋顶前斜面
    roof_front_points = [
        (0, roof_height),
        (width, roof_height),
        (width // 2, 0),
    ]
    
    # 屋顶侧面
    roof_side_points = [
        (width, roof_height),
        (width + depth_offset, roof_height - depth_offset // 2),
        (width // 2 + depth_offset, -depth_offset // 2),
        (width // 2, 0),
    ]
    
    roof_side_dark = tuple(max(0, c - 50) for c in roof_color)
    draw.polygon(roof_side_points, fill=roof_side_dark + (255,))
    draw.polygon(roof_front_points, fill=roof_color + (255,))
    
    # 屋顶轮廓线
    draw.line([(0, roof_height), (width // 2, 0), (width, roof_height)], fill=(80, 50, 40), width=2)
    draw.line([(width, roof_height), (width // 2 + depth_offset, -depth_offset // 2)], fill=(80, 50, 40), width=2)
    
    # ==================== 烟囱（可选） ====================
    if has_chimney:
        chimney_x = width // 4 + depth_offset // 2
        chimney_y = roof_height - depth_offset // 2 - 20
        chimney_w = width // 10
        chimney_h = 25
        
        chimney_color = (139, 69, 19)  # 棕色
        draw.rectangle([chimney_x, chimney_y, chimney_x + chimney_w, chimney_y + chimney_h], 
                       fill=chimney_color + (255,))
        # 烟囱顶
        draw.rectangle([chimney_x - 3, chimney_y, chimney_x + chimney_w + 3, chimney_y + 5], 
                       fill=(min(255, chimney_color[0] + 20), min(255, chimney_color[1] + 20), min(255, chimney_color[2] + 20)) + (255,))
    
    # ==================== 尖塔（可选，教堂用） ====================
    if has_steeple:
        steeple_base_x = width // 2
        steeple_base_y = 0
        steeple_height = height // 4
        
        # 尖塔主体
        steeple_points = [
            (steeple_base_x - 15, steeple_base_y),
            (steeple_base_x + 15, steeple_base_y),
            (steeple_base_x, steeple_base_y - steeple_height),
        ]
        steeple_color = (218, 165, 32)  # 金色
        draw.polygon(steeple_points, fill=steeple_color + (255,))
        draw.line(steeple_points + [steeple_points[0]], fill=(139, 90, 43), width=2)
        
        # 尖塔顶十字架
        cross_y = steeple_base_y - steeple_height
        draw.line([(steeple_base_x, cross_y - 15), (steeple_base_x, cross_y + 5)], fill=(139, 90, 43), width=3)
        draw.line([(steeple_base_x - 8, cross_y - 5), (steeple_base_x + 8, cross_y - 5)], fill=(139, 90, 43), width=3)
    
    # ==================== 招牌（可选，酒馆用） ====================
    if has_sign:
        sign_x = width // 2
        sign_y = wall_top + 20
        sign_w = 50
        sign_h = 30
        
        # 招牌绳子
        draw.line([(sign_x - 20, wall_top), (sign_x - 20, sign_y)], fill=(101, 67, 33), width=2)
        draw.line([(sign_x + 20, wall_top), (sign_x + 20, sign_y)], fill=(101, 67, 33), width=2)
        
        # 招牌主体
        sign_color = (210, 180, 140)  # 木色
        draw.rectangle([sign_x - sign_w//2, sign_y, sign_x + sign_w//2, sign_y + sign_h], 
                       fill=sign_color + (255,))
        draw.rectangle([sign_x - sign_w//2, sign_y, sign_x + sign_w//2, sign_y + sign_h], 
                       outline=(101, 67, 33), width=2)
    
    return img


def generate_all_buildings():
    """生成所有 10 栋建筑"""
    
    buildings = {
        # 可进入建筑（5 栋）
        'blacksmith': {
            'width': 256, 'height': 192, 'roof_height': 50,
            'wall_color': (160, 120, 100),  # 棕色墙壁
            'roof_color': (178, 34, 34),     # 红色屋顶
            'has_chimney': True,
            'desc': '铁匠铺 - 雷叔'
        },
        'church': {
            'width': 320, 'height': 256, 'roof_height': 70,
            'wall_color': (200, 200, 200),  # 白色墙壁
            'roof_color': (139, 90, 43),     # 棕色屋顶
            'has_steeple': True,
            'desc': '教堂 - 老约翰'
        },
        'tavern': {
            'width': 320, 'height': 192, 'roof_height': 50,
            'wall_color': (139, 90, 43),    # 深木色
            'roof_color': (160, 82, 45),     # 红棕色屋顶
            'has_sign': True,
            'desc': '酒馆 - 大熊'
        },
        'merchant': {
            'width': 256, 'height': 192, 'roof_height': 50,
            'wall_color': (188, 143, 89),   # 浅木色
            'roof_color': (107, 142, 35),    # 绿色屋顶
            'desc': '商人行会 - 金铃'
        },
        'school': {
            'width': 192, 'height': 192, 'roof_height': 50,
            'wall_color': (210, 180, 140),  # 米色
            'roof_color': (100, 100, 100),   # 灰色屋顶
            'desc': '学校 - 小安'
        },
        
        # 背景建筑（5 栋）
        'chenmo_hut': {
            'width': 192, 'height': 128, 'roof_height': 40,
            'wall_color': (101, 67, 33),    # 深棕色（破旧）
            'roof_color': (139, 90, 43),     # 棕色屋顶
            'desc': '陈默小屋 - 简陋'
        },
        'baizhi_garden': {
            'width': 256, 'height': 192, 'roof_height': 50,
            'wall_color': (160, 120, 100),  # 棕色
            'roof_color': (85, 107, 47),     # 橄榄绿
            'desc': '白芷药园'
        },
        'guard_post': {
            'width': 256, 'height': 192, 'roof_height': 50,
            'wall_color': (112, 128, 144),  # 灰蓝色（军事）
            'roof_color': (105, 105, 105),   # 深灰
            'desc': '守卫营房 - 阿虎'
        },
        'abandoned_warehouse': {
            'width': 192, 'height': 128, 'roof_height': 40,
            'wall_color': (105, 105, 105),  # 灰色（破旧）
            'roof_color': (80, 80, 80),      # 深灰
            'desc': '废弃仓库 - 神秘'
        },
        'ying_home': {
            'width': 192, 'height': 128, 'roof_height': 40,
            'wall_color': (72, 61, 139),    # 暗紫色
            'roof_color': (47, 79, 79),      # 暗青色
            'desc': '影的住所 - 隐蔽'
        },
    }
    
    output_dir = 'buildings'
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    for building_id, config in buildings.items():
        print(f"生成建筑：{building_id} - {config['desc']}")
        
        building = create_isometric_building(
            width=config['width'],
            height=config['height'],
            roof_height=config['roof_height'],
            wall_color=config['wall_color'],
            roof_color=config['roof_color'],
            has_chimney=config.get('has_chimney', False),
            has_steeple=config.get('has_steeple', False),
            has_sign=config.get('has_sign', False)
        )
        
        filename = f"{output_dir}/building_{building_id}.png"
        building.save(filename, 'PNG')
        print(f"  ✓ 已保存：{filename} ({config['width']}×{config['height']})")
    
    print(f"\n✅ 建筑生成完成！共 {len(buildings)} 栋")


# ==================== 装饰物生成 ====================

def create_tree_pine():
    """创建松树（64×128）"""
    img = Image.new('RGBA', (64, 128), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 树干
    trunk_color = (101, 67, 33)
    draw.rectangle([28, 100, 36, 128], fill=trunk_color + (255,))
    
    # 树冠（三角形层叠）
    tree_color = (34, 139, 34)
    # 下层
    draw.polygon([(32, 40), (8, 110), (56, 110)], fill=tree_color + (255,))
    # 中层
    draw.polygon([(32, 25), (12, 85), (52, 85)], fill=(min(255, tree_color[0]+15), min(255, tree_color[1]+15), min(255, tree_color[2]+15)) + (255,))
    # 上层
    draw.polygon([(32, 10), (16, 60), (48, 60)], fill=(min(255, tree_color[0]+30), min(255, tree_color[1]+30), min(255, tree_color[2]+30)) + (255,))
    
    return img


def create_tree_oak():
    """创建橡树（64×96）"""
    img = Image.new('RGBA', (64, 96), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 树干
    trunk_color = (139, 90, 43)
    draw.rectangle([26, 70, 38, 96], fill=trunk_color + (255,))
    
    # 树冠（圆形）
    tree_color = (60, 179, 113)
    draw.ellipse([8, 15, 56, 75], fill=tree_color + (255,))
    # 树冠细节
    draw.ellipse([12, 20, 50, 70], fill=(min(255, tree_color[0]+20), min(255, tree_color[1]+20), min(255, tree_color[2]+20)) + (255,))
    
    return img


def create_tree_fruit():
    """创建果树（64×96，带粉色花朵）"""
    img = Image.new('RGBA', (64, 96), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 树干
    trunk_color = (101, 67, 33)
    draw.rectangle([28, 70, 36, 96], fill=trunk_color + (255,))
    
    # 树冠
    tree_color = (144, 238, 144)  # 浅绿
    draw.ellipse([10, 20, 54, 75], fill=tree_color + (255,))
    
    # 花朵（粉色点）
    import random
    random.seed(42)
    for _ in range(20):
        fx = random.randint(15, 49)
        fy = random.randint(25, 65)
        draw.ellipse([fx-2, fy-2, fx+2, fy+2], fill=(255, 183, 197) + (255,))  # 粉色
    
    return img


def create_street_light():
    """创建路灯（32×96）"""
    img = Image.new('RGBA', (32, 96), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 灯柱
    pole_color = (47, 79, 79)
    draw.rectangle([14, 30, 18, 96], fill=pole_color + (255,))
    
    # 灯头
    lamp_color = (255, 215, 0)  # 金色
    draw.ellipse([8, 15, 24, 35], fill=lamp_color + (255,))
    # 灯光效果（半透明）
    draw.ellipse([6, 12, 26, 38], fill=(255, 255, 200, 100))
    
    # 灯顶
    draw.rectangle([10, 10, 22, 18], fill=(min(255, pole_color[0]+30), min(255, pole_color[1]+30), min(255, pole_color[2]+30)) + (255,))
    
    return img


def create_flower_bed():
    """创建花坛（64×64）"""
    img = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 花坛边缘（石头）
    stone_color = (128, 128, 128)
    draw.ellipse([4, 4, 60, 60], fill=stone_color + (255,))
    draw.ellipse([8, 8, 56, 56], fill=(100, 80, 60) + (255,))  # 泥土
    
    # 花朵（多色）
    import random
    random.seed(42)
    flower_colors = [(255, 0, 0), (255, 165, 0), (255, 255, 0), (255, 0, 255), (255, 192, 203)]
    for _ in range(15):
        fx = random.randint(12, 52)
        fy = random.randint(12, 52)
        color = flower_colors[random.randint(0, len(flower_colors)-1)]
        draw.ellipse([fx-3, fy-3, fx+3, fy+3], fill=color + (255,))
    
    return img


def create_bench():
    """创建长椅（96×32）"""
    img = Image.new('RGBA', (96, 32), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 椅腿
    leg_color = (101, 67, 33)
    draw.rectangle([10, 20, 18, 32], fill=leg_color + (255,))
    draw.rectangle([78, 20, 86, 32], fill=leg_color + (255,))
    
    # 椅面
    seat_color = (139, 90, 43)
    draw.rectangle([5, 15, 91, 25], fill=seat_color + (255,))
    
    # 椅背
    draw.rectangle([5, 5, 91, 18], fill=seat_color + (255,))
    draw.line([(15, 8), (15, 15)], fill=(101, 67, 33), width=2)
    draw.line([(48, 8), (48, 15)], fill=(101, 67, 33), width=2)
    draw.line([(81, 8), (81, 15)], fill=(101, 67, 33), width=2)
    
    return img


def create_well():
    """创建水井（64×96）"""
    img = Image.new('RGBA', (64, 96), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 井身（圆柱）
    well_color = (128, 128, 128)
    draw.rectangle([12, 40, 52, 96], fill=well_color + (255,))
    # 井口椭圆
    draw.ellipse([12, 35, 52, 50], fill=(100, 100, 100) + (255,))
    draw.ellipse([16, 38, 48, 48], fill=(50, 50, 50) + (255,))  # 井水
    
    # 井顶支架
    wood_color = (139, 90, 43)
    draw.rectangle([8, 20, 16, 45], fill=wood_color + (255,))
    draw.rectangle([48, 20, 56, 45], fill=wood_color + (255,))
    draw.rectangle([8, 15, 56, 25], fill=wood_color + (255,))
    
    # 水桶和绳子
    draw.line([(32, 18), (32, 40)], fill=(101, 67, 33), width=2)  # 绳子
    draw.ellipse([26, 38, 38, 48], fill=(160, 82, 45) + (255,))  # 水桶
    
    return img


def create_barrel():
    """创建木桶（32×32）"""
    img = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 桶身
    barrel_color = (139, 90, 43)
    draw.ellipse([4, 4, 28, 28], fill=barrel_color + (255,))
    draw.ellipse([6, 6, 26, 26], fill=(min(255, barrel_color[0]+20), min(255, barrel_color[1]+20), min(255, barrel_color[2]+20)) + (255,))
    
    # 铁箍
    draw.arc([6, 10, 26, 14], 0, 360, fill=(100, 100, 100), width=2)
    draw.arc([6, 20, 26, 24], 0, 360, fill=(100, 100, 100), width=2)
    
    return img


def generate_all_decorations():
    """生成所有装饰物"""
    
    decorations = {
        'tree_pine': (create_tree_pine, (64, 128), '松树'),
        'tree_oak': (create_tree_oak, (64, 96), '橡树'),
        'tree_fruit': (create_tree_fruit, (64, 96), '果树'),
        'street_light': (create_street_light, (32, 96), '路灯'),
        'flower_bed': (create_flower_bed, (64, 64), '花坛'),
        'bench': (create_bench, (96, 32), '长椅'),
        'well': (create_well, (64, 96), '水井'),
        'barrel': (create_barrel, (32, 32), '木桶'),
    }
    
    output_dir = 'decorations'
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    for dec_id, (create_func, size, desc) in decorations.items():
        print(f"生成装饰物：{dec_id} - {desc} ({size[0]}×{size[1]})")
        
        decoration = create_func()
        filename = f"{output_dir}/{dec_id}.png"
        decoration.save(filename, 'PNG')
        print(f"  ✓ 已保存：{filename}")
    
    print(f"\n✅ 装饰物生成完成！共 {len(decorations)} 种")


# ==================== 主函数 ====================

def main():
    print("=" * 60)
    print("暮色村 - 建筑和装饰物 Sprite 生成器")
    print("伪 3D 斜角视角（45°俯视）")
    print("=" * 60)
    print()
    
    # 生成建筑
    print("【建筑生成】")
    generate_all_buildings()
    print()
    
    # 生成装饰物
    print("【装饰物生成】")
    generate_all_decorations()
    
    print()
    print("=" * 60)
    print("🎉 全部完成！")
    print("=" * 60)


if __name__ == '__main__':
    main()
