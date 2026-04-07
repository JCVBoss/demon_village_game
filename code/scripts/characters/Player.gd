## Player - 玩家角色
## 处理玩家移动、动画状态机、交互检测
## 支持 8 方向移动和 WASD/方向键输入
extends CharacterBody2D

# ==================== 信号 ====================
signal direction_changed(new_direction: Vector2)
signal movement_state_changed(new_state: MovementState)

# ==================== 枚举 ====================
enum MovementState { IDLE, WALKING }
enum Direction { DOWN, DOWN_LEFT, LEFT, UP_LEFT, UP, UP_RIGHT, RIGHT, DOWN_RIGHT }

# ==================== 导出变量 ====================
@export_group("Movement")
@export var walk_speed: float = 150.0  ## 行走速度
@export var run_speed: float = 250.0   ## 跑步速度（Shift 键）
@export var acceleration: float = 10.0  ## 加速度
@export var friction: float = 8.0       ## 摩擦力

@export_group("Interaction")
@export var interaction_range: float = 60.0  ## 交互范围

# ==================== 状态 ====================
var current_state: MovementState = MovementState.IDLE
var current_direction: Direction = Direction.DOWN
var current_target: Node2D = null
var is_in_dialogue: bool = false
var is_running: bool = false

# 动画状态
var last_movement_direction: Vector2 = Vector2.DOWN

# ==================== 节点引用 ====================
@onready var animated_sprite: AnimatedSprite2D = $AnimatedSprite2D
@onready var interaction_area: Area2D = $InteractionArea
@onready var interaction_label: Label = $InteractionLabel
@onready var collision_shape: CollisionShape2D = $CollisionShape2D

# ==================== 输入映射 ====================
# WASD 和方向键都映射到相同的动作


func _ready() -> void:
	_setup_input_actions()
	_connect_signals()
	_initialize_player()
	print("[Player] 玩家初始化完成，支持 8 方向移动")


func _setup_input_actions() -> void:
	"""设置输入动作映射（如果未定义）"""
	# 检查并添加 WASD 映射
	var actions = ["move_up", "move_down", "move_left", "move_right"]
	for action in actions:
		if not InputMap.has_action(action):
			InputMap.add_action(action)

	# 添加按键映射
	_add_key_to_action("move_up", KEY_W)
	_add_key_to_action("move_up", KEY_UP)
	_add_key_to_action("move_down", KEY_S)
	_add_key_to_action("move_down", KEY_DOWN)
	_add_key_to_action("move_left", KEY_A)
	_add_key_to_action("move_left", KEY_LEFT)
	_add_key_to_action("move_right", KEY_D)
	_add_key_to_action("move_right", KEY_RIGHT)


func _add_key_to_action(action: String, keycode: int) -> void:
	"""添加按键到动作映射"""
	var event = InputEventKey.new()
	event.keycode = keycode
	InputMap.action_add_event(action, event)


func _connect_signals() -> void:
	"""连接信号"""
	if interaction_area:
		interaction_area.area_entered.connect(_on_interaction_area_entered)
		interaction_area.area_exited.connect(_on_interaction_area_exited)

	DialogueManager.dialogue_ended.connect(_on_dialogue_ended)


func _initialize_player() -> void:
	"""初始化玩家状态"""
	if interaction_label:
		interaction_label.visible = false

	# 初始化动画
	_update_animation()


func _physics_process(delta: float) -> void:
	"""物理帧处理"""
	if is_in_dialogue:
		_apply_friction(delta)
		move_and_slide()
		return

	# 检查是否在跑步
	is_running = Input.is_action_pressed("run")

	# 处理移动
	_handle_movement(delta)

	# 处理交互
	_handle_interaction()

	# 应用移动
	move_and_slide()

	# 更新动画
	_update_animation_state()


# ==================== 移动系统 ====================

func _handle_movement(delta: float) -> void:
	"""处理玩家移动输入"""
	var input_direction = _get_input_direction()

	if input_direction != Vector2.ZERO:
		# 移动中
		var target_speed = walk_speed if not is_running else run_speed
		var target_velocity = input_direction * target_speed

		# 平滑加速
		velocity = velocity.lerp(target_velocity, acceleration * delta)

		# 更新方向
		last_movement_direction = input_direction
		current_direction = _get_direction_from_vector(input_direction)

		# 更新状态
		if current_state != MovementState.WALKING:
			_set_movement_state(MovementState.WALKING)
	else:
		# 应用摩擦力减速
		_apply_friction(delta)


func _get_input_direction() -> Vector2:
	"""获取输入方向（8 方向）"""
	var direction = Vector2.ZERO

	if Input.is_action_pressed("move_left"):
		direction.x -= 1
	if Input.is_action_pressed("move_right"):
		direction.x += 1
	if Input.is_action_pressed("move_up"):
		direction.y -= 1
	if Input.is_action_pressed("move_down"):
		direction.y += 1

	# 标准化并限制为 8 方向
	if direction.length() > 0:
		direction = direction.normalized()
		# 将角度转换为 8 方向
		var angle = direction.angle()
		var snap_angle = snappedf(angle, PI / 4)
		direction = Vector2.RIGHT.rotated(snap_angle)

	return direction


