## DialogueBox - 对话框 UI 组件
extends Control

# ==================== 信号 ====================
signal dialogue_finished

# ==================== 引用 ====================
@onready var portrait: TextureRect = $MarginContainer/HBoxContainer/PortraitSection/Portrait
@onready var speaker_name: Label = $MarginContainer/HBoxContainer/ContentSection/SpeakerName
@onready var dialogue_text: RichTextLabel = $MarginContainer/HBoxContainer/ContentSection/DialogueText
@onready var choices_container: VBoxContainer = $MarginContainer/HBoxContainer/ContentSection/ChoicesScroll/ChoicesContainer
@onready var continue_hint: Label = $MarginContainer/HBoxContainer/ContentSection/ContinueHint

# ==================== 状态 ====================
var is_showing_choices: bool = false

## 角色表情映射
const CHARACTER_EXPRESSIONS = {
	"chenmo": {
		"default": "normal",
		"expressions": ["angry", "happy", "normal", "sad", "surprised"]
	},
	"yeya": {
		"default": "normal",
		"expressions": ["calm", "conflicted", "normal", "thinking"]
	},
	"jinling": {
		"default": "normal",
		"expressions": ["calculating", "normal", "smile", "surprised"]
	},
	"baizhi": {
		"default": "normal",
		"expressions": ["concerned", "gentle_smile", "normal", "sad"]
	},
	"john": {
		"default": "normal",
		"expressions": ["mysterious", "normal", "serious", "wise"]
	},
	"daxiong": {
		"default": "normal",
		"expressions": ["laugh", "listening", "normal", "serious"]
	},
	"leishu": {
		"default": "normal",
		"expressions": ["angry", "happy", "normal", "tired"]
	},
	"xiaoan": {
		"default": "normal",
		"expressions": ["curious", "excited", "happy", "normal", "sad"]
	},
	"ahu": {
		"default": "normal",
		"expressions": ["determined", "excited", "normal", "serious"]
	},
	"ying": {
		"default": "normal",
		"expressions": ["cold", "normal", "thinking", "warning"]
	}
}

## 角色名称映射
const CHARACTER_NAMES = {
	"player": "勇者",
	"narrator": "——",
	"chenmo": "陈默",
	"yeya": "夜鸦",
	"jinling": "金铃",
	"baizhi": "白芷",
	"john": "老约翰",
	"daxiong": "大熊",
	"leishu": "雷叔",
	"xiaoan": "小安",
	"ahu": "阿虎",
	"ying": "影"
}


func _ready() -> void:
	_connect_dialogue_manager()
	continue_hint.hide()
	portrait.hide()


func _input(event: InputEvent) -> void:
	if not visible:
		return

	if event.is_action_pressed("ui_accept") and not is_showing_choices:
		_on_continue_pressed()


func _connect_dialogue_manager() -> void:
	DialogueManager.dialogue_line_spoken.connect(_on_dialogue_line_spoken)
	DialogueManager.choice_presented.connect(_on_choices_presented)
	DialogueManager.choice_made.connect(_on_choice_made)
	DialogueManager.dialogue_ended.connect(_on_dialogue_ended)


# ==================== 公共方法 ==================

## 开始与指定村民的对话
func start_dialogue(villager_id: String) -> void:
	DialogueManager.start_dialogue(villager_id)


# ==================== 回调函数 ==================

func _on_dialogue_line_spoken(speaker: String, text: String) -> void:
	"""对话行显示"""
	show()  # 确保对话框可见
	_update_speaker_name(speaker)
	_update_portrait(speaker, text)
	dialogue_text.text = text
	continue_hint.show()
	_clear_choices()


func _on_choices_presented(choices: Array) -> void:
	is_showing_choices = true
	continue_hint.hide()
	_show_choices(choices)


func _on_choice_made(_choice_index: int, _choice_text: String) -> void:
	is_showing_choices = false
	_clear_choices()


func _on_dialogue_ended(_villager_id: String) -> void:
	hide()
	portrait.hide()
	dialogue_finished.emit()


func _on_continue_pressed() -> void:
	DialogueManager.continue_dialogue()


# ==================== 辅助方法 ==================

func _update_speaker_name(speaker: String) -> void:
	"""更新说话者名称"""
	speaker_name.text = CHARACTER_NAMES.get(speaker, speaker)


func _update_portrait(speaker: String, _text: String) -> void:
	"""更新角色立绘"""
	# 叙述者和玩家不显示立绘
	if speaker == "narrator" or speaker == "player":
		portrait.hide()
		return

	# 检查角色是否有立绘数据
	if not CHARACTER_EXPRESSIONS.has(speaker):
		portrait.hide()
		return

	var char_data = CHARACTER_EXPRESSIONS[speaker]
	var expression = char_data.default

	# 尝试加载立绘
	var portrait_path = "res://assets/sprites/characters/%s_%s.png" % [speaker, expression]

	if ResourceLoader.exists(portrait_path):
		portrait.texture = load(portrait_path)
		portrait.show()
	else:
		portrait.hide()


func _show_choices(choices: Array) -> void:
	_clear_choices()

	for i in range(choices.size()):
		var choice = choices[i]
		var button = Button.new()

		# 构建按钮文本，显示信任值变化
		var text = "%d. %s" % [i + 1, choice.text]
		if choice.has("trust_change"):
			var trust_change = choice.trust_change
			if trust_change > 0:
				text += " (+%d信任)" % trust_change
			elif trust_change < 0:
				text += " (%d信任)" % trust_change

		button.text = text
		button.pressed.connect(_on_choice_button_pressed.bind(i))
		choices_container.add_child(button)


func _clear_choices() -> void:
	for child in choices_container.get_children():
		child.queue_free()


func _on_choice_button_pressed(index: int) -> void:
	DialogueManager.select_choice(index)