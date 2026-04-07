## SaveSystem - 存档系统
## 负责游戏数据的保存和加载
extends Node

# ==================== 信号 ====================
signal save_completed(slot_index: int)
signal load_completed(slot_index: int)
signal save_failed(slot_index: int)
signal load_failed(slot_index: int)

# ==================== 配置 ====================
const MAX_SLOTS: int = 5
const SAVE_DIR: String = "user://saves/"
const CURRENT_VERSION: String = "0.1.0"

# ==================== 状态 ====================
var current_slot: int = -1
var last_save_time: float = 0.0


func _ready() -> void:
	print("[SaveSystem] 存档系统初始化完成")
	_ensure_save_directory()


func _ensure_save_directory() -> void:
	"""确保存档目录存在"""
	var dir = DirAccess.open("user://")
	if dir and not dir.dir_exists("saves"):
		dir.make_dir("saves")
		print("[SaveSystem] 创建存档目录")


# ==================== 存档操作 ====================

## 保存游戏
func save_game(slot_index: int) -> bool:
	if slot_index < 0 or slot_index >= MAX_SLOTS:
		print("[SaveSystem] 无效的存档槽位: %d" % slot_index)
		return false

	var save_data = _collect_save_data()
	var file_path = _get_save_path(slot_index)

	var file = FileAccess.open(file_path, FileAccess.WRITE)
	if file == null:
		print("[SaveSystem] 无法创建存档文件: %s" % file_path)
		save_failed.emit(slot_index)
		return false

	file.store_string(JSON.stringify(save_data, "  "))
	file.close()

	current_slot = slot_index
	last_save_time = Time.get_unix_time_from_system()

	print("[SaveSystem] 游戏已保存到槽位 %d" % slot_index)
	save_completed.emit(slot_index)
	return true


## 加载游戏
func load_game(slot_index: int) -> bool:
	if slot_index < 0 or slot_index >= MAX_SLOTS:
		print("[SaveSystem] 无效的存档槽位: %d" % slot_index)
		return false

	var file_path = _get_save_path(slot_index)
	if not FileAccess.file_exists(file_path):
		print("[SaveSystem] 存档文件不存在: %s" % file_path)
		load_failed.emit(slot_index)
		return false

	var file = FileAccess.open(file_path, FileAccess.READ)
	if file == null:
		print("[SaveSystem] 无法读取存档文件: %s" % file_path)
		load_failed.emit(slot_index)
		return false

	var json_string = file.get_as_text()
	file.close()

	var json = JSON.new()
	if json.parse(json_string) != OK:
		print("[SaveSystem] 存档文件解析失败: %s" % json.get_error_message())
		load_failed.emit(slot_index)
		return false

	var save_data = json.data
	_apply_save_data(save_data)

	current_slot = slot_index
	print("[SaveSystem] 游戏已从槽位 %d 加载" % slot_index)
	load_completed.emit(slot_index)
	return true


## 删除存档
func delete_save(slot_index: int) -> bool:
	var file_path = _get_save_path(slot_index)
	var dir = DirAccess.open("user://saves/")

	if dir and dir.file_exists(file_path.get_file()):
		dir.remove(file_path.get_file())
		print("[SaveSystem] 已删除槽位 %d 的存档" % slot_index)
		return true

	return false


# ==================== 数据收集和应用 ====================

## 收集存档数据
func _collect_save_data() -> Dictionary:
	# 获取玩家位置
	var player_pos = Vector2.ZERO
	var player_node = get_tree().get_first_node_in_group("player")
	if player_node:
		player_pos = player_node.global_position

	return {
		"version": CURRENT_VERSION,
		"timestamp": Time.get_unix_time_from_system(),
		"current_day": GameManager.current_day,
		"action_points": GameManager.action_points,
		"player_data": GameManager.player_data.duplicate(true),
		"player_position": {"x": player_pos.x, "y": player_pos.y},
		"game_state": {
			"current_state": GameManager.current_state,
			"is_first_play": GameManager.is_first_play
		},
		"trust_data": TrustManager.get_save_data(),
		"event_data": EventManager.get_save_data(),
		"trigger_data": EventTriggerSystem.get_save_data() if EventTriggerSystem else {},
		"dialogue_data": DialogueManager.get_save_data() if DialogueManager else {}
	}


