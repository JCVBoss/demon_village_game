## Main - 主入口脚本
## 负责游戏启动和场景管理
extends Node

# ==================== 引用 ====================
@onready var ui_root: CanvasLayer = $UIRoot
@onready var main_menu: Control = $UIRoot/MainMenu
@onready var save_load_ui: Control = $UIRoot/SaveLoadUI

# ==================== 场景路径 ====================
const GAME_SCENE_PATH := "res://scenes/locations/Village.tscn"


func _ready() -> void:
	print("[Main] 游戏启动")
	_connect_signals()


func _connect_signals() -> void:
	# 连接主菜单信号
	if main_menu:
		main_menu.new_game_pressed.connect(_on_new_game_pressed)
		main_menu.load_game_pressed.connect(_on_load_game_pressed)
		main_menu.quit_pressed.connect(_on_quit_pressed)

	# 连接存档界面信号
	if save_load_ui:
		save_load_ui.load_completed.connect(_on_load_completed)
		save_load_ui.cancelled.connect(_on_save_load_cancelled)


func _on_new_game_pressed() -> void:
	print("[Main] 开始新游戏")
	GameManager.start_new_game()
	_load_game_scene()


func _on_load_game_pressed() -> void:
	print("[Main] 打开存档界面")
	if save_load_ui:
		save_load_ui.show_load_mode()


func _on_load_completed(_slot_index: int) -> void:
	print("[Main] 存档加载完成")
	if save_load_ui:
		save_load_ui.hide()
	_load_game_scene()


func _on_save_load_cancelled() -> void:
	print("[Main] 取消存档操作")
	if save_load_ui:
		save_load_ui.hide()


func _on_quit_pressed() -> void:
	print("[Main] 退出游戏")
	get_tree().quit()


func _load_game_scene() -> void:
	var result = get_tree().change_scene_to_file(GAME_SCENE_PATH)
	if result != OK:
		push_error("[Main] 无法加载游戏场景: %s" % GAME_SCENE_PATH)