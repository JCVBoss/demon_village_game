## DialogueBox - 对话框 UI 组件
extends PanelContainer

# ==================== 信号 ====================
signal dialogue_finished

# ==================== 引用 ====================
@onready var speaker_name: Label = $VBoxContainer/SpeakerName
@onready var dialogue_text: RichTextLabel = $VBoxContainer/DialogueText
@onready var choices_container: VBoxContainer = $VBoxContainer/ChoicesContainer
@onready var continue_hint: Label = $VBoxContainer/ContinueHint

# ==================== 状态 ====================
var is_showing_choices: bool = false


func _ready() -> void:
	_connect_dialogue_manager()
	continue_hint.hide()


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


# ==================== 公共方法 ====================

## 开始与指定村民的对话
func start_dialogue(villager_id: String) -> void:
	DialogueManager.start_dialogue(villager_id)


# ==================== 回调函数 ====================

func _on_dialogue_line_spoken(speaker: String, text: String) -> void:
	"""对话行显示"""
	show()  # 确保对话框可见
	_update_speaker_name(speaker)
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
	dialogue_finished.emit()


func _on_continue_pressed() -> void:
	DialogueManager.continue_dialogue()


# ==================== 辅助方法 ====================

func _update_speaker_name(speaker: String) -> void:
	"""更新说话者名称"""
	match speaker:
		"player":
			speaker_name.text = "勇者"
		"narrator":
			speaker_name.text = "——"
		"chenmo":
			speaker_name.text = "陈默"
		"yeya":
			speaker_name.text = "夜鸦"
		"jinling":
			speaker_name.text = "金铃"
		"baizhi":
			speaker_name.text = "白芷"
		"john":
			speaker_name.text = "老约翰"
		"daxiong":
			speaker_name.text = "大熊"
		"leishu":
			speaker_name.text = "雷叔"
		"xiaoan":
			speaker_name.text = "小安"
		"ahu":
			speaker_name.text = "阿虎"
		"ying":
			speaker_name.text = "影"
		_:
			speaker_name.text = speaker


func _show_choices(choices: Array) -> void:
	_clear_choices()

	for i in range(choices.size()):
		var choice = choices[i]
		var button = Button.new()
		button.text = "%d. %s" % [i + 1, choice.text]
		button.pressed.connect(_on_choice_button_pressed.bind(i))
		choices_container.add_child(button)


func _clear_choices() -> void:
	for child in choices_container.get_children():
		child.queue_free()


func _on_choice_button_pressed(index: int) -> void:
	DialogueManager.select_choice(index)