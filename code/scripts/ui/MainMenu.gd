## MainMenu - 主菜单脚本
extends Control

# ==================== 信号 ====================
signal new_game_pressed
signal continue_pressed
signal load_game_pressed
signal quit_pressed

# ==================== 引用 ====================
@onready var new_game_button: Button = $VBoxContainer/NewGameButton
@onready var continue_button: Button = $VBoxContainer/ContinueButton
@onready var quit_button: Button = $VBoxContainer/QuitButton


func _ready() -> void:
	_connect_buttons()
	_check_save_files()


func _connect_buttons() -> void:
	if new_game_button:
		new_game_button.pressed.connect(_on_new_game_pressed)
	if continue_button:
		continue_button.pressed.connect(_on_continue_pressed)
	if quit_button:
		quit_button.pressed.connect(_on_quit_pressed)


func _check_save_files() -> void:
	# 检查是否有任何存档
	var has_save = false
	for i in range(5):
		if FileAccess.file_exists("user://save_%d.json" % i):
			has_save = true
			break

	if continue_button:
		continue_button.disabled = not has_save


func _on_new_game_pressed() -> void:
	new_game_pressed.emit()


func _on_continue_pressed() -> void:
	load_game_pressed.emit()


func _on_quit_pressed() -> void:
	quit_pressed.emit()