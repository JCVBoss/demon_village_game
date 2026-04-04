## DialogueTreeParser - 对话树解析器
## 负责加载、解析和管理对话树数据
extends Node

# ==================== 信号 ====================
signal tree_loaded(villager_id: String)
signal node_entered(node_id: String)
signal choice_made(choice_index: int, choice_data: Dictionary)
signal tree_finished(villager_id: String)

# ==================== 数据结构 ====================
## 对话树数据
var trees: Dictionary = {}

## 当前对话状态
var current_tree_id: String = ""
var current_node_id: String = ""
var current_tree_data: Dictionary = {}
var available_nodes: Array = []

## 已访问节点（用于存档）
var visited_nodes: Dictionary = {}


# ==================== 初始化 ====================

func _ready() -> void:
	print("[DialogueTreeParser] 对话树解析器初始化完成")


# ==================== 加载对话树 ====================

func load_tree(villager_id: String) -> bool:
	"""加载指定村民的对话树"""
	var file_path = "res://resources/dialogues/dialogues.json"
	var file = FileAccess.open(file_path, FileAccess.READ)

	if not file:
		push_error("[DialogueTreeParser] 无法打开对话文件: %s" % file_path)
		return false

	var json_string = file.get_as_text()
	file.close()

	var json = JSON.new()
	if json.parse(json_string) != OK:
		push_error("[DialogueTreeParser] JSON 解析失败: %s" % json.get_error_message())
		return false

	var data = json.data
	if not data.has(villager_id):
		push_error("[DialogueTreeParser] 未找到村民对话: %s" % villager_id)
		return false

	# 缓存对话树
	trees[villager_id] = data[villager_id]

	tree_loaded.emit(villager_id)
	print("[DialogueTreeParser] 加载对话树: %s" % villager_id)
	return true


func load_all_trees() -> void:
	"""加载所有对话树"""
	var file_path = "res://resources/dialogues/dialogues.json"
	var file = FileAccess.open(file_path, FileAccess.READ)

	if not file:
		push_error("[DialogueTreeParser] 无法打开对话文件")
		return

	var json_string = file.get_as_text()
	file.close()

	var json = JSON.new()
	if json.parse(json_string) != OK:
		push_error("[DialogueTreeParser] JSON 解析失败")
		return

	trees = json.data
	print("[DialogueTreeParser] 加载了 %d 个对话树" % trees.size())


# ==================== 节点筛选 ====================

func get_available_nodes(villager_id: String) -> Array:
	"""获取当前可用的对话节点"""
	if not trees.has(villager_id):
		if not load_tree(villager_id):
			return []

	var tree_data = trees[villager_id]
	var dialogue_nodes = tree_data.get("dialogue_nodes", {})
	var current_day = GameManager.current_day
	var current_trust = TrustManager.get_trust(villager_id)

	available_nodes.clear()

	for node_id in dialogue_nodes:
		var node = dialogue_nodes[node_id]
		if _check_node_conditions(node, current_day, current_trust):
			available_nodes.append({
				"node_id": node_id,
				"node_data": node
			})

	return available_nodes


func _check_node_conditions(node: Dictionary, day: int, trust: int) -> bool:
	"""检查节点触发条件"""
	# 检查信任值要求
	var trust_required = node.get("trust_required", 0)
	var trust_max = node.get("trust_max", 100)

	if trust < trust_required or trust > trust_max:
		return false

	# 检查日期范围
	var day_min = node.get("day_min", 1)
	var day_max = node.get("day_max", 10)

	if day < day_min or day > day_max:
		return false

	# 检查事件标志要求
	var event_flags_required = node.get("event_flags_required", [])
	for flag in event_flags_required:
		if not EventManager.get_story_flag(flag):
			return false

	# 检查禁止的事件标志
	var event_flags_forbidden = node.get("event_flags_forbidden", [])
	for flag in event_flags_forbidden:
		if EventManager.get_story_flag(flag):
			return false

	return true


func get_best_node(villager_id: String) -> Dictionary:
	"""获取最合适的对话节点"""
	var nodes = get_available_nodes(villager_id)

	if nodes.is_empty():
		return {}

	# 优先级排序：
	# 1. 有最高信任值要求的节点
	# 2. 未访问过的节点
	# 3. 最新日期范围的节点

	var best_node = nodes[0]
	var best_score = -1

	for node_info in nodes:
		var score = 0
		var node_data = node_info.node_data

		# 信任值要求越高优先级越高
		score += node_data.get("trust_required", 0) * 10

		# 未访问过的节点优先
		var visited_key = "%s_%s" % [villager_id, node_info.node_id]
		if not visited_nodes.has(visited_key):
			score += 100

		# 日期范围越窄优先级越高
		var day_min = node_data.get("day_min", 1)
		var day_max = node_data.get("day_max", 10)
		var day_range = day_max - day_min
		score -= day_range

		if score > best_score:
			best_score = score
			best_node = node_info

	return best_node


