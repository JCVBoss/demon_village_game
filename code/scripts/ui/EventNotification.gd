## EventNotification - 事件通知 UI
## 显示剧情事件触发的通知
extends CanvasLayer

# ==================== 节点引用 ====================
@onready var notification_panel: PanelContainer = $MarginContainer/PanelContainer
@onready var title_label: Label = $MarginContainer/PanelContainer/VBoxContainer/TitleLabel
@onready var content_label: Label = $MarginContainer/PanelContainer/VBoxContainer/ContentLabel

# ==================== 配置 ====================
var display_duration: float = 3.0
var fade_duration: float = 0.5


func _ready() -> void:
	# 连接事件管理器信号
	EventManager.event_triggered.connect(_on_event_triggered)
	hide()


func _on_event_triggered(event_id: String, event_data: Dictionary) -> void:
	"""事件触发时显示通知"""
	show_notification(event_id, event_data)


func show_notification(event_id: String, event_data: Dictionary) -> void:
	"""显示事件通知"""
	var title = _get_event_title(event_id)
	var content = event_data.get("description", "有新的事情发生了...")

	if title_label:
		title_label.text = title
	if content_label:
		content_label.text = content

	show()

	# 淡入动画
	modulate.a = 0.0
	var tween = create_tween()
	tween.tween_property(self, "modulate:a", 1.0, fade_duration)

	# 等待后淡出
	await get_tree().create_timer(display_duration).timeout
	_fade_out()


func _fade_out() -> void:
	"""淡出动画"""
	var tween = create_tween()
	tween.tween_property(self, "modulate:a", 0.0, fade_duration)
	tween.tween_callback(hide)
	modulate.a = 1.0


func _get_event_title(event_id: String) -> String:
	"""获取事件标题"""
	match event_id:
		"chenmo_secret_discovered":
			return "【剧情触发】"
		"yeya_order_received":
			return "【紧急情报】"
		"xiaoan_revelation":
			return "【真相揭露】"
		"final_day":
			return "【最终日】"
		_:
			return "【事件】"