## 应用存档数据
func _apply_save_data(data: Dictionary) -> void:
	# 恢复游戏状态
	GameManager.current_day = data.get("current_day", 1)
	GameManager.action_points = data.get("action_points", 4)
	GameManager.player_data = data.get("player_data", {})
	GameManager.current_state = data.get("game_state", {}).get("current_state", 0)
	GameManager.is_first_play = data.get("game_state", {}).get("is_first_play", false)

	# 存储玩家位置供场景恢复使用
	var player_pos_data = data.get("player_position", {})
	if not player_pos_data.is_empty():
		GameManager.player_data["saved_position"] = Vector2(
			player_pos_data.get("x", 960),
			player_pos_data.get("y", 800)
		)

	# 恢复各系统数据
	var trust_data = data.get("trust_data", {})
	if not trust_data.is_empty():
		TrustManager.load_save_data(trust_data)

	var event_data = data.get("event_data", {})
	if not event_data.is_empty():
		EventManager.load_save_data(event_data)

	var trigger_data = data.get("trigger_data", {})
	if not trigger_data.is_empty() and EventTriggerSystem:
		EventTriggerSystem.load_save_data(trigger_data)

	var dialogue_data = data.get("dialogue_data", {})
	if not dialogue_data.is_empty() and DialogueManager:
		DialogueManager.load_save_data(dialogue_data)


# ==================== 存档信息查询 ====================

## 获取存档信息
func get_save_info(slot_index: int) -> Dictionary:
	var file_path = _get_save_path(slot_index)
	if not FileAccess.file_exists(file_path):
		return {}

	var file = FileAccess.open(file_path, FileAccess.READ)
	if file == null:
		return {}

	var json_string = file.get_as_text()
	file.close()

	var json = JSON.new()
	if json.parse(json_string) != OK:
		return {}

	var data = json.data
	return {
		"slot": slot_index,
		"day": data.get("current_day", 1),
		"timestamp": data.get("timestamp", 0),
		"version": data.get("version", "unknown"),
		"player_name": data.get("player_data", {}).get("name", "勇者")
	}


## 获取所有存档信息
func get_all_save_info() -> Array:
	var result = []
	for i in range(MAX_SLOTS):
		var info = get_save_info(i)
		if not info.is_empty():
			result.append(info)
	return result


## 检查存档是否存在
func has_save(slot_index: int) -> bool:
	return FileAccess.file_exists(_get_save_path(slot_index))


## 获取存档文件路径
func _get_save_path(slot_index: int) -> String:
	return "%ssave_%d.json" % [SAVE_DIR, slot_index]


## 获取格式化的存档时间
func get_formatted_time(slot_index: int) -> String:
	var info = get_save_info(slot_index)
	if info.is_empty():
		return "空"

	var timestamp = info.get("timestamp", 0)
	if timestamp == 0:
		return "未知"

	var datetime = Time.get_datetime_dict_from_unix_time(timestamp)
	return "%04d-%02d-%02d %02d:%02d" % [
		datetime.year, datetime.month, datetime.day,
		datetime.hour, datetime.minute
	]


# ==================== 快速存档/读档 ====================

## 快速存档（使用当前槽位或槽位0）
func quick_save() -> bool:
	var slot = current_slot if current_slot >= 0 else 0
	return save_game(slot)


## 快速读档（使用当前槽位或槽位0）
func quick_load() -> bool:
	var slot = current_slot if current_slot >= 0 else 0
	return load_game(slot)


## 自动存档
func auto_save() -> bool:
	# 使用最后一个槽位作为自动存档
	return save_game(MAX_SLOTS - 1)