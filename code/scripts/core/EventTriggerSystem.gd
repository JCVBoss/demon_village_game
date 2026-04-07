## EventTriggerSystem - 事件触发系统
## 负责管理各类事件触发器（位置/对话/物品/时间）
extends Node

# ==================== 信号 ====================
signal trigger_activated(trigger_id: String, trigger_data: Dictionary)
signal trigger_completed(trigger_id: String)

# ==================== 触发器类型 ====================
enum TriggerType {
	POSITION,		## 位置触发器（进入/离开区域）
	DIALOGUE,		## 对话触发器（与 NPC 对话后）
	ITEM,			## 物品触发器（获得/使用物品）
	TIME,			## 时间触发器（特定天数/时间）
	STORY_FLAG,		## 故事标志触发器
	COMBINATION		## 组合触发器（多个条件）
}

# ==================== 触发器状态 ====================
enum TriggerState {
	INACTIVE,		## 未激活
	ACTIVE,			## 已激活，等待触发
	TRIGGERED,		## 已触发
	COMPLETED,		## 已完成
	DISABLED		## 已禁用
}

# ==================== 数据 ====================
var triggers: Dictionary = {}
var active_triggers: Array = []
var completed_triggers: Array = []

# 位置触发器区域
var position_areas: Dictionary = {}

# ==================== 引用 ====================
var player: CharacterBody2D = null


func _ready() -> void:
	print("[EventTriggerSystem] 事件触发系统初始化完成")


func _process(_delta: float) -> void:
	# 检查位置触发器
	_check_position_triggers()


# ==================== 初始化 ====================

## 设置玩家引用
func set_player(player_node: CharacterBody2D) -> void:
	player = player_node


## 加载触发器配置
func load_triggers(config_path: String) -> bool:
	if not ResourceLoader.exists(config_path):
		print("[EventTriggerSystem] 配置文件不存在: %s" % config_path)
		return false

	var file = FileAccess.open(config_path, FileAccess.READ)
	if file == null:
		return false

	var json_text = file.get_as_text()
	file.close()

	var json = JSON.new()
	if json.parse(json_text) != OK:
		print("[EventTriggerSystem] JSON 解析错误: %s" % json.get_error_message())
		return false

	var data = json.data
	for trigger_id in data.get("triggers", {}):
		register_trigger(trigger_id, data.triggers[trigger_id])

	print("[EventTriggerSystem] 加载了 %d 个触发器" % triggers.size())
	return true


## 注册触发器
func register_trigger(trigger_id: String, config: Dictionary) -> void:
	var trigger = {
		"id": trigger_id,
		"type": _parse_trigger_type(config.get("type", "position")),
		"state": TriggerState.INACTIVE,
		"config": config,
		"trigger_count": 0,
		"max_triggers": config.get("max_triggers", 1),  # 最大触发次数
		"one_shot": config.get("one_shot", true),  # 是否只触发一次
		"cooldown": config.get("cooldown", 0.0),  # 冷却时间
		"last_triggered": 0.0  # 上次触发时间
	}

	triggers[trigger_id] = trigger

	# 如果是位置触发器，创建检测区域
	if trigger.type == TriggerType.POSITION:
		_create_position_area(trigger_id, config)


func _parse_trigger_type(type_str: String) -> TriggerType:
	match type_str.to_lower():
		"position", "area":
			return TriggerType.POSITION
		"dialogue", "conversation":
			return TriggerType.DIALOGUE
		"item", "inventory":
			return TriggerType.ITEM
		"time", "day":
			return TriggerType.TIME
		"flag", "story_flag":
			return TriggerType.STORY_FLAG
		"combination", "multi":
			return TriggerType.COMBINATION
		_:
			return TriggerType.POSITION


# ==================== 位置触发器 ====================

