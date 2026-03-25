## Player - 玩家角色
## 处理玩家移动、交互检测
extends CharacterBody2D

# ==================== 信号 ====================
signal interacted_with(target: Node2D)

# ==================== 导出变量 ====================
@export var speed: float = 200.0  ## 移动速度
@export var interaction_range: float = 60.0  ## 交互范围

# ==================== 状态 ====================
var current_target: Node2D = null
var is_in_dialogue: bool = false

# ==================== 节点引用 ====================
@onready var sprite: Sprite2D = $Sprite2D
@onready var interaction_area: Area2D = $InteractionArea
@onready var interaction_label: Label = $InteractionLabel


func _ready() -> void:
	# 连接交互区域信号
	if interaction_area:
		interaction_area.body_entered.connect(_on_interaction_area_body_entered)
		interaction_area.body_exited.connect(_on_interaction_area_body_exited)

	# 连接对话管理器信号
	DialogueManager.dialogue_line_spoken.connect(_on_dialogue_line)
	DialogueManager.choice_presented.connect(_on_choices_presented)
	DialogueManager.dialogue_ended.connect(_on_dialogue_ended)

	# 初始化交互提示
	if interaction_label:
		interaction_label.visible = false

	print("[Player] 玩家初始化完成")


func _physics_process(delta: float) -> void:
	# 对话中不能移动
	if is_in_dialogue:
		return

	# 处理移动
	_handle_movement()

	# 处理交互
	_handle_interaction()


# ==================== 移动系统 ====================

func _handle_movement() -> void:
	"""处理玩家移动输入"""
	var direction = Vector2.ZERO

	# 获取输入方向
	if Input.is_action_pressed("ui_left"):
		direction.x -= 1
	if Input.is_action_pressed("ui_right"):
		direction.x += 1
	if Input.is_action_pressed("ui_up"):
		direction.y -= 1
	if Input.is_action_pressed("ui_down"):
		direction.y += 1

	# 标准化方向向量
	if direction.length() > 0:
		direction = direction.normalized()
		velocity = direction * speed

		# 翻转精灵朝向
		if sprite:
			sprite.flip_h = direction.x < 0
	else:
		velocity = Vector2.ZERO

	move_and_slide()


# ==================== 交互系统 ====================

func _handle_interaction() -> void:
	"""处理交互输入"""
	if Input.is_action_just_pressed("interact"):
		if current_target and current_target.has_method("start_dialogue"):
			# 开始对话
			is_in_dialogue = true
			current_target.start_dialogue()

			# 隐藏交互提示
			if interaction_label:
				interaction_label.visible = false


func _on_interaction_area_body_entered(body: Node2D) -> void:
	"""进入交互范围"""
	if body.is_in_group("villagers"):
		current_target = body
		if interaction_label:
			interaction_label.text = "按 E 与 %s 对话" % body.villager_name
			interaction_label.visible = true
		print("[Player] 靠近村民: %s" % body.villager_name)


func _on_interaction_area_body_exited(body: Node2D) -> void:
	"""离开交互范围"""
	if body == current_target:
		current_target = null
		if interaction_label:
			interaction_label.visible = false
		print("[Player] 离开村民")


# ==================== 对话系统回调 ====================

func _on_dialogue_line(speaker: String, text: String) -> void:
	"""接收到对话行"""
	# 信号会被 Village 场景接收并更新 UI
	pass


func _on_choices_presented(choices: Array) -> void:
	"""显示对话选项"""
	# 信号会被 Village 场景接收并更新 UI
	pass


func _on_dialogue_ended(_villager_id: String) -> void:
	"""对话结束"""
	is_in_dialogue = false


# ==================== 公共方法 ====================

func set_position_safe(new_pos: Vector2) -> void:
	"""安全设置位置"""
	global_position = new_pos