func _apply_friction(delta: float) -> void:
	"""应用摩擦力"""
	if velocity.length() > 5:
		velocity = velocity.lerp(Vector2.ZERO, friction * delta)
	else:
		velocity = Vector2.ZERO
		if current_state != MovementState.IDLE:
			_set_movement_state(MovementState.IDLE)


func _get_direction_from_vector(dir: Vector2) -> Direction:
	"""从向量获取 8 方向枚举"""
	var angle = dir.angle()

	# 标准化角度到 [0, 2*PI)
	while angle < 0:
		angle += TAU

	# 根据角度返回方向
	if angle < PI / 8:
		return Direction.RIGHT
	elif angle < 3 * PI / 8:
		return Direction.DOWN_RIGHT
	elif angle < 5 * PI / 8:
		return Direction.DOWN
	elif angle < 7 * PI / 8:
		return Direction.DOWN_LEFT
	elif angle < 9 * PI / 8:
		return Direction.LEFT
	elif angle < 11 * PI / 8:
		return Direction.UP_LEFT
	elif angle < 13 * PI / 8:
		return Direction.UP
	elif angle < 15 * PI / 8:
		return Direction.UP_RIGHT
	else:
		return Direction.RIGHT


# ==================== 动画系统 ====================

func _update_animation_state() -> void:
	"""更新动画状态"""
	if velocity.length() > 5:
		if current_state != MovementState.WALKING:
			_set_movement_state(MovementState.WALKING)
	else:
		if current_state != MovementState.IDLE:
			_set_movement_state(MovementState.IDLE)


func _set_movement_state(new_state: MovementState) -> void:
	"""设置移动状态"""
	if current_state == new_state:
		return
	current_state = new_state
	movement_state_changed.emit(new_state)
	_update_animation()


func _update_animation() -> void:
	"""更新动画播放"""
	if not animated_sprite:
		return

	var anim_name = _get_animation_name()

	if animated_sprite.animation != anim_name:
		animated_sprite.play(anim_name)

	# 设置动画速度
	animated_sprite.speed_scale = 1.5 if is_running else 1.0


func _get_animation_name() -> String:
	"""获取当前动画名称"""
	var prefix = "walk" if current_state == MovementState.WALKING else "idle"
	var suffix = _get_direction_suffix()

	var full_name = "%s_%s" % [prefix, suffix]

	# 检查动画是否存在，如果不存在则使用基本动画
	if animated_sprite.sprite_frames and animated_sprite.sprite_frames.has_animation(full_name):
		return full_name
	else:
		# 回退到 4 方向动画
		match current_direction:
			Direction.UP, Direction.UP_LEFT, Direction.UP_RIGHT:
				return "%s_up" % prefix
			Direction.DOWN, Direction.DOWN_LEFT, Direction.DOWN_RIGHT:
				return "%s_down" % prefix
			Direction.LEFT:
				return "%s_left" % prefix
			Direction.RIGHT:
				return "%s_right" % prefix
			_:
				return "%s_down" % prefix


func _get_direction_suffix() -> String:
	"""获取方向后缀"""
	match current_direction:
		Direction.DOWN: return "down"
		Direction.DOWN_LEFT: return "down_left"
		Direction.LEFT: return "left"
		Direction.UP_LEFT: return "up_left"
		Direction.UP: return "up"
		Direction.UP_RIGHT: return "up_right"
		Direction.RIGHT: return "right"
		Direction.DOWN_RIGHT: return "down_right"
		_: return "down"


# ==================== 交互系统 ====================

func _handle_interaction() -> void:
	"""处理交互输入"""
	if Input.is_action_just_pressed("interact"):
		if current_target and current_target.has_method("start_dialogue"):
			is_in_dialogue = true
			current_target.start_dialogue()

			if interaction_label:
				interaction_label.visible = false


func _on_interaction_area_entered(area: Area2D) -> void:
	"""进入交互范围"""
	if area.is_in_group("villagers"):
		current_target = area
		if interaction_label:
			var villager_name = area.villager_name if "villager_name" in area else "村民"
			interaction_label.text = "按 E 与 %s 对话" % villager_name
			interaction_label.visible = true


func _on_interaction_area_exited(area: Area2D) -> void:
	"""离开交互范围"""
	if area == current_target:
		current_target = null
		if interaction_label:
			interaction_label.visible = false


# ==================== 对话系统回调 ====================

func _on_dialogue_ended(_villager_id: String) -> void:
	"""对话结束"""
	is_in_dialogue = false


# ==================== 公共方法 ====================

func set_position_safe(new_pos: Vector2) -> void:
	"""安全设置位置"""
	global_position = new_pos


func get_movement_state_name() -> String:
	"""获取当前状态名称"""
	return MovementState.keys()[current_state]


func get_direction_name() -> String:
	"""获取当前方向名称"""
	return Direction.keys()[current_direction]