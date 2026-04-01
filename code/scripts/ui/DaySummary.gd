## DaySummary - 每日总结界面
## 显示一天结束时的总结信息
extends Control

# ==================== 信号 ====================
signal continue_pressed

# ==================== 节点引用 ====================
@onready var day_label: Label = $CenterContainer/PanelContainer/VBoxContainer/DayLabel
@onready var summary_label: RichTextLabel = $CenterContainer/PanelContainer/VBoxContainer/SummaryLabel
@onready var continue_button: Button = $CenterContainer/PanelContainer/VBoxContainer/ContinueButton


func _ready() -> void:
	if continue_button:
		continue_button.pressed.connect(_on_continue_pressed)
	hide()


func show_summary(day: int, interactions: int, trust_changes: Dictionary) -> void:
	"""显示每日总结"""
	if day_label:
		day_label.text = "第 %d 天结束" % day

	if summary_label:
		var text = ""
		text += "今日互动次数: %d\n\n" % interactions

		if trust_changes.size() > 0:
			text += "信任值变化:\n"
			for villager in trust_changes:
				var change = trust_changes[villager]
				if change != 0:
					var sign = "+" if change > 0 else ""
					text += "  %s: %s%d\n" % [villager, sign, change]
		else:
			text += "今天没有互动...\n"

		text += "\n剩余天数: %d" % (GameManager.MAX_DAYS - day)

		summary_label.text = text

	show()


func _on_continue_pressed() -> void:
	continue_pressed.emit()
	hide()