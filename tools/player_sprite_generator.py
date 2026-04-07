#!/usr/bin/env python3
"""
玩家角色行走动画 Sprite 生成器
生成 32x32 像素的像素风格玩家行走动画
"""

from PIL import Image, ImageDraw
import os

# 配置
SPRITE_SIZE = 32
FRAMES_PER_DIRECTION = 4
OUTPUT_DIR = "code/assets/sprites/characters"
PALETTE = {
    'skin': (255, 220, 180),          # 皮肤色
    'skin_shadow': (220, 180, 150),   # 皮肤阴影
    'hair': (60, 40, 20),             # 头发棕色
    'hair_light': (100, 70, 40),      # 头发高光
    'shirt': (65, 105, 225),          # 衣服蓝色
    'shirt_shadow': (45, 85, 205),    # 衣服阴影
    'pants': (60, 60, 60),            # 裤子灰色
    'pants_shadow': (40, 40, 40),     # 裤子阴影
    'shoes': (40, 30, 20),            # 鞋子棕色
    'outline': (20, 20, 20),          # 轮廓线
}

def create_player_frame(direction, frame):
    """
    创建玩家行走动画帧
    direction: 0=下，1=左，2=右，3=上
    frame: 0-3（行走周期）
    """
    img = Image.new('RGBA', (SPRITE_SIZE, SPRITE_SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 行走偏移（动画）
    body_offset = 0
    leg_offset = 0
    arm_offset = 0
    
    if frame == 0:  # 站立
        body_offset = 0
        leg_offset = 0
        arm_offset = 0
    elif frame == 1:  # 左脚前
        body_offset = -1
        leg_offset = 2
        arm_offset = 2
    elif frame == 2:  # 右脚前
        body_offset = 0
        leg_offset = 0
        arm_offset = 0
    elif frame == 3:  # 左脚后
        body_offset = 1
        leg_offset = -2
        arm_offset = -2
    
    # 根据方向调整
    if direction == 3:  # 向上 - 看不到脸
        # 身体
        draw.rectangle([10, 12+body_offset, 22, 24], fill=PALETTE['shirt'])
        # 头
        draw.rectangle([11, 4, 21, 12], fill=PALETTE['hair'])
        # 腿
        if frame == 1:
            draw.rectangle([11, 24, 15, 30], fill=PALETTE['pants'])
            draw.rectangle([17, 24, 21, 28], fill=PALETTE['pants'])
        elif frame == 3:
            draw.rectangle([11, 24, 15, 28], fill=PALETTE['pants'])
            draw.rectangle([17, 24, 21, 30], fill=PALETTE['pants'])
        else:
            draw.rectangle([11, 24, 15, 30], fill=PALETTE['pants'])
            draw.rectangle([17, 24, 21, 30], fill=PALETTE['pants'])
        # 鞋子
        draw.rectangle([11, 30, 15, 32], fill=PALETTE['shoes'])
        draw.rectangle([17, 30, 21, 32], fill=PALETTE['shoes'])
        
    elif direction == 0:  # 向下 - 看到脸
        # 腿
        if frame == 1:
            draw.rectangle([11, 24+leg_offset, 15, 30], fill=PALETTE['pants'])
            draw.rectangle([17, 24-leg_offset, 21, 28], fill=PALETTE['pants'])
        elif frame == 3:
            draw.rectangle([11, 24-leg_offset, 15, 28], fill=PALETTE['pants'])
            draw.rectangle([17, 24+leg_offset, 21, 30], fill=PALETTE['pants'])
        else:
            draw.rectangle([11, 24, 15, 30], fill=PALETTE['pants'])
            draw.rectangle([17, 24, 21, 30], fill=PALETTE['pants'])
        # 鞋子
        draw.rectangle([11, 30, 15, 32], fill=PALETTE['shoes'])
        draw.rectangle([17, 30, 21, 32], fill=PALETTE['shoes'])
        # 身体
        draw.rectangle([10, 14+body_offset, 22, 24], fill=PALETTE['shirt'])
        # 手臂
        if frame == 1:
            draw.rectangle([6, 14+arm_offset, 10, 22], fill=PALETTE['skin'])
            draw.rectangle([22, 14-arm_offset, 26, 22], fill=PALETTE['skin'])
        elif frame == 3:
            draw.rectangle([6, 14-arm_offset, 10, 22], fill=PALETTE['skin'])
            draw.rectangle([22, 14+arm_offset, 26, 22], fill=PALETTE['skin'])
        else:
            draw.rectangle([6, 14, 10, 22], fill=PALETTE['skin'])
            draw.rectangle([22, 14, 26, 22], fill=PALETTE['skin'])
        # 头
        draw.rectangle([11, 6, 21, 14], fill=PALETTE['skin'])
        # 头发
        draw.rectangle([11, 6, 21, 10], fill=PALETTE['hair'])
        # 眼睛
        draw.point((14, 11), fill=PALETTE['outline'])
        draw.point((18, 11), fill=PALETTE['outline'])
        # 嘴巴
        if frame == 2:
            draw.point((16, 13), fill=PALETTE['outline'])
        
    elif direction == 1:  # 向左
        # 腿
        if frame == 1:
            draw.rectangle([10, 24+leg_offset, 16, 30], fill=PALETTE['pants'])
            draw.rectangle([16, 24-leg_offset, 20, 28], fill=PALETTE['pants'])
        elif frame == 3:
            draw.rectangle([10, 24-leg_offset, 16, 28], fill=PALETTE['pants'])
            draw.rectangle([16, 24+leg_offset, 20, 30], fill=PALETTE['pants'])
        else:
            draw.rectangle([10, 24, 16, 30], fill=PALETTE['pants'])
            draw.rectangle([16, 24, 20, 30], fill=PALETTE['pants'])
        # 鞋子
        draw.rectangle([10, 30, 16, 32], fill=PALETTE['shoes'])
        draw.rectangle([16, 30, 20, 32], fill=PALETTE['shoes'])
        # 身体
        draw.rectangle([10, 14+body_offset, 20, 24], fill=PALETTE['shirt'])
        # 头
        draw.rectangle([10, 6, 20, 14], fill=PALETTE['skin'])
        # 头发
        draw.rectangle([10, 6, 18, 10], fill=PALETTE['hair'])
        # 眼睛（侧面）
        draw.point((16, 11), fill=PALETTE['outline'])
        # 手臂（前）
        draw.rectangle([14, 16, 22, 20], fill=PALETTE['skin'])
        
    elif direction == 2:  # 向右
        # 腿
        if frame == 1:
            draw.rectangle([14, 24+leg_offset, 20, 30], fill=PALETTE['pants'])
            draw.rectangle([10, 24-leg_offset, 16, 28], fill=PALETTE['pants'])
        elif frame == 3:
            draw.rectangle([14, 24-leg_offset, 20, 28], fill=PALETTE['pants'])
            draw.rectangle([10, 24+leg_offset, 16, 30], fill=PALETTE['pants'])
        else:
            draw.rectangle([14, 24, 20, 30], fill=PALETTE['pants'])
            draw.rectangle([10, 24, 16, 30], fill=PALETTE['pants'])
        # 鞋子
        draw.rectangle([14, 30, 20, 32], fill=PALETTE['shoes'])
        draw.rectangle([10, 30, 16, 32], fill=PALETTE['shoes'])
        # 身体
        draw.rectangle([12, 14+body_offset, 22, 24], fill=PALETTE['shirt'])
        # 头
        draw.rectangle([12, 6, 22, 14], fill=PALETTE['skin'])
        # 头发
        draw.rectangle([14, 6, 22, 10], fill=PALETTE['hair'])
        # 眼睛（侧面）
        draw.point((18, 11), fill=PALETTE['outline'])
        # 手臂（前）
        draw.rectangle([10, 16, 18, 20], fill=PALETTE['skin'])
    
    return img

def create_spritesheet():
    """创建完整的行走动画 Sprite Sheet"""
    print("🚶 开始生成玩家行走动画...")
    
    # 创建输出目录
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # 生成所有帧
    # 布局：4 行（方向）x 4 列（帧）
    directions = ['down', 'left', 'right', 'up']
    cols = FRAMES_PER_DIRECTION
    rows = len(directions)
    
    sheet_width = cols * SPRITE_SIZE
    sheet_height = rows * SPRITE_SIZE
    
    spritesheet = Image.new('RGBA', (sheet_width, sheet_height), (0, 0, 0, 0))
    
    for dir_idx, dir_name in enumerate(directions):
        for frame in range(FRAMES_PER_DIRECTION):
            frame_img = create_player_frame(dir_idx, frame)
            col = frame
            row = dir_idx
            spritesheet.paste(frame_img, (col * SPRITE_SIZE, row * SPRITE_SIZE))
            print(f"  ✓ {dir_name}_frame{frame}")
    
    # 保存 Sprite Sheet
    sheet_path = os.path.join(OUTPUT_DIR, 'player_walk.png')
    spritesheet.save(sheet_path)
    print(f"\n✅ 玩家行走动画已保存到：{sheet_path}")
    print(f"   尺寸：{sheet_width}x{sheet_height} 像素")
    print(f"   帧数：{len(directions)} 方向 x {FRAMES_PER_DIRECTION} 帧 = {len(directions)*FRAMES_PER_DIRECTION} 帧")
    
    # 同时保存单个帧文件（方便调试）
    frames_dir = os.path.join(OUTPUT_DIR, 'player')
    os.makedirs(frames_dir, exist_ok=True)
    
    for dir_idx, dir_name in enumerate(directions):
        for frame in range(FRAMES_PER_DIRECTION):
            frame_img = create_player_frame(dir_idx, frame)
            frame_path = os.path.join(frames_dir, f'{dir_name}_frame{frame}.png')
            frame_img.save(frame_path)
    
    print(f"   单帧文件：{frames_dir}/")
    
    return sheet_path

if __name__ == '__main__':
    create_spritesheet()
