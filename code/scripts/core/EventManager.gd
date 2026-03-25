## Event Manager - 事件管理器
## 负责管理游戏事件、触发条件和情报传播
extends Node

# ==================== 信号 ====================
signal event_triggered(event_id: String, event_data: Dictionary)
signal rumor_spread(rumor_id: String, affected_villagers: Array)
signal story_flag_set(flag_name: String, value: bool)

# ==================== 事件类型 ====================
enum EventType {
	DIALOGUE,		# 对话事件
	STORY,			# 剧情事件
	TIMED,			# 定时事件
	RANDOM,			# 随机事件
	CHOICE			# 选择事件
}

# ==================== 事件数据 ====================
var events: Dictionary = {}
var active_events: Array = []
var completed_events: Array = []
var story_flags: Dictionary = {}

# ==================== 情报系统 ====================
var rumors: Dictionary = {}
var villager_knowledge: Dictionary = {}  # 每个村民知道的信息


func _ready() -> void:
	print("[EventManager] 事件管理器初始化完成")
	_load_events()
	_init_villager_knowledge()


# ==================== 初始化 ====================

## 加载事件数据
func _load_events() -> void:
	# TODO: 从 JSON 文件加载事件数据
	# 目前使用测试数据
	events = {
		"chenmo_secret_discovered": {
			"id": "chenmo_secret_discovered",
			"type": EventType.STORY,
			"trigger_day": 3,
			"trigger_conditions": {
				"trust_chenmo": 40
			},
			"data": {
				"description": "发现陈默是逃兵的秘密",
				"villagers_involved": ["chenmo", "player"]
			}
		},
		"yeya_order_received": {
			"id": "yeya_order_received",
			"type": EventType.STORY,
			"trigger_day": 5,
			"trigger_conditions": {},
			"data": {
				"description": "夜鸦收到魔王军的进攻指令",
				"villagers_involved": ["yeya"]
			}
		},
		"xiaoan_revelation": {
			"id": "xiaoan_revelation",
			"type": EventType.STORY,
			"trigger_day": 7,
			"trigger_conditions": {
				"flag_chenmo_secret_known": true
			},
			"data": {
				"description": "小安身世揭露",
				"villagers_involved": ["xiaoan", "chenmo", "player"]
			}
		},
		"final_day": {
			"id": "final_day",
			"type": EventType.STORY,
			"trigger_day": 10,
			"trigger_conditions": {},
			"data": {
				"description": "魔王军抵达暮色村",
				"villagers_involved": ["all"]
			}
		}
	}


## 初始化村民知识库
func _init_villager_knowledge() -> void:
	var villagers = [
		"chenmo", "leishu", "jinling", "baizhi", "john",
		"daxiong", "ying", "xiaoan", "ahu", "yeya"
	]

	for villager in villagers:
		villager_knowledge[villager] = {
			"known_rumors": [],
			"known_secrets": [],
			"knowledge_level": {}  # 对其他村民的了解程度
		}


# ==================== 事件触发 ====================

## 检查并触发事件
func check_events(_current_day: int) -> void:
	for event_id in events:
		var event = events[event_id]

		# 检查是否已完成
		if event_id in completed_events:
			continue

		# 检查触发条件
		if _check_trigger_conditions(event):
			trigger_event(event_id)


## 检查触发条件
func _check_trigger_conditions(event: Dictionary) -> bool:
	var conditions = event.get("trigger_conditions", {})

	# 检查触发天数
	if event.has("trigger_day"):
		if GameManager.current_day < event.trigger_day:
			return false

	# 检查信任值条件
	for condition_key in conditions:
		if condition_key.begins_with("trust_"):
			var villager_id = condition_key.replace("trust_", "")
			var required_trust = conditions[condition_key]
			if TrustManager.get_trust(villager_id) < required_trust:
				return false

		# 检查故事标志
		if condition_key.begins_with("flag_"):
			var flag_name = condition_key.replace("flag_", "")
			if not story_flags.get(flag_name, false):
				return false

	return true


