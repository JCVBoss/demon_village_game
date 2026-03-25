## Main - 主入口脚本
## 负责游戏启动和场景管理
extends Node

# ==================== 引用 ====================
@onready var ui_root: CanvasLayer = $UIRoot
@onready var main_menu: Control = $UIRoot/MainMenu

# ==================== 场景路径 ====================
const GAME_SCENE_PATH := "res://scenes/locations/Village.tscn"


func _ready() -> void:
	print("[Main] 游戏启动")
	_connect_signals()


func _connect_signals() -> void:
	# 连接主菜单信号
	if main_menu:
		main_menu.new_game_pressed.connect(_on_new_game_pressed)
		main_menu.continue_pressed.connect(_on_continue_pressed)
		main_menu.quit_pressed.connect(_on_quit_pressed)


func _on_new_game_pressed() -> void:
	print("[Main] 开始新游戏")
	GameManager.start_new_game()
	_load_game_scene()


func _on_continue_pressed() -> void:
	print("[Main] 继续游戏")
	if GameManager.continue_game():
		_load_game_scene()
	else:
		# 显示无存档提示
		print("[Main] 没有可用的存档")


func _on_quit_pressed() -> void:
	print("[Main] 退出游戏")
	get_tree().quit()


func _load_game_scene() -> void:
	var result = get_tree().change_scene_to_file(GAME_SCENE_PATH)
	if result != OK:
		push_error("[Main] 无法加载游戏场景: %s" % GAME_SCENE_PATH)