# ==================== 对话流程 ====================

func start_dialogue(villager_id: String) -> bool:
	"""开始对话，选择最合适的节点"""
	var best_node = get_best_node(villager_id)

	if best_node.is_empty():
		push_error("[DialogueTreeParser] 没有可用的对话节点: %s" % villager_id)
		return false

	current_tree_id = villager_id
	current_node_id = best_node.node_id
	current_tree_data = trees[villager_id]

	# 标记节点为已访问
	var visited_key = "%s_%s" % [villager_id, current_node_id]
	visited_nodes[visited_key] = true

	node_entered.emit(current_node_id)
	print("[DialogueTreeParser] 开始对话: %s, 节点: %s" % [villager_id, current_node_id])
	return true


func start_dialogue_at_node(villager_id: String, node_id: String) -> bool:
	"""从指定节点开始对话"""
	if not trees.has(villager_id):
		if not load_tree(villager_id):
			return false

	var dialogue_nodes = trees[villager_id].get("dialogue_nodes", {})
	if not dialogue_nodes.has(node_id):
		push_error("[DialogueTreeParser] 节点不存在: %s" % node_id)
		return false

	current_tree_id = villager_id
	current_node_id = node_id
	current_tree_data = trees[villager_id]

	# 标记节点为已访问
	var visited_key = "%s_%s" % [villager_id, current_node_id]
	visited_nodes[visited_key] = true

	node_entered.emit(current_node_id)
	return true


func get_current_lines() -> Array:
	"""获取当前节点的对话行"""
	if current_node_id.is_empty():
		return []

	var dialogue_nodes = current_tree_data.get("dialogue_nodes", {})
	if not dialogue_nodes.has(current_node_id):
		return []

	return dialogue_nodes[current_node_id].get("lines", [])


func get_current_choices() -> Array:
	"""获取当前节点的选项"""
	if current_node_id.is_empty():
		return []

	var dialogue_nodes = current_tree_data.get("dialogue_nodes", {})
	if not dialogue_nodes.has(current_node_id):
		return []

	return dialogue_nodes[current_node_id].get("choices", [])


func select_choice(choice_index: int) -> bool:
	"""选择对话选项"""
	var choices = get_current_choices()

	if choice_index < 0 or choice_index >= choices.size():
		push_error("[DialogueTreeParser] 无效的选项索引: %d" % choice_index)
		return false

	var choice = choices[choice_index]

	# 应用信任值变化
	if choice.has("trust_change"):
		TrustManager.modify_trust(current_tree_id, choice.trust_change, "对话选择")

	# 设置事件标志
	if choice.has("event_flag"):
		EventManager.set_story_flag(choice.event_flag, true)

	choice_made.emit(choice_index, choice)

	# 跳转到下一个节点
	var next_node = choice.get("next_node")
	if next_node and not next_node.is_empty():
		return start_dialogue_at_node(current_tree_id, next_node)
	else:
		# 对话结束
		end_dialogue()
		return true


func end_dialogue() -> void:
	"""结束对话"""
	tree_finished.emit(current_tree_id)

	print("[DialogueTreeParser] 对话结束: %s" % current_tree_id)

	current_tree_id = ""
	current_node_id = ""
	current_tree_data = {}


# ==================== 查询方法 ====================

func get_tree_data(villager_id: String) -> Dictionary:
	"""获取对话树数据"""
	if not trees.has(villager_id):
		load_tree(villager_id)
	return trees.get(villager_id, {})


func get_trust_stage_name(villager_id: String, trust_value: int) -> String:
	"""根据信任值获取阶段名称"""
	var tree_data = get_tree_data(villager_id)
	var trust_stages = tree_data.get("trust_stages", {})

	for stage_name in trust_stages:
		var stage = trust_stages[stage_name]
		var min_val = stage.get("min", 0)
		var max_val = stage.get("max", 100)

		if trust_value >= min_val and trust_value <= max_val:
			return stage_name

	return "unknown"


func has_unvisited_nodes(villager_id: String) -> bool:
	"""检查是否有未访问的节点"""
	var nodes = get_available_nodes(villager_id)

	for node_info in nodes:
		var visited_key = "%s_%s" % [villager_id, node_info.node_id]
		if not visited_nodes.has(visited_key):
			return true

	return false


# ==================== 存档支持 ====================

func get_save_data() -> Dictionary:
	"""获取存档数据"""
	return {
		"visited_nodes": visited_nodes.duplicate(true),
		"current_tree_id": current_tree_id,
		"current_node_id": current_node_id
	}


func load_save_data(data: Dictionary) -> void:
	"""加载存档数据"""
	visited_nodes = data.get("visited_nodes", {})
	current_tree_id = data.get("current_tree_id", "")
	current_node_id = data.get("current_node_id", "")