## 触发事件
func trigger_event(event_id: String) -> void:
	if not events.has(event_id):
		print("[EventManager] 未找到事件: %s" % event_id)
		return

	var event = events[event_id]

	print("[EventManager] 触发事件: %s" % event_id)
	active_events.append(event_id)
	event_triggered.emit(event_id, event.data)


## 完成事件
func complete_event(event_id: String) -> void:
	if event_id in active_events:
		active_events.erase(event_id)
		completed_events.append(event_id)
		print("[EventManager] 完成事件: %s" % event_id)


# ==================== 故事标志 ====================

## 设置故事标志
func set_story_flag(flag_name: String, value: bool = true) -> void:
	story_flags[flag_name] = value
	story_flag_set.emit(flag_name, value)
	print("[EventManager] 设置故事标志: %s = %s" % [flag_name, value])


## 获取故事标志
func get_story_flag(flag_name: String) -> bool:
	return story_flags.get(flag_name, false)


# ==================== 情报传播系统 ====================

## 创建情报
func create_rumor(rumor_id: String, content: String, source: String, spread_type: String = "normal") -> void:
	rumors[rumor_id] = {
		"id": rumor_id,
		"content": content,
		"source": source,
		"spread_type": spread_type,  # "fast", "normal", "slow", "secret"
		"affected_villagers": [],
		"created_day": GameManager.current_day
	}
	print("[EventManager] 创建情报: %s" % rumor_id)


## 传播情报
func spread_rumor(rumor_id: String) -> void:
	if not rumors.has(rumor_id):
		return

	var rumor = rumors[rumor_id]
	var affected = []

	# 根据传播类型决定传播范围
	match rumor.spread_type:
		"fast":
			# 快速传播，大部分村民知道
			affected = villager_knowledge.keys()
		"normal":
			# 正常传播，相关村民知道
			affected = _get_connected_villagers(rumor.source)
		"slow":
			# 慢速传播，少数村民知道
			affected = _get_close_villagers(rumor.source)
		"secret":
			# 秘密，不自动传播
			affected = []

	# 更新村民知识
	for villager in affected:
		if not rumor_id in villager_knowledge[villager].known_rumors:
			villager_knowledge[villager].known_rumors.append(rumor_id)
			rumor.affected_villagers.append(villager)

	if affected.size() > 0:
		rumor_spread.emit(rumor_id, affected)
		print("[EventManager] 情报 %s 传播给了: %s" % [rumor_id, affected])


## 获取关联村民
func _get_connected_villagers(source: String) -> Array:
	# TODO: 基于关系网返回关联村民
	# 简化版本：返回随机3-5个村民
	var all_villagers = villager_knowledge.keys()
	all_villagers.erase(source)
	return all_villagers.slice(0, min(4, all_villagers.size()))


## 获取亲密村民
func _get_close_villagers(source: String) -> Array:
	# TODO: 基于关系网返回亲密村民
	# 简化版本：返回随机1-2个村民
	var all_villagers = villager_knowledge.keys()
	all_villagers.erase(source)
	return all_villagers.slice(0, min(2, all_villagers.size()))


## 检查村民是否知道情报
func villager_knows_rumor(villager_id: String, rumor_id: String) -> bool:
	if villager_knowledge.has(villager_id):
		return rumor_id in villager_knowledge[villager_id].known_rumors
	return false


# ==================== 存档支持 ====================

## 获取存档数据
func get_save_data() -> Dictionary:
	return {
		"active_events": active_events,
		"completed_events": completed_events,
		"story_flags": story_flags,
		"rumors": rumors,
		"villager_knowledge": villager_knowledge
	}


## 加载存档数据
func load_save_data(data: Dictionary) -> void:
	active_events = data.get("active_events", [])
	completed_events = data.get("completed_events", [])
	story_flags = data.get("story_flags", {})
	rumors = data.get("rumors", {})
	villager_knowledge = data.get("villager_knowledge", {})