## 创建位置检测区域
func _create_position_area(trigger_id: String, config: Dictionary) -> void:
	var area_data = {
		"trigger_id": trigger_id,
		"position": Vector2(config.get("x", 0), config.get("y", 0)),
		"size": Vector2(config.get("width", 100), config.get("height", 100)),
		"shape": config.get("shape", "rectangle"),  # rectangle 或 circle
		"radius": config.get("radius", 50.0)
	}
	position_areas[trigger_id] = area_data


## 检查位置触发器
func _check_position_triggers() -> void:
	if player == null:
		return

	var player_pos = player.global_position

	for trigger_id in position_areas:
		var trigger = triggers.get(trigger_id)
		if trigger == null or trigger.state == TriggerState.DISABLED:
			continue

		if trigger.state == TriggerState.COMPLETED and trigger.one_shot:
			continue

		var area = position_areas[trigger_id]
		var is_inside = false

		if area.shape == "rectangle":
			is_inside = _is_in_rect(player_pos, area.position, area.size)
		else:  # circle
			is_inside = _is_in_circle(player_pos, area.position, area.radius)

		if is_inside:
			if trigger.state == TriggerState.INACTIVE:
				_activate_trigger(trigger_id)
			elif trigger.state == TriggerState.ACTIVE:
				_try_trigger(trigger_id)
		else:
			if trigger.state == TriggerState.ACTIVE:
				_deactivate_trigger(trigger_id)


func _is_in_rect(point: Vector2, rect_pos: Vector2, rect_size: Vector2) -> bool:
	return point.x >= rect_pos.x and point.x <= rect_pos.x + rect_size.x and \
		   point.y >= rect_pos.y and point.y <= rect_pos.y + rect_size.y


func _is_in_circle(point: Vector2, center: Vector2, radius: float) -> bool:
	return point.distance_to(center) <= radius


# ==================== 对话触发器 ====================

## 检查对话触发器
func check_dialogue_trigger(villager_id: String, dialogue_id: String) -> void:
	for trigger_id in triggers:
		var trigger = triggers[trigger_id]
		if trigger.type != TriggerType.DIALOGUE:
			continue
		if trigger.state == TriggerState.DISABLED or trigger.state == TriggerState.COMPLETED:
			continue

		var config = trigger.config
		var target_villager = config.get("villager_id", "")
		var target_dialogue = config.get("dialogue_id", "")

		if (target_villager == "" or target_villager == villager_id) and \
		   (target_dialogue == "" or target_dialogue == dialogue_id):
			_try_trigger(trigger_id)


## 对话结束后检查
func on_dialogue_ended(villager_id: String) -> void:
	check_dialogue_trigger(villager_id, "")


# ==================== 物品触发器 ====================

## 检查物品触发器
func check_item_trigger(item_id: String, action: String = "obtain") -> void:
	for trigger_id in triggers:
		var trigger = triggers[trigger_id]
		if trigger.type != TriggerType.ITEM:
			continue
		if trigger.state == TriggerState.DISABLED or trigger.state == TriggerState.COMPLETED:
			continue

		var config = trigger.config
		var target_item = config.get("item_id", "")
		var target_action = config.get("action", "obtain")

		if target_item == item_id and (target_action == "" or target_action == action):
			_try_trigger(trigger_id)


## 物品获得
func on_item_obtained(item_id: String) -> void:
	check_item_trigger(item_id, "obtain")


## 物品使用
func on_item_used(item_id: String) -> void:
	check_item_trigger(item_id, "use")


# ==================== 时间触发器 ====================

## 检查时间触发器
func check_time_trigger(current_day: int) -> void:
	for trigger_id in triggers:
		var trigger = triggers[trigger_id]
		if trigger.type != TriggerType.TIME:
			continue
		if trigger.state == TriggerState.DISABLED or trigger.state == TriggerState.COMPLETED:
			continue

		var config = trigger.config
		var target_day = config.get("day", 0)
		var day_range = config.get("day_range", [])

		var should_trigger = false

		if target_day > 0 and current_day >= target_day:
			should_trigger = true
		elif day_range.size() == 2:
			if current_day >= day_range[0] and current_day <= day_range[1]:
				should_trigger = true

		if should_trigger:
			_try_trigger(trigger_id)


