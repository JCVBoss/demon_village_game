## Dialogue Manager - 对话管理器
## 负责处理玩家与村民的对话系统
## 使用 DialogueTreeParser 进行对话树解析
extends Node

# ==================== 信号 ====================
signal dialogue_started(villager_id: String)
signal dialogue_ended(villager_id: String)
signal dialogue_line_spoken(speaker: String, text: String)
signal choice_presented(choices: Array)
signal choice_made(choice_index: int, choice_text: String)

# ==================== 对话状态 ====================
var is_in_dialogue: bool = false
var current_villager_id: String = ""
var current_dialogue_data: Dictionary = {}
var current_line_index: int = 0

# ==================== 对话数据 ====================
# 存储所有对话脚本数据（保留用于向后兼容）
var dialogue_scripts: Dictionary = {}

# 当前对话节点
var current_node_id: String = ""

# 使用解析器模式
var use_parser: bool = true


func _ready() -> void:
	print("[DialogueManager] 对话管理器初始化完成")
	_load_dialogue_scripts()


# ==================== 对话数据加载 ====================

## 加载所有对话脚本
func _load_dialogue_scripts() -> void:
	"""从 JSON 文件加载对话数据"""
	var file = FileAccess.open("res://resources/dialogues/dialogues.json", FileAccess.READ)
	if file:
		var json_string = file.get_as_text()
		file.close()

		var json = JSON.new()
		if json.parse(json_string) == OK:
			dialogue_scripts = json.data
			print("[DialogueManager] 加载了 %d 个村民的对话数据" % dialogue_scripts.size())
		else:
			print("[DialogueManager] 对话数据解析失败: %s" % json.get_error_message())
	else:
		print("[DialogueManager] 无法打开对话数据文件")


## 获取村民的信任等级
func _get_trust_stage(villager_id: String, trust_value: int) -> String:
	"""根据信任值返回信任阶段名称"""
	if dialogue_scripts.has(villager_id):
		var stages = dialogue_scripts[villager_id].get("trust_stages", {})
		for stage_name in stages:
			var stage = stages[stage_name]
			if trust_value >= stage.min and trust_value <= stage.max:
				return stage_name
	return "wary"


# ==================== 对话流程控制 ====================

## 开始对话（主入口）
func start_dialogue(villager_id: String, trust_value: int = 0, node_id: String = "") -> void:
	if is_in_dialogue:
		print("[DialogueManager] 已在对话中，无法开始新对话")
		return

	# 使用新的解析器模式
	if use_parser and DialogueTreeParser:
		_start_with_parser(villager_id, trust_value, node_id)
	else:
		_start_with_legacy(villager_id, trust_value, node_id)


## 使用解析器开始对话
func _start_with_parser(villager_id: String, _trust_value: int, node_id: String) -> void:
	"""使用 DialogueTreeParser 开始对话"""
	var success: bool

	if node_id.is_empty():
		# 自动选择最合适的节点
		success = DialogueTreeParser.start_dialogue(villager_id)
	else:
		# 从指定节点开始
		success = DialogueTreeParser.start_dialogue_at_node(villager_id, node_id)

	if not success:
		print("[DialogueManager] 解析器无法开始对话")
		return

	is_in_dialogue = true
	current_villager_id = villager_id
	current_node_id = DialogueTreeParser.current_node_id
	current_dialogue_data = DialogueTreeParser.current_tree_data.get("dialogue_nodes", {}).get(current_node_id, {})
	current_line_index = 0

	GameManager.enter_dialogue()
	dialogue_started.emit(villager_id)

	print("[DialogueManager] 开始与 %s 对话，节点: %s (解析器模式)" % [villager_id, current_node_id])
	_play_dialogue()


## 使用旧模式开始对话（向后兼容）
func _start_with_legacy(villager_id: String, trust_value: int, node_id: String) -> void:
	"""使用旧模式开始对话"""
	if node_id.is_empty():
		node_id = "initial"

	if not dialogue_scripts.has(villager_id):
		print("[DialogueManager] 未找到村民 %s 的对话数据" % villager_id)
		return

	var villager_data = dialogue_scripts[villager_id]
	var dialogue_nodes = villager_data.get("dialogue_nodes", {})

	if not dialogue_nodes.has(node_id):
		print("[DialogueManager] 未找到对话节点: %s" % node_id)
		return

	# 检查信任值要求
	var node = dialogue_nodes[node_id]
	var trust_required = node.get("trust_required", 0)
	if trust_value < trust_required:
		print("[DialogueManager] 信任值不足，需要 %d，当前 %d" % [trust_required, trust_value])
		# 找到合适的对话节点
		node_id = _find_suitable_node(villager_id, trust_value)
		if node_id.is_empty():
			print("[DialogueManager] 未找到合适的对话节点")
			return
		node = dialogue_nodes[node_id]

	is_in_dialogue = true
	current_villager_id = villager_id
	current_node_id = node_id
	current_dialogue_data = node
	current_line_index = 0

	GameManager.enter_dialogue()
	dialogue_started.emit(villager_id)

	print("[DialogueManager] 开始与 %s 对话，节点: %s" % [villager_id, node_id])
	_play_dialogue()


