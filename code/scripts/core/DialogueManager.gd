## Dialogue Manager - 对话管理器
## 负责处理玩家与村民的对话系统
class_name DialogueManager
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
# 存储所有对话脚本数据
var dialogue_scripts: Dictionary = {}


func _ready() -> void:
	print("[DialogueManager] 对话管理器初始化完成")
	_load_dialogue_scripts()


# ==================== 对话数据加载 ====================

## 加载所有对话脚本
func _load_dialogue_scripts() -> void:
	# TODO: 从 JSON 文件加载对话数据
	# 目前使用测试数据
	dialogue_scripts = {
		"chenmo": {
			"initial": {
				"lines": [
					{"speaker": "chenmo", "text": "......你是新来的？"},
					{"speaker": "chenmo", "text": "我不认识你，也不想认识。"},
					{"speaker": "player", "text": "（这个人看起来很警惕）"}
				],
				"choices": [
					{"text": "友好地打招呼", "trust_change": 5, "next": "friendly_greeting"},
					{"text": "直接询问村子情况", "trust_change": 0, "next": "ask_about_village"},
					{"text": "保持沉默离开", "trust_change": -2, "next": "leave_silently"}
				]
			},
			"friendly_greeting": {
				"lines": [
					{"speaker": "player", "text": "你好，我叫勇者。听说村子需要帮忙？"},
					{"speaker": "chenmo", "text": "......帮忙？"},
					{"speaker": "chenmo", "text": "（沉默片刻）如果你真的想帮忙，去找大熊吧。酒馆在东边。"}
				],
				"choices": []
			},
			"ask_about_village": {
				"lines": [
					{"speaker": "player", "text": "请问这个村子是什么情况？"},
					{"speaker": "chenmo", "text": "......"},
					{"speaker": "chenmo", "text": "自己去酒馆问。"}
				],
				"choices": []
			},
			"leave_silently": {
				"lines": [
					{"speaker": "player", "text": "......"},
					{"speaker": "chenmo", "text": "（他看着你离开，没有说话）"}
				],
				"choices": []
			}
		}
	}


# ==================== 对话流程控制 ====================

## 开始对话
func start_dialogue(villager_id: String, dialogue_key: String = "initial") -> void:
	if is_in_dialogue:
		print("[DialogueManager] 已在对话中，无法开始新对话")
		return

	if not dialogue_scripts.has(villager_id):
		print("[DialogueManager] 未找到村民 %s 的对话数据" % villager_id)
		return

	var villager_dialogues = dialogue_scripts[villager_id]
	if not villager_dialogues.has(dialogue_key):
		print("[DialogueManager] 未找到对话键: %s" % dialogue_key)
		return

	is_in_dialogue = true
	current_villager_id = villager_id
	current_dialogue_data = villager_dialogues[dialogue_key]
	current_line_index = 0

	GameManager.enter_dialogue()
	dialogue_started.emit(villager_id)

	_play_dialogue()


## 播放对话内容
func _play_dialogue() -> void:
	var lines = current_dialogue_data.get("lines", [])

	if current_line_index < lines.size():
		var line = lines[current_line_index]
		dialogue_line_spoken.emit(line.speaker, line.text)
		current_line_index += 1
	else:
		# 对话行结束，显示选项或结束对话
		var choices = current_dialogue_data.get("choices", [])
		if choices.size() > 0:
			choice_presented.emit(choices)
		else:
			end_dialogue()


## 继续对话（玩家点击继续）
func continue_dialogue() -> void:
	if not is_in_dialogue:
		return

	_play_dialogue()


## 选择对话选项
func select_choice(choice_index: int) -> void:
	var choices = current_dialogue_data.get("choices", [])
	if choice_index < 0 or choice_index >= choices.size():
		return

	var choice = choices[choice_index]
	choice_made.emit(choice_index, choice.text)

	# 应用信任值变化
	if choice.has("trust_change"):
		TrustManager.modify_trust(current_villager_id, choice.trust_change)

	# 跳转到下一个对话节点
	if choice.has("next"):
		var next_key = choice.next
		if dialogue_scripts[current_villager_id].has(next_key):
			current_dialogue_data = dialogue_scripts[current_villager_id][next_key]
			current_line_index = 0
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

	GameManager.exit_dialogue()
	dialogue_ended.emit(villager_id)

	print("[DialogueManager] 与 %s 的对话结束" % villager_id)


# ==================== 对话数据查询 ====================

## 获取村民对话选项
func get_available_dialogues(villager_id: String) -> Array:
	# TODO: 根据信任值、游戏进度返回可用对话
	if dialogue_scripts.has(villager_id):
		return dialogue_scripts[villager_id].keys()
	return []


## 检查对话是否可用
func is_dialogue_available(villager_id: String, dialogue_key: String) -> bool:
	# TODO: 检查前置条件
	return dialogue_scripts.has(villager_id) and dialogue_scripts[villager_id].has(dialogue_key)