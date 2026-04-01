## Village - 村庄主场景
## 包含村庄背景、村民角色、交互系统
extends Node2D

# ==================== 信号 ====================
signal villager_selected(villager_id: String)

# ==================== 导出变量 ====================
@export var village_name: String = "暮色村"

# ==================== 节点引用 ====================
@onready var villagers_container: Node2D = $Villagers
@onready var player: CharacterBody2D = $Player
@onready var dialogue_box: PanelContainer = $UIRoot/DialogueBox
@onready var village_ui: CanvasLayer = $UIRoot
@onready var pause_menu: Control = $UIRoot/PauseMenu
@onready var save_load_ui: Control = $UIRoot/SaveLoadUI
@onready var menu_button: Button = $UIRoot/BottomBar/MenuButton
@onready var day_summary: Control = $UIRoot/DaySummary

# ==================== 状态 ====================
var is_paused: bool = false
var daily_interactions: int = 0
var daily_trust_changes: Dictionary = {}

# ==================== 配置 ====================
const VillagerScene = preload("res://scenes/characters/Villager.tscn")

# 村民位置配置 (ID -> 位置)
const VILLAGER_POSITIONS: Dictionary = {
	"chenmo": Vector2(200, 300),
	"leishu": Vector2(400, 250),
	"jinling": Vector2(600, 350),
	"baizhi": Vector2(300, 450),
	"john": Vector2(150, 200),
	"daxiong": Vector2(700, 200),
	"ying": Vector2(850, 400),
	"xiaoan": Vector2(500, 500),
	"ahu": Vector2(100, 400),
	"yeya": Vector2(800, 300)
}


func _ready() -> void:
	print("[Village] 进入村庄: %s" % village_name)

	# 连接游戏管理器信号
	_connect_game_manager_signals()

	# 连接对话管理器信号
	_connect_dialogue_signals()

	# 连接信任系统信号
	_connect_trust_signals()

	# 连接UI信号
	_connect_ui_signals()

	# 生成村民
	_spawn_villagers()

	# 更新 UI
	_update_ui()

	# 检查每日事件
	EventManager.check_events(GameManager.current_day)


# ==================== 信号连接 ====================

func _connect_game_manager_signals() -> void:
	"""连接游戏管理器信号"""
	GameManager.day_changed.connect(_on_day_changed)
	GameManager.action_points_changed.connect(_on_action_points_changed)


func _connect_trust_signals() -> void:
	"""连接信任系统信号"""
	TrustManager.trust_changed.connect(_on_trust_changed)
	TrustManager.secret_unlocked.connect(_on_secret_unlocked)

func _connect_dialogue_signals() -> void:
	"""连接对话管理器信号"""
	DialogueManager.dialogue_line_spoken.connect(_on_dialogue_line)
	DialogueManager.choice_presented.connect(_on_choices_presented)
	DialogueManager.dialogue_ended.connect(_on_dialogue_ended)


func _connect_ui_signals() -> void:
	"""连接UI信号"""
	# 菜单按钮
	if menu_button:
		menu_button.pressed.connect(_on_menu_button_pressed)

	# 暂停菜单
	if pause_menu:
		pause_menu.resume_pressed.connect(_on_resume_pressed)
		pause_menu.save_pressed.connect(_on_save_pressed)
		pause_menu.load_pressed.connect(_on_load_pressed)
		pause_menu.quit_to_menu_pressed.connect(_on_quit_to_menu_pressed)
		pause_menu.hide()

	# 存档界面
	if save_load_ui:
		save_load_ui.save_completed.connect(_on_save_completed)
		save_load_ui.load_completed.connect(_on_load_completed)
		save_load_ui.cancelled.connect(_on_save_load_cancelled)
		save_load_ui.hide()


# ==================== 村民生成 ====================

func _spawn_villagers() -> void:
	"""根据配置生成所有村民"""
	for villager_id in VILLAGER_POSITIONS:
		var villager = VillagerScene.instantiate()
		villager.villager_id = villager_id
		villager.position = VILLAGER_POSITIONS[villager_id]

		# 连接对话信号
		villager.dialogue_started.connect(_on_villager_dialogue_started)
		villager.dialogue_ended.connect(_on_villager_dialogue_ended)

		villagers_container.add_child(villager)

	print("[Village] 已生成 %d 位村民" % VILLAGER_POSITIONS.size())


# ==================== 对话系统回调 ====================

func _on_villager_dialogue_started(villager_id: String) -> void:
	"""村民对话开始"""
	print("[Village] 村民 %s 开始对话" % villager_id)
	villager_selected.emit(villager_id)

	# 显示对话框
	if dialogue_box:
		dialogue_box.show()

	# 记录今日互动次数
	daily_interactions += 1


func _on_villager_dialogue_ended() -> void:
	"""村民对话结束（备用）"""
	pass


func _consume_action_point() -> void:
	"""消耗行动点并检查是否进入下一天"""
	GameManager.action_points -= 1
	GameManager.action_points_changed.emit(GameManager.action_points)
	_update_ui()
	print("[Village] 消耗 1 行动点，剩余 %d" % GameManager.action_points)

	# 检查是否需要进入下一天
	if GameManager.action_points <= 0:
		GameManager.advance_day()


func _on_dialogue_line(_speaker: String, _text: String) -> void:
	"""对话行显示 - 由 DialogueBox 处理"""
	pass


func _on_choices_presented(_choices: Array) -> void:
	"""选项显示 - 由 DialogueBox 处理"""
	pass


func _on_dialogue_ended(_villager_id: String) -> void:
	"""对话结束回调 - DialogueManager 信号"""
	print("[Village] 对话结束 (DialogueManager)")
	# 隐藏对话框
	if dialogue_box:
		dialogue_box.hide()

	# 对话结束后消耗行动点
	_consume_action_point()


