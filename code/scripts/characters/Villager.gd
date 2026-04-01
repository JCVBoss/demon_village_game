## Villager - 村民角色基类
## 处理村民的交互、对话触发、状态管理
extends Area2D

# ==================== 信号 ====================
signal dialogue_started(villager_id: String)
signal dialogue_ended()

# ==================== 导出变量 ====================
@export var villager_id: String = "chenmo"  ## 村民 ID
@export var villager_name: String = "陈默"   ## 显示名称
@export var interaction_range: float = 50.0  ## 交互范围

# ==================== 状态 ====================
var is_player_nearby: bool = false
var is_in_dialogue: bool = false
var current_trust: int = 0
var current_expression: String = "normal"  ## 当前表情

# ==================== 节点引用 ====================
@onready var sprite: Sprite2D = $Sprite2D
@onready var interaction_label: Label = $InteractionLabel
@onready var name_label: Label = $NameLabel
@onready var collision: CollisionShape2D = $CollisionShape2D

# ==================== 配置 ====================
var _villager_data: Dictionary = {}

# 村民 ID 到精灵文件名的映射
const SPRITE_MAPPING: Dictionary = {
	"chenmo": "chenmo",
	"leishu": "leishu",
	"jinling": "jinling",
	"baizhi": "baizhi",
	"john": "laojohn",  # 老约翰的文件名是 laojohn
	"daxiong": "daxiong",
	"ying": "ying",
	"xiaoan": "xiaoan",
	"ahu": "xiaohu",  # 阿虎的文件名是 xiaohu
	"yeya": "yeya"
}


func _ready() -> void:
	# 添加到 villagers 分组（关键！用于 Player 检测）
	add_to_group("villagers")

	# 连接信号
	body_entered.connect(_on_body_entered)
	body_exited.connect(_on_body_exited)

	# 加载村民数据
	_load_villager_data()

	# 加载精灵图
	_load_sprite()

	# 初始化 UI
	_setup_ui()

	print("[Villager] %s 初始化完成，已加入 villagers 分组" % villager_name)


func _process(_delta: float) -> void:
	# 检测交互输入
	if is_player_nearby and Input.is_action_just_pressed("interact"):
		if not is_in_dialogue:
			start_dialogue()


# ==================== 初始化 ====================

func _load_villager_data() -> void:
	"""从 JSON 文件加载村民数据"""
	var file = FileAccess.open("res://resources/data/villagers.json", FileAccess.READ)
	if file:
		var json_string = file.get_as_text()
		file.close()

		var json = JSON.new()
		if json.parse(json_string) == OK:
			var data = json.data
			# JSON 结构是 {"villagers": {"chenmo": {...}, ...}}
			var villagers = data.get("villagers", data)
			if villagers.has(villager_id):
				_villager_data = villagers[villager_id]
				villager_name = _villager_data.get("name", villager_name)
				print("[Villager] 加载 %s 数据成功" % villager_name)
			else:
				print("[Villager] 未找到村民 %s 的数据" % villager_id)


func _load_sprite() -> void:
	"""加载村民精灵图"""
	if not sprite:
		return

	# 获取精灵文件名
	var sprite_name = SPRITE_MAPPING.get(villager_id, villager_id)
	var sprite_path = "res://assets/sprites/characters/%s_%s.png" % [sprite_name, current_expression]

	# 尝试加载精灵
	if ResourceLoader.exists(sprite_path):
		var texture = load(sprite_path)
		sprite.texture = texture
		print("[Villager] 加载精灵: %s" % sprite_path)
	else:
		# 尝试加载 normal 表情作为默认
		sprite_path = "res://assets/sprites/characters/%s_normal.png" % sprite_name
		if ResourceLoader.exists(sprite_path):
			var texture = load(sprite_path)
			sprite.texture = texture
			print("[Villager] 加载默认精灵: %s" % sprite_path)
		else:
			print("[Villager] 未找到精灵: %s" % sprite_name)


func _setup_ui() -> void:
	"""设置 UI 元素"""
	if interaction_label:
		interaction_label.text = "按 E 交互"
		interaction_label.visible = false

	if name_label:
		name_label.text = villager_name
		name_label.visible = true

	# 从 TrustManager 获取当前信任值
	current_trust = TrustManager.get_trust(villager_id)


# ==================== 表情系统 ====================

func set_expression(expression: String) -> void:
	"""设置村民表情"""
	current_expression = expression
	_load_sprite()


# ==================== 交互系统 ====================

func _on_body_entered(body: Node2D) -> void:
	"""玩家进入交互范围"""
	if body.is_in_group("player"):
		is_player_nearby = true
		if interaction_label:
			interaction_label.visible = true
		print("[Villager] 玩家靠近 %s" % villager_name)


func _on_body_exited(body: Node2D) -> void:
	"""玩家离开交互范围"""
	if body.is_in_group("player"):
		is_player_nearby = false
		if interaction_label:
			interaction_label.visible = false
		print("[Villager] 玩家离开 %s" % villager_name)


func start_dialogue() -> void:
	"""开始对话"""
	is_in_dialogue = true

	# 设置对话表情
	set_expression("happy")

	# 从 TrustManager 获取当前信任值
	current_trust = TrustManager.get_trust(villager_id)

	# 通知游戏管理器进入对话状态
	GameManager.enter_dialogue()

	# 隐藏交互提示
	if interaction_label:
		interaction_label.visible = false

	# 触发对话开始信号
	dialogue_started.emit(villager_id)

	# 调用对话管理器开始对话，传递信任值
	DialogueManager.start_dialogue(villager_id, current_trust)

	print("[Villager] 开始与 %s 对话 (信任值: %d)" % [villager_name, current_trust])


func end_dialogue() -> void:
	"""结束对话"""
	is_in_dialogue = false

	# 恢复普通表情
	set_expression("normal")

	# 通知游戏管理器退出对话状态
	GameManager.exit_dialogue()

	# 显示交互提示
	if interaction_label and is_player_nearby:
		interaction_label.visible = true

	# 触发对话结束信号
	dialogue_ended.emit()

	print("[Villager] 与 %s 对话结束" % villager_name)


# ==================== 信任系统 ====================

func update_trust(amount: int) -> void:
	"""更新信任值"""
	current_trust = clamp(current_trust + amount, 0, 100)
	GameManager.modify_trust(villager_id, amount)

	# 更新村民数据中的信任值
	if _villager_data.has("trust_level"):
		_villager_data["trust_level"] = current_trust

	print("[Villager] %s 信任值更新: %d" % [villager_name, current_trust])


func get_trust_level() -> String:
	"""获取信任等级名称"""
	if current_trust >= 81:
		return "忠诚"
	elif current_trust >= 61:
		return "信任"
	elif current_trust >= 41:
		return "友好"
	elif current_trust >= 21:
		return "中立"
	else:
		return "警惕"


# ==================== 数据获取 ====================

func get_villager_data() -> Dictionary:
	"""获取村民完整数据"""
	return _villager_data


func get_personality() -> String:
	"""获取性格描述"""
	return _villager_data.get("personality", "")


func get_secrets() -> Array:
	"""获取秘密列表"""
	return _villager_data.get("secrets", [])


func get_relationships() -> Dictionary:
	"""获取关系网络"""
	return _villager_data.get("relationships", {})