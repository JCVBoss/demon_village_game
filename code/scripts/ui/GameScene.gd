## GameScene - 游戏主场景脚本
extends Node2D

# ==================== 引用 ====================
@onready var day_label: Label = $UIRoot/TopBar/HBoxContainer/DayLabel
@onready var action_points_label: Label = $UIRoot/TopBar/HBoxContainer/ActionPointsLabel
@onready var dialogue_box: Control = $UIRoot/DialogueBox
@onready var menu_button: Button = $UIRoot/BottomBar/MenuButton

# ==================== 测试用 ====================
var test_villager_id := "chenmo"


func _ready() -> void:
	_connect_signals()
	_connect_game_manager_signals()
	_update_ui()
	_show_test_dialogue()


func _connect_signals() -> void:
	menu_button.pressed.connect(_on_menu_pressed)


func _connect_game_manager_signals() -> void:
	GameManager.day_changed.connect(_on_day_changed)
	GameManager.action_points_changed.connect(_on_action_points_changed)
	DialogueManager.dialogue_started.connect(_on_dialogue_started)
	DialogueManager.dialogue_ended.connect(_on_dialogue_ended)


func _update_ui() -> void:
	day_label.text = "第 %d 天" % GameManager.current_day
	action_points_label.text = "行动点: %d/%d" % [GameManager.action_points, GameManager.MAX_ACTION_POINTS]


# ==================== 信号回调 ====================

func _on_day_changed(new_day: int) -> void:
	day_label.text = "第 %d 天" % new_day


func _on_action_points_changed(new_points: int) -> void:
	action_points_label.text = "行动点: %d/%d" % [new_points, GameManager.MAX_ACTION_POINTS]


func _on_menu_pressed() -> void:
	# TODO: 打开游戏菜单
	GameManager.pause_game()


func _on_dialogue_started(_villager_id: String) -> void:
	dialogue_box.show()


func _on_dialogue_ended(_villager_id: String) -> void:
	dialogue_box.hide()


# ==================== 测试功能 ====================

func _show_test_dialogue() -> void:
	# 延迟显示测试对话
	await get_tree().create_timer(1.0).timeout
	dialogue_box.start_dialogue(test_villager_id)