# ==================== UI 更新 ====================

func _update_ui() -> void:
	"""更新 UI 显示"""
	# 更新天数和行动点显示
	var day_label = get_node_or_null("UIRoot/TopBar/HBoxContainer/DayLabel")
	var action_label = get_node_or_null("UIRoot/TopBar/HBoxContainer/ActionPointsLabel")
	var village_label = get_node_or_null("UIRoot/TopBar/HBoxContainer/VillageNameLabel")

	if day_label:
		day_label.text = "第 %d 天" % GameManager.current_day

	if action_label:
		action_label.text = "行动点: %d/%d" % [GameManager.action_points, GameManager.MAX_ACTION_POINTS]

	if village_label:
		village_label.text = village_name


# ==================== 游戏流程 ====================

func _on_day_changed(new_day: int) -> void:
	"""天数变化回调"""
	print("[Village] 进入第 %d 天" % new_day)

	# 显示每日总结
	_show_day_summary(new_day - 1)

	# 检查新一天的事件
	EventManager.check_events(new_day)


func _show_day_summary(completed_day: int) -> void:
	"""显示每日总结"""
	if day_summary:
		day_summary.show_summary(completed_day, daily_interactions, daily_trust_changes)
		# 等待玩家点击继续
		await day_summary.continue_pressed

	# 重置每日统计
	_reset_daily_stats()


func _reset_daily_stats() -> void:
	"""重置每日统计"""
	daily_interactions = 0
	daily_trust_changes.clear()


func _on_action_points_changed(new_points: int) -> void:
	"""行动点变化回调"""
	_update_ui()
	if new_points <= 0:
		print("[Village] 行动点耗尽，即将进入下一天")


func _on_trust_changed(villager_id: String, _old_value: int, new_value: int) -> void:
	"""信任值变化回调"""
	print("[Village] %s 信任值更新为 %d" % [villager_id, new_value])

	# 记录今日信任变化
	if not daily_trust_changes.has(villager_id):
		daily_trust_changes[villager_id] = 0
	# 计算实际变化量
	var change = new_value - _old_value
	daily_trust_changes[villager_id] += change

	# 更新对应村民的信任值显示
	_update_villager_trust_display(villager_id, new_value)


func _on_secret_unlocked(villager_id: String, secret_id: String) -> void:
	"""秘密解锁回调"""
	print("[Village] 解锁 %s 的秘密: %s" % [villager_id, secret_id])
	# TODO: 显示秘密解锁提示


func _update_villager_trust_display(villager_id: String, trust_value: int) -> void:
	"""更新村民信任值显示"""
	if villagers_container:
		for child in villagers_container.get_children():
			if child.villager_id == villager_id:
				child.set_trust_value(trust_value)


func advance_to_next_day() -> void:
	"""进入下一天（已由 GameManager 自动处理）"""
	_update_ui()
	EventManager.check_events(GameManager.current_day)
	print("[Village] 进入第 %d 天" % GameManager.current_day)


# ==================== 输入处理 ====================

func _input(event: InputEvent) -> void:
	"""处理输入"""
	# ESC 键打开菜单
	if event.is_action_pressed("ui_cancel"):
		_on_menu_button_pressed()


func _on_menu_button_pressed() -> void:
	"""菜单按钮按下"""
	print("[Village] 打开菜单")
	_pause_game()
	if pause_menu:
		pause_menu.show_menu()


# ==================== 暂停菜单回调 ====================

func _pause_game() -> void:
	"""暂停游戏"""
	is_paused = true
	get_tree().paused = true


func _resume_game() -> void:
	"""恢复游戏"""
	is_paused = false
	get_tree().paused = false


func _on_resume_pressed() -> void:
	"""继续游戏"""
	print("[Village] 继续游戏")
	_resume_game()
	if pause_menu:
		pause_menu.hide_menu()


func _on_save_pressed() -> void:
	"""打开保存界面"""
	print("[Village] 打开保存界面")
	if pause_menu:
		pause_menu.hide_menu()
	if save_load_ui:
		save_load_ui.show_save_mode()


func _on_load_pressed() -> void:
	"""打开读取界面"""
	print("[Village] 打开读取界面")
	if pause_menu:
		pause_menu.hide_menu()
	if save_load_ui:
		save_load_ui.show_load_mode()


func _on_quit_to_menu_pressed() -> void:
	"""返回主菜单"""
	print("[Village] 返回主菜单")
	_resume_game()
	var result = get_tree().change_scene_to_file("res://scenes/Main.tscn")
	if result != OK:
		push_error("[Village] 无法返回主菜单")


# ==================== 存档界面回调 ====================

func _on_save_completed(_slot_index: int) -> void:
	"""存档完成"""
	print("[Village] 存档完成")
	if save_load_ui:
		save_load_ui.hide()
	if pause_menu:
		pause_menu.show_menu()


func _on_load_completed(_slot_index: int) -> void:
	"""读档完成"""
	print("[Village] 读档完成")
	_resume_game()
	if save_load_ui:
		save_load_ui.hide()
	_update_ui()
	# 重新生成村民位置
	_spawn_villagers_after_load()


func _on_save_load_cancelled() -> void:
	"""取消存档操作"""
	print("[Village] 取消存档操作")
	if save_load_ui:
		save_load_ui.hide()
	if pause_menu:
		pause_menu.show_menu()


func _spawn_villagers_after_load() -> void:
	"""加载后刷新村民"""
	# 清除现有村民
	if villagers_container:
		for child in villagers_container.get_children():
			child.queue_free()
	# 重新生成
	_spawn_villagers()