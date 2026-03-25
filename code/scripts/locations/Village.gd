## Village - 村庄主场景
## 包含村庄背景、村民角色、交互系统
extends Node2D

# ==================== 信号 ====================
signal villager_selected(villager_id: String)

# ==================== 导出变量 ====================
@export var village_name: String = "暮色村"

# ==================== 节点引用 ====================
@onready var villagers_container: Node2D = $Villagers
@onready var player: CharacterBody2D = $Player
@onready var dialogue_box: PanelContainer = $UIRoot/DialogueBox
@onready var village_ui: CanvasLayer = $UIRoot

# ==================== 配置 ====================
const VillagerScene = preload("res://scenes/characters/Villager.tscn")

# 村民位置配置 (ID -> 位置)
const VILLAGER_POSITIONS: Dictionary = {
	"chenmo": Vector2(200, 300),
	"leishu": Vector2(400, 250),
	"jinling": Vector2(600, 350),
	"baizhi": Vector2(300, 450),
	"john": Vector2(150, 200),
	"daxiong": Vector2(700, 200),
	"ying": Vector2(850, 400),
	"xiaoan": Vector2(500, 500),
	"ahu": Vector2(100, 400),
	"yeya": Vector2(800, 300)
}


func _ready() -> void:
	print("[Village] 进入村庄: %s" % village_name)

	# 连接对话管理器信号
	_connect_dialogue_signals()

	# 生成村民
	_spawn_villagers()

	# 更新 UI
	_update_ui()


# ==================== 信号连接 ====================

func _connect_dialogue_signals() -> void:
	"""连接对话管理器信号"""
	DialogueManager.dialogue_line_spoken.connect(_on_dialogue_line)
	DialogueManager.choice_presented.connect(_on_choices_presented)
	DialogueManager.dialogue_ended.connect(_on_dialogue_ended)


# ==================== 村民生成 ====================

func _spawn_villagers() -> void:
	"""根据配置生成所有村民"""
	for villager_id in VILLAGER_POSITIONS:
		var villager = VillagerScene.instantiate()
		villager.villager_id = villager_id
		villager.position = VILLAGER_POSITIONS[villager_id]

		# 连接对话信号
		villager.dialogue_started.connect(_on_villager_dialogue_started)
		villager.dialogue_ended.connect(_on_villager_dialogue_ended)

		villagers_container.add_child(villager)

	print("[Village] 已生成 %d 位村民" % VILLAGER_POSITIONS.size())


# ==================== 对话系统回调 ====================

func _on_villager_dialogue_started(villager_id: String) -> void:
	"""村民对话开始"""
	print("[Village] 村民 %s 开始对话" % villager_id)
	villager_selected.emit(villager_id)

	# 显示对话框
	if dialogue_box:
		dialogue_box.show()

	# 消耗行动点
	GameManager.use_action_point(1)


func _on_villager_dialogue_ended() -> void:
	"""村民对话结束"""
	print("[Village] 对话结束")
	# 隐藏对话框
	if dialogue_box:
		dialogue_box.hide()


func _on_dialogue_line(_speaker: String, _text: String) -> void:
	"""对话行显示 - 由 DialogueBox 处理"""
	pass


func _on_choices_presented(_choices: Array) -> void:
	"""选项显示 - 由 DialogueBox 处理"""
	pass


func _on_dialogue_ended(_villager_id: String) -> void:
	"""对话结束回调"""
	# 隐藏对话框
	if dialogue_box:
		dialogue_box.hide()


# ==================== UI 更新 ====================

func _update_ui() -> void:
	"""更新 UI 显示"""
	# 更新天数和行动点显示
	var day_label = get_node_or_null("UIRoot/TopBar/HBoxContainer/DayLabel")
	var action_label = get_node_or_null("UIRoot/TopBar/HBoxContainer/ActionPointsLabel")
	var village_label = get_node_or_null("UIRoot/TopBar/HBoxContainer/VillageNameLabel")

	if day_label:
		day_label.text = "第 %d 天" % GameManager.current_day

	if action_label:
		action_label.text = "行动点: %d/%d" % [GameManager.action_points, GameManager.MAX_ACTION_POINTS]

	if village_label:
		village_label.text = village_name


# ==================== 游戏流程 ====================

func advance_to_next_day() -> void:
	"""进入下一天"""
	# 更新 UI
	_update_ui()

	# 触发每日事件
	EventManager.trigger_daily_events(GameManager.current_day)

	print("[Village] 进入第 %d 天" % GameManager.current_day)


# ==================== 输入处理 ====================

func _input(event: InputEvent) -> void:
	"""处理输入"""
	# ESC 键打开菜单
	if event.is_action_pressed("ui_cancel"):
		_on_menu_button_pressed()


func _on_menu_button_pressed() -> void:
	"""菜单按钮按下"""
	print("[Village] 打开菜单")
	# TODO: 实现暂停菜单