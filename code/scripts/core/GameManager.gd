## Game Manager - 游戏全局管理器
## 负责游戏状态、存档、场景切换等核心功能
extends Node

# ==================== 信号 ====================
signal game_started
signal game_paused
signal game_resumed
signal day_changed(new_day: int)
signal action_points_changed(new_points: int)

# ==================== 游戏状态枚举 ====================
enum GameState {
	MENU,			# 主菜单
	PLAYING,		# 游戏进行中
	DIALOGUE,		# 对话中
	PAUSED,			# 暂停
	CUTSCENE,		# 剧情动画
	ENDING			# 结局
}

# ==================== 配置常量 ====================
const MAX_DAYS: int = 10			# 最大天数
const MAX_ACTION_POINTS: int = 4	# 每日最大行动点

# ==================== 游戏状态 ====================
var current_state: GameState = GameState.MENU
var current_day: int = 1
var action_points: int = MAX_ACTION_POINTS
var is_first_play: bool = true

# ==================== 玩家数据 ====================
var player_data: Dictionary = {
	"name": "勇者",
	"trust_levels": {},			# 村民信任值
	"known_secrets": [],		# 已知秘密
	"choices_made": [],			# 做出的选择
	"inventory": []				# 物品栏
}

# ==================== 引用 ====================
var current_scene: Node = null


func _ready() -> void:
	print("[GameManager] 游戏管理器初始化完成")


# ==================== 游戏流程控制 ====================

## 开始新游戏
func start_new_game() -> void:
	current_day = 1
	action_points = MAX_ACTION_POINTS
	player_data = {
		"name": "勇者",
		"trust_levels": {},
		"known_secrets": [],
		"choices_made": [],
		"inventory": []
	}
	current_state = GameState.PLAYING
	is_first_play = false

	# 初始化所有村民信任值
	_init_villager_trust()

	game_started.emit()
	print("[GameManager] 新游戏开始 - 第 %d 天" % current_day)


## 继续游戏（从存档）
func continue_game() -> bool:
	# TODO: 实现存档系统
	print("[GameManager] 继续游戏功能待实现")
	return false


## 暂停游戏
func pause_game() -> void:
	if current_state == GameState.PLAYING:
		current_state = GameState.PAUSED
		get_tree().paused = true
		game_paused.emit()
		print("[GameManager] 游戏暂停")


## 恢复游戏
func resume_game() -> void:
	if current_state == GameState.PAUSED:
		current_state = GameState.PLAYING
		get_tree().paused = false
		game_resumed.emit()
		print("[GameManager] 游戏恢复")


## 进入对话状态
func enter_dialogue() -> void:
	current_state = GameState.DIALOGUE


## 退出对话状态
func exit_dialogue() -> void:
	current_state = GameState.PLAYING


# ==================== 时间系统 ====================

## 进入下一天
func advance_day() -> void:
	if current_day >= MAX_DAYS:
		# 触发最终章节
		trigger_final_chapter()
		return

	current_day += 1
	action_points = MAX_ACTION_POINTS

	day_changed.emit(current_day)
	print("[GameManager] 进入第 %d 天" % current_day)


## 消耗行动点
func use_action_point(amount: int = 1) -> bool:
	if action_points >= amount:
		action_points -= amount
		action_points_changed.emit(action_points)
		print("[GameManager] 消耗 %d 行动点，剩余 %d" % [amount, action_points])

		# 检查是否需要进入下一天
		if action_points <= 0:
			advance_day()

		return true
	else:
		print("[GameManager] 行动点不足")
		return false


## 触发最终章节
func trigger_final_chapter() -> void:
	print("[GameManager] 第 10 天 - 魔王军抵达")
	current_state = GameState.ENDING
	# TODO: 触发最终章节剧情


# ==================== 村民信任系统 ====================

## 初始化村民信任值
func _init_villager_trust() -> void:
	var villagers = [
		"chenmo", "leishu", "jinling", "baizhi", "john",
		"daxiong", "ying", "xiaoan", "ahu", "yeya"
	]
	for villager in villagers:
		player_data.trust_levels[villager] = 0


## 获取村民信任值
func get_trust(villager_id: String) -> int:
	return player_data.trust_levels.get(villager_id, 0)


## 修改信任值
func modify_trust(villager_id: String, amount: int) -> void:
	var current = get_trust(villager_id)
	var new_value = clamp(current + amount, 0, 100)
	player_data.trust_levels[villager_id] = new_value
	print("[GameManager] %s 信任值: %d -> %d" % [villager_id, current, new_value])


# ==================== 存档系统 ====================

## 保存游戏
func save_game(slot: int = 0) -> bool:
	var save_data = {
		"version": "0.1.0",
		"timestamp": Time.get_unix_time_from_system(),
		"current_day": current_day,
		"action_points": action_points,
		"player_data": player_data.duplicate(true)
	}

	var file = FileAccess.open("user://save_%d.json" % slot, FileAccess.WRITE)
	if file:
		file.store_string(JSON.stringify(save_data, "  "))
		file.close()
		print("[GameManager] 游戏已保存到槽位 %d" % slot)
		return true

	print("[GameManager] 保存失败")
	return false


## 加载游戏
func load_game(slot: int = 0) -> bool:
	var file = FileAccess.open("user://save_%d.json" % slot, FileAccess.READ)
	if file:
		var json_string = file.get_as_text()
		file.close()

		var json = JSON.new()
		var parse_result = json.parse(json_string)

		if parse_result == OK:
			var save_data = json.data
			current_day = save_data.current_day
			action_points = save_data.action_points
			player_data = save_data.player_data
			print("[GameManager] 游戏已从槽位 %d 加载" % slot)
			return true

	print("[GameManager] 加载失败")
	return false


# ==================== 场景管理 ====================

## 切换场景
func change_scene(scene_path: String) -> void:
	get_tree().change_scene_to_file(scene_path)