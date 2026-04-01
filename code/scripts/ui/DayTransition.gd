## DayTransition - 天数过渡提示
## 显示天数变化的动画效果
extends CanvasLayer

# ==================== 节点引用 ====================
@onready var day_label: Label = $CenterContainer/PanelContainer/VBoxContainer/DayLabel
@onready var hint_label: Label = $CenterContainer/PanelContainer/VBoxContainer/HintLabel

# ==================== 配置 ====================
var display_duration: float = 2.0  # 显示持续时间
var fade_duration: float = 0.5    # 淡出时间


func _ready() -> void:
	# 连接信号
	GameManager.day_changed.connect(_on_day_changed)
	hide()


func _on_day_changed(new_day: int) -> void:
	"""天数变化时显示过渡"""
	show_transition(new_day)


func show_transition(day: int) -> void:
	"""显示天数过渡"""
	if day_label:
		day_label.text = "第 %d 天" % day

	if hint_label:
		if day == GameManager.MAX_DAYS:
			hint_label.text = "魔王军即将抵达..."
		else:
			hint_label.text = "新的一天开始了"

	show()

	# 等待显示时间后淡出
	await get_tree().create_timer(display_duration).timeout
	_fade_out()


func _fade_out() -> void:
	"""淡出动画"""
	var tween = create_tween()
	tween.tween_property(self, "modulate:a", 0.0, fade_duration)
	tween.tween_callback(hide)
	# 重置透明度
	modulate.a = 1.0