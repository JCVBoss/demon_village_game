## GameScene - 游戏主场景脚本
extends Node2D

# ==================== 引用 ====================
@onready var background: TextureRect = $UIRoot/Background
@onready var day_label: Label = $UIRoot/TopBar/HBoxContainer/DayLabel
@onready var action_points_label: Label = $UIRoot/TopBar/HBoxContainer/ActionPointsLabel
@onready var dialogue_box: Control = $UIRoot/DialogueBox
@onready var menu_button: Button = $UIRoot/BottomBar/MenuButton

# ==================== 测试用 ====================
var test_villager_id := "chenmo"

## 场景类型
enum SceneType { VILLAGE, FOREST }
var current_scene: SceneType = SceneType.VILLAGE

## 时间段
enum TimeOfDay { DAY, TWILIGHT, NIGHT }
var current_time: TimeOfDay = TimeOfDay.DAY


func _ready() -> void:
	_connect_signals()
	_connect_game_manager_signals()
	_update_ui()
	_update_background()
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


# ==================== 背景系统 ====================

func _update_background() -> void:
	"""根据场景和时间更新背景"""
	var scene_name = "village" if current_scene == SceneType.VILLAGE else "forest"
	var time_name = _get_time_name()

	var bg_path = "res://assets/sprites/backgrounds/%s_%s.png" % [scene_name, time_name]

	if ResourceLoader.exists(bg_path):
		background.texture = load(bg_path)
	else:
		# 如果没有对应背景，使用纯色
		background.texture = null


func _get_time_name() -> String:
	"""获取时间段名称"""
	match current_time:
		TimeOfDay.DAY:
			return "day"
		TimeOfDay.TWILIGHT:
			return "twilight"
		TimeOfDay.NIGHT:
			return "night"
	return "day"


func set_scene(scene_type: SceneType) -> void:
	"""切换场景"""
	current_scene = scene_type
	_update_background()


func set_time_of_day(time: TimeOfDay) -> void:
	"""设置时间段"""
	current_time = time
	_update_background()


# ==================== 信号回调 ====================

func _on_day_changed(new_day: int) -> void:
	day_label.text = "第 %d 天" % new_day
	# 可以根据天数切换时间段
	_update_background()


func _on_action_points_changed(new_points: int) -> void:
	action_points_label.text = "行动点: %d/%d" % [new_points, GameManager.MAX_ACTION_POINTS]
	# 行动点变化时可以切换时间段
	_update_time_from_action_points(new_points)


func _update_time_from_action_points(points: int) -> void:
	"""根据行动点数更新时间段"""
	var max_points = GameManager.MAX_ACTION_POINTS

	if points > max_points * 0.6:
		current_time = TimeOfDay.DAY
	elif points > max_points * 0.3:
		current_time = TimeOfDay.TWILIGHT
	else:
		current_time = TimeOfDay.NIGHT

	_update_background()


func _on_menu_pressed() -> void:
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