## 查找适合当前信任值的对话节点
func _find_suitable_node(villager_id: String, trust_value: int) -> String:
	"""根据信任值找到最适合的对话节点"""
	if not dialogue_scripts.has(villager_id):
		return ""

	var dialogue_nodes = dialogue_scripts[villager_id].get("dialogue_nodes", {})
	var best_node = ""
	var best_trust = -1

	for node_id in dialogue_nodes:
		var node = dialogue_nodes[node_id]
		var trust_required = node.get("trust_required", 0)
		if trust_value >= trust_required and trust_required > best_trust:
			best_trust = trust_required
			best_node = node_id

	return best_node


## 播放对话内容
func _play_dialogue() -> void:
	var lines: Array

	if use_parser and DialogueTreeParser and DialogueTreeParser.current_node_id == current_node_id:
		lines = DialogueTreeParser.get_current_lines()
	else:
		lines = current_dialogue_data.get("lines", [])

	if current_line_index < lines.size():
		var line = lines[current_line_index]
		dialogue_line_spoken.emit(line.speaker, line.text)
		current_line_index += 1
	else:
		# 对话行结束，显示选项或结束对话
		var choices = _get_current_choices()
		if choices.size() > 0:
			choice_presented.emit(choices)
		else:
			end_dialogue()


## 获取当前选项
func _get_current_choices() -> Array:
	if use_parser and DialogueTreeParser and DialogueTreeParser.current_node_id == current_node_id:
		return DialogueTreeParser.get_current_choices()
	else:
		return current_dialogue_data.get("choices", [])


## 继续对话（玩家点击继续）
func continue_dialogue() -> void:
	if not is_in_dialogue:
		return

	_play_dialogue()


## 选择对话选项
func select_choice(choice_index: int) -> void:
	var choices = _get_current_choices()
	if choice_index < 0 or choice_index >= choices.size():
		return

	var choice = choices[choice_index]
	choice_made.emit(choice_index, choice.text)

	# 使用解析器模式
	if use_parser and DialogueTreeParser and DialogueTreeParser.current_node_id == current_node_id:
		DialogueTreeParser.select_choice(choice_index)

		# 检查对话是否继续
		if DialogueTreeParser.is_in_dialogue or not DialogueTreeParser.current_node_id.is_empty():
			current_node_id = DialogueTreeParser.current_node_id
			current_dialogue_data = DialogueTreeParser.current_tree_data.get("dialogue_nodes", {}).get(current_node_id, {})
			current_line_index = 0
			_play_dialogue()
			return

		# 对话结束
		end_dialogue()
		return

	# 旧模式
	# 应用信任值变化
	if choice.has("trust_change"):
		TrustManager.modify_trust(current_villager_id, choice.trust_change)

	# 跳转到下一个对话节点
	var next_node = choice.get("next_node")
	if next_node and not next_node.is_empty():
		var dialogue_nodes = dialogue_scripts[current_villager_id].get("dialogue_nodes", {})
		if dialogue_nodes.has(next_node):
			current_node_id = next_node
			current_dialogue_data = dialogue_nodes[next_node]
			current_line_index = 0
			print("[DialogueManager] 跳转到对话节点: %s" % next_node)
			_play_dialogue()
			return

	# 没有后续对话，结束对话
	end_dialogue()


## 结束对话
func end_dialogue() -> void:
	var villager_id = current_villager_id

	is_in_dialogue = false
	current_villager_id = ""
	current_dialogue_data = {}
	current_line_index = 0

	# 同步解析器状态
	if DialogueTreeParser:
		DialogueTreeParser.end_dialogue()

	GameManager.exit_dialogue()
	dialogue_ended.emit(villager_id)

	print("[DialogueManager] 与 %s 的对话结束" % villager_id)


# ==================== 对话数据查询 ====================

## 获取村民对话选项
func get_available_dialogues(villager_id: String) -> Array:
	if use_parser and DialogueTreeParser:
		var nodes = DialogueTreeParser.get_available_nodes(villager_id)
		var result = []
		for node_info in nodes:
			result.append(node_info.node_id)
		return result

	if dialogue_scripts.has(villager_id):
		return dialogue_scripts[villager_id].keys()
	return []


## 检查对话是否可用
func is_dialogue_available(villager_id: String, dialogue_key: String) -> bool:
	return dialogue_scripts.has(villager_id) and dialogue_scripts[villager_id].has(dialogue_key)


## 检查是否有未访问的对话节点
func has_new_dialogue(villager_id: String) -> bool:
	"""检查是否有新的对话可用"""
	if use_parser and DialogueTreeParser:
		return DialogueTreeParser.has_unvisited_nodes(villager_id)
	return true