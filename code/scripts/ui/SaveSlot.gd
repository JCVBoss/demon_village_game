## SaveSlot - 存档槽位组件
## 显示单个存档的信息
extends Button

# ==================== 信号 ====================
signal slot_selected(slot_index: int)
signal slot_deleted(slot_index: int)

# ==================== 导出变量 ====================
@export var slot_index: int = 0

# ==================== 节点引用 ====================
@onready var slot_label: Label = $HBoxContainer/SlotLabel
@onready var info_label: Label = $HBoxContainer/InfoLabel
@onready var delete_button: Button = $HBoxContainer/DeleteButton

# ==================== 状态 ====================
var is_empty: bool = true
var save_data: Dictionary = {}


func _ready() -> void:
	pressed.connect(_on_pressed)
	if delete_button:
		delete_button.pressed.connect(_on_delete_pressed)


# ==================== 公共方法 ====================

func update_display(data: Dictionary, empty: bool = true) -> void:
	"""更新存档槽位显示"""
	is_empty = empty
	save_data = data

	if slot_label:
		slot_label.text = "槽位 %d" % (slot_index + 1)

	if is_empty:
		if info_label:
			info_label.text = "空槽位"
		if delete_button:
			delete_button.visible = false
	else:
		# 显示存档信息
		var day = data.get("current_day", 1)
		var action_points = data.get("action_points", 4)
		var timestamp = data.get("timestamp", 0)

		var time_str = ""
		if timestamp > 0:
			var datetime = Time.get_datetime_dict_from_unix_time(timestamp)
			time_str = "%04d-%02d-%02d %02d:%02d" % [
				datetime.year, datetime.month, datetime.day,
				datetime.hour, datetime.minute
			]

		if info_label:
			info_label.text = "第%d天 | 行动点:%d | %s" % [day, action_points, time_str]

		if delete_button:
			delete_button.visible = true


# ==================== 信号处理 ====================

func _on_pressed() -> void:
	slot_selected.emit(slot_index)


func _on_delete_pressed() -> void:
	slot_deleted.emit(slot_index)