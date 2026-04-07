# 玩家移动系统文档

## 概述

本文档描述魔王城下的最后村庄的玩家移动系统实现。

## 控制方式

### 移动控制
| 按键 | 功能 |
|------|------|
| W / ↑ | 向上移动 |
| S / ↓ | 向下移动 |
| A / ← | 向左移动 |
| D / → | 向右移动 |
| Shift | 按住跑步 |

### 交互控制
| 按键 | 功能 |
|------|------|
| E | 与 NPC 对话 / 交互 |
| ESC | 打开菜单 |

## 移动特性

### 8 方向移动
支持 8 个方向的平滑移动：
- 上 (Up)
- 右上 (Up-Right)
- 右 (Right)
- 右下 (Down-Right)
- 下 (Down)
- 左下 (Down-Left)
- 左 (Left)
- 左上 (Up-Left)

### 平滑移动
- 使用加速度/摩擦力实现平滑移动
- 停止按键后会逐渐减速

### 速度配置
| 状态 | 速度 |
|------|------|
| 行走 | 150 像素/秒 |
| 跑步 | 250 像素/秒 |
| 加速度 | 10 |
| 摩擦力 | 8 |

## 动画系统

### 状态机
```
IDLE ←→ WALKING
```

### 动画列表
- `walk_down` - 向下行走
- `walk_up` - 向上行走
- `walk_left` - 向左行走
- `walk_right` - 向右行走
- `idle_down` - 向下站立
- `idle_up` - 向上站立
- `idle_left` - 向左站立
- `idle_right` - 向右站立

### 动画帧
每个方向 4 帧，帧率 8 FPS。

## 碰撞系统

### 碰撞层
- Layer 1: 玩家
- Mask 2: 检测障碍物（建筑、边界等）

### 碰撞形状
- 圆形碰撞体，半径 16 像素
- 交互检测范围 60 像素

## 代码结构

### Player.gd
```gdscript
# 主要组件
@onready var animated_sprite: AnimatedSprite2D
@onready var interaction_area: Area2D
@onready var interaction_label: Label

# 状态
enum MovementState { IDLE, WALKING }
enum Direction { DOWN, DOWN_LEFT, LEFT, UP_LEFT, UP, UP_RIGHT, RIGHT, DOWN_RIGHT }

# 核心方法
func _handle_movement(delta: float)  # 处理移动输入
func _update_animation()              # 更新动画
func _get_input_direction() -> Vector2  # 获取 8 方向输入
```

## 扩展说明

### 添加新动画
1. 在 SpriteFrames 资源中添加新动画
2. 更新 `_get_animation_name()` 方法

### 修改移动参数
在检查器中调整导出变量：
- `walk_speed` - 行走速度
- `run_speed` - 跑步速度
- `acceleration` - 加速度
- `friction` - 摩擦力

### 添加新输入
1. 在 `_setup_input_actions()` 中添加新的按键映射
2. 在 `_get_input_direction()` 中处理新输入

## 相关文件

- `scripts/characters/Player.gd` - 玩家脚本
- `scenes/characters/Player.tscn` - 玩家场景
- `resources/characters/player_spriteframes.tres` - 动画资源
- `assets/sprites/characters/player_walk.png` - 精灵图

---

**文档版本**: 1.0
**创建日期**: 2026-04-07
**相关 Issue**: #69 CS-007: 玩家移动系统重构