## SaveLoadUI - 存档/读档界面
## 管理存档槽位、保存和加载游戏
extends Control

# ==================== 信号 ====================
signal save_completed(slot_index: int)
signal load_completed(slot_index: int)
signal cancelled

# ==================== 导出变量 ====================
@export var max_slots: int = 5  ## 最大存档槽位数
@export var mode: String = "load"  ## 模式：load 或 save

# ==================== 节点引用 ====================
@onready var title_label: Label = $PanelContainer/VBoxContainer/TitleLabel
@onready var slots_container: VBoxContainer = $PanelContainer/VBoxContainer/ScrollContainer/SlotsContainer
@onready var back_button: Button = $PanelContainer/VBoxContainer/HBoxContainer/BackButton

# ==================== 配置 ====================
const SaveSlotScene = preload("res://scenes/ui/SaveSlot.tscn")

# 存档槽位数组
var slots: Array = []


func _ready() -> void:
	_setup_ui()
	_load_all_saves()
	_connect_signals()


# ==================== 初始化 ====================

func _setup_ui() -> void:
	"""设置UI"""
	# 设置标题
	if title_label:
		if mode == "save":
			title_label.text = "保存游戏"
		else:
			title_label.text = "读取存档"

	# 生成存档槽位
	if slots_container:
		for child in slots_container.get_children():
			child.queue_free()

		slots.clear()

		for i in range(max_slots):
			var slot = SaveSlotScene.instantiate()
			slot.slot_index = i
			slots_container.add_child(slot)
			slots.append(slot)


func _connect_signals() -> void:
	"""连接信号"""
	if back_button:
		back_button.pressed.connect(_on_back_pressed)

	# 连接槽位信号
	for slot in slots:
		slot.slot_selected.connect(_on_slot_selected)
		slot.slot_deleted.connect(_on_slot_deleted)


# ==================== 存档操作 ====================

func _load_all_saves() -> void:
	"""加载所有存档信息"""
	for i in range(max_slots):
		var save_data = _load_save_data(i)
		var is_empty = save_data.is_empty()
		slots[i].update_display(save_data, is_empty)


func _load_save_data(slot_index: int) -> Dictionary:
	"""加载单个存档数据"""
	var file_path = "user://save_%d.json" % slot_index
	var file = FileAccess.open(file_path, FileAccess.READ)

	if file:
		var json_string = file.get_as_text()
		file.close()

		var json = JSON.new()
		if json.parse(json_string) == OK:
			return json.data

	return {}


func _save_game(slot_index: int) -> bool:
	"""保存游戏到指定槽位"""
	var save_data = {
		"version": "0.1.0",
		"timestamp": Time.get_unix_time_from_system(),
		"current_day": GameManager.current_day,
		"action_points": GameManager.action_points,
		"player_data": GameManager.player_data.duplicate(true),
		"game_state": {
			"current_state": GameManager.current_state,
			"is_first_play": GameManager.is_first_play
		},
		"trust_data": TrustManager.get_save_data(),
		"event_data": EventManager.get_save_data()
	}

	var file_path = "user://save_%d.json" % slot_index
	var file = FileAccess.open(file_path, FileAccess.WRITE)

	if file:
		file.store_string(JSON.stringify(save_data, "  "))
		file.close()
		print("[SaveLoadUI] 游戏已保存到槽位 %d" % slot_index)
		return true

	print("[SaveLoadUI] 保存失败")
	return false


func _load_game(slot_index: int) -> bool:
	"""从指定槽位加载游戏"""
	var save_data = _load_save_data(slot_index)

	if save_data.is_empty():
		print("[SaveLoadUI] 槽位 %d 为空" % slot_index)
		return false

	# 恢复游戏状态
	GameManager.current_day = save_data.get("current_day", 1)
	GameManager.action_points = save_data.get("action_points", 4)
	GameManager.player_data = save_data.get("player_data", {})
	GameManager.current_state = save_data.get("game_state", {}).get("current_state", 0)
	GameManager.is_first_play = save_data.get("game_state", {}).get("is_first_play", false)

	# 恢复信任系统数据
	var trust_data = save_data.get("trust_data", {})
	if not trust_data.is_empty():
		TrustManager.load_save_data(trust_data)

	# 恢复事件系统数据
	var event_data = save_data.get("event_data", {})
	if not event_data.is_empty():
		EventManager.load_save_data(event_data)

	print("[SaveLoadUI] 已从槽位 %d 加载游戏" % slot_index)
	return true


func _delete_save(slot_index: int) -> bool:
	"""删除指定槽位的存档"""
	var file_path = "user://save_%d.json" % slot_index
	var dir = DirAccess.open("user://")

	if dir and dir.file_exists(file_path):
		dir.remove(file_path)
		print("[SaveLoadUI] 已删除槽位 %d 的存档" % slot_index)
		return true

	return false


# ==================== 信号处理 ====================

func _on_slot_selected(slot_index: int) -> void:
	"""槽位被选中"""
	if mode == "save":
		# 保存模式：直接保存
		if _save_game(slot_index):
			_load_all_saves()  # 刷新显示
			save_completed.emit(slot_index)
	else:
		# 读取模式：加载存档
		var save_data = _load_save_data(slot_index)
		if not save_data.is_empty():
			if _load_game(slot_index):
				load_completed.emit(slot_index)
		else:
			print("[SaveLoadUI] 槽位 %d 为空，无法加载" % slot_index)


func _on_slot_deleted(slot_index: int) -> void:
	"""删除存档"""
	_delete_save(slot_index)
	_load_all_saves()  # 刷新显示


func _on_back_pressed() -> void:
	"""返回按钮"""
	cancelled.emit()
	hide()


# ==================== 公共方法 ====================

func show_save_mode() -> void:
	"""显示保存模式"""
	mode = "save"
	_setup_ui()
	_connect_signals()
	_load_all_saves()
	show()


func show_load_mode() -> void:
	"""显示读取模式"""
	mode = "load"
	_setup_ui()
	_connect_signals()
	_load_all_saves()
	show()