## PauseMenu - 游戏暂停菜单
extends Control

# ==================== 信号 ====================
signal resume_pressed
signal save_pressed
signal load_pressed
signal quit_to_menu_pressed

# ==================== 节点引用 ====================
@onready var resume_button: Button = $PanelContainer/VBoxContainer/ResumeButton
@onready var save_button: Button = $PanelContainer/VBoxContainer/SaveButton
@onready var load_button: Button = $PanelContainer/VBoxContainer/LoadButton
@onready var quit_button: Button = $PanelContainer/VBoxContainer/QuitButton


func _ready() -> void:
	_connect_signals()


func _connect_signals() -> void:
	if resume_button:
		resume_button.pressed.connect(_on_resume_pressed)
	if save_button:
		save_button.pressed.connect(_on_save_pressed)
	if load_button:
		load_button.pressed.connect(_on_load_pressed)
	if quit_button:
		quit_button.pressed.connect(_on_quit_pressed)


func _on_resume_pressed() -> void:
	resume_pressed.emit()
	hide()


func _on_save_pressed() -> void:
	save_pressed.emit()


func _on_load_pressed() -> void:
	load_pressed.emit()


func _on_quit_pressed() -> void:
	quit_to_menu_pressed.emit()


func show_menu() -> void:
	show()


func hide_menu() -> void:
	hide()