# ==================== 故事标志触发器 ====================

## 检查故事标志触发器
func check_story_flag_trigger(flag_name: String, value: bool) -> void:
	for trigger_id in triggers:
		var trigger = triggers[trigger_id]
		if trigger.type != TriggerType.STORY_FLAG:
			continue
		if trigger.state == TriggerState.DISABLED or trigger.state == TriggerState.COMPLETED:
			continue

		var config = trigger.config
		var target_flag = config.get("flag_name", "")
		var target_value = config.get("value", true)

		if target_flag == flag_name and target_value == value:
			_try_trigger(trigger_id)


# ==================== 组合触发器 ====================

## 检查组合触发器
func check_combination_trigger(trigger_id: String) -> bool:
	var trigger = triggers.get(trigger_id)
	if trigger == null or trigger.type != TriggerType.COMBINATION:
		return false

	var config = trigger.config
	var conditions = config.get("conditions", [])
	var logic = config.get("logic", "and")  # and 或 or

	var results = []
	for condition in conditions:
		var condition_type = condition.get("type", "")
		var satisfied = false

		match condition_type:
			"trust":
				var villager = condition.get("villager_id", "")
				var min_trust = condition.get("min_trust", 0)
				satisfied = TrustManager.get_trust(villager) >= min_trust
			"flag":
				var flag_name = condition.get("flag_name", "")
				var flag_value = condition.get("value", true)
				satisfied = EventManager.get_story_flag(flag_name) == flag_value
			"day":
				var min_day = condition.get("min_day", 0)
				satisfied = GameManager.current_day >= min_day
			"event_completed":
				var event_id = condition.get("event_id", "")
				satisfied = event_id in EventManager.completed_events
			"dialogue_seen":
				var dialogue_id = condition.get("dialogue_id", "")
				satisfied = DialogueManager.has_seen_dialogue(dialogue_id)

		results.append(satisfied)

	if logic == "and":
		return results.all(func(r): return r)
	else:  # or
		return results.any(func(r): return r)


# ==================== 触发器状态管理 ====================

## 激活触发器
func _activate_trigger(trigger_id: String) -> void:
	var trigger = triggers.get(trigger_id)
	if trigger == null:
		return

	trigger.state = TriggerState.ACTIVE
	if trigger_id not in active_triggers:
		active_triggers.append(trigger_id)

	print("[EventTriggerSystem] 触发器激活: %s" % trigger_id)


## 停用触发器
func _deactivate_trigger(trigger_id: String) -> void:
	var trigger = triggers.get(trigger_id)
	if trigger == null:
		return

	trigger.state = TriggerState.INACTIVE
	if trigger_id in active_triggers:
		active_triggers.erase(trigger_id)


## 尝试触发
func _try_trigger(trigger_id: String) -> bool:
	var trigger = triggers.get(trigger_id)
	if trigger == null:
		return false

	# 检查是否可以触发
	if trigger.state == TriggerState.COMPLETED and trigger.one_shot:
		return false

	# 检查冷却时间
	if trigger.cooldown > 0:
		var current_time = Time.get_unix_time_from_system()
		if current_time - trigger.last_triggered < trigger.cooldown:
			return false

	# 检查组合条件
	if trigger.type == TriggerType.COMBINATION:
		if not check_combination_trigger(trigger_id):
			return false

	# 检查前置条件
	var prereqs = trigger.config.get("prerequisites", [])
	for prereq in prereqs:
		if prereq not in completed_triggers:
			print("[EventTriggerSystem] 触发器 %s 缺少前置条件: %s" % [trigger_id, prereq])
			return false

	# 触发
	trigger.state = TriggerState.TRIGGERED
	trigger.trigger_count += 1
	trigger.last_triggered = Time.get_unix_time_from_system()

	# 检查是否完成
	if trigger.one_shot or trigger.trigger_count >= trigger.max_triggers:
		trigger.state = TriggerState.COMPLETED
		if trigger_id not in completed_triggers:
			completed_triggers.append(trigger_id)

	# 发送触发信号
	var event_id = trigger.config.get("event_id", trigger_id)
	trigger_activated.emit(trigger_id, {
		"event_id": event_id,
		"trigger_data": trigger.config.get("trigger_data", {}),
		"trigger_type": trigger.type
	})

	print("[EventTriggerSystem] 触发器触发: %s -> 事件: %s" % [trigger_id, event_id])

	# 触发关联的事件
	if event_id != trigger_id:
		EventManager.trigger_event(event_id)

	return true


## 完成触发器
func complete_trigger(trigger_id: String) -> void:
	var trigger = triggers.get(trigger_id)
	if trigger == null:
		return

	trigger.state = TriggerState.COMPLETED
	if trigger_id not in completed_triggers:
		completed_triggers.append(trigger_id)
	if trigger_id in active_triggers:
		active_triggers.erase(trigger_id)

	trigger_completed.emit(trigger_id)
	print("[EventTriggerSystem] 触发器完成: %s" % trigger_id)


## 重置触发器
func reset_trigger(trigger_id: String) -> void:
	var trigger = triggers.get(trigger_id)
	if trigger == null:
		return

	trigger.state = TriggerState.INACTIVE
	trigger.trigger_count = 0
	trigger.last_triggered = 0.0

	if trigger_id in active_triggers:
		active_triggers.erase(trigger_id)
	if trigger_id in completed_triggers:
		completed_triggers.erase(trigger_id)


## 禁用触发器
func disable_trigger(trigger_id: String) -> void:
	var trigger = triggers.get(trigger_id)
	if trigger:
		trigger.state = TriggerState.DISABLED


## 启用触发器
func enable_trigger(trigger_id: String) -> void:
	var trigger = triggers.get(trigger_id)
	if trigger and trigger.state == TriggerState.DISABLED:
		trigger.state = TriggerState.INACTIVE


# ==================== 查询 ====================

## 获取触发器状态
func get_trigger_state(trigger_id: String) -> TriggerState:
	var trigger = triggers.get(trigger_id)
	if trigger:
		return trigger.state
	return TriggerState.INACTIVE


## 检查触发器是否已完成
func is_trigger_completed(trigger_id: String) -> bool:
	return trigger_id in completed_triggers


## 检查触发器是否激活
func is_trigger_active(trigger_id: String) -> bool:
	return trigger_id in active_triggers


# ==================== 存档支持 ====================

## 获取存档数据
func get_save_data() -> Dictionary:
	var trigger_states = {}
	for trigger_id in triggers:
		var trigger = triggers[trigger_id]
		trigger_states[trigger_id] = {
			"state": trigger.state,
			"trigger_count": trigger.trigger_count,
			"last_triggered": trigger.last_triggered
		}

	return {
		"trigger_states": trigger_states,
		"active_triggers": active_triggers,
		"completed_triggers": completed_triggers
	}


## 加载存档数据
func load_save_data(data: Dictionary) -> void:
	var trigger_states = data.get("trigger_states", {})
	for trigger_id in trigger_states:
		if triggers.has(trigger_id):
			var state_data = trigger_states[trigger_id]
			triggers[trigger_id].state = state_data.get("state", TriggerState.INACTIVE)
			triggers[trigger_id].trigger_count = state_data.get("trigger_count", 0)
			triggers[trigger_id].last_triggered = state_data.get("last_triggered", 0.0)

	active_triggers = data.get("active_triggers", [])
	completed_triggers = data.get("completed_triggers", [])