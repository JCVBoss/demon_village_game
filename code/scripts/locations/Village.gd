## Village - 村庄主场景
## 星露谷物语风格地图：Y-sorting 渲染，建筑使用独立 Sprite
extends Node2D

# ==================== 信号 ====================
signal villager_selected(villager_id: String)

# ==================== 导出变量 ====================
@export var village_name: String = "暮色村"

# ==================== 节点引用 ====================
# TileMap 图层 (按设计文档 z-index 规范)
@onready var ground_layer: TileMapLayer = $TileMapRoot/Ground
@onready var roads_layer: TileMapLayer = $TileMapRoot/Roads
@onready var ground_decoration_layer: TileMapLayer = $TileMapRoot/GroundDecoration
@onready var water_layer: TileMapLayer = $TileMapRoot/Water
@onready var buildings_layer: TileMapLayer = $TileMapRoot/Buildings
@onready var borders_layer: TileMapLayer = $TileMapRoot/Borders

# Objects 层 (YSort) - Sprite 实现，按 Y 坐标排序 (z=10)
@onready var y_sort_root: Node2D = $YSortRoot
@onready var objects_container: Node2D = $YSortRoot/Objects
@onready var buildings_container: Node2D = $YSortRoot/Buildings
@onready var villagers_container: Node2D = $YSortRoot/Villagers
@onready var player: CharacterBody2D = $YSortRoot/Player

# UI 层
@onready var dialogue_box: Control = $UIRoot/DialogueBox
@onready var village_ui: CanvasLayer = $UIRoot
@onready var pause_menu: Control = $UIRoot/PauseMenu
@onready var save_load_ui: Control = $UIRoot/SaveLoadUI
@onready var menu_button: Button = $UIRoot/BottomBar/MenuButton
@onready var day_summary: Control = $UIRoot/DaySummary
@onready var time_overlay: CanvasModulate = $TimeOverlay

# ==================== 状态 ====================
var is_paused: bool = false
var daily_interactions: int = 0
var daily_trust_changes: Dictionary = {}

## 时间段
enum TimeOfDay { DAY, TWILIGHT, NIGHT }
var current_time: TimeOfDay = TimeOfDay.DAY

# ==================== 配置 ====================
const VillagerScene = preload("res://scenes/characters/Villager.tscn")

# 村民位置配置 (ID -> 位置) - 对齐设计文档 NPC 活动范围
const VILLAGER_POSITIONS: Dictionary = {
	"chenmo": Vector2(352, 352),    # 陈默小屋前
	"leishu": Vector2(224, 544),    # 铁匠铺前
	"jinling": Vector2(1344, 704),  # 商人行会前
	"baizhi": Vector2(352, 1024),   # 药园中
	"john": Vector2(960, 640),      # 教堂前/广场
	"daxiong": Vector2(1344, 544),  # 酒馆前
	"ying": Vector2(1632, 1024),    # 影的住所前
	"xiaoan": Vector2(448, 864),    # 学校前
	"ahu": Vector2(1312, 1184),     # 守卫营房前
	"yeya": Vector2(1632, 352)      # 观察点/废弃仓库附近
}

# 地图尺寸配置 (16px 瓦片 = 1920x1600px 像素)
const MAP_WIDTH: int = 120
const MAP_HEIGHT: int = 100
const TILE_SIZE: int = 16

# TileSet 源索引 (与 VillageTileset.tres 一致)
const SOURCE_GRASS: int = 0
const SOURCE_ROADS: int = 1
const SOURCE_WATER: int = 2

# 事件触发器配置
const TRIGGER_CONFIG_PATH: String = "res://resources/events/village_triggers.json"


func _ready() -> void:
	print("[Village] 进入村庄: %s (Y-sorting 模式)" % village_name)

	# 连接游戏管理器信号
	_connect_game_manager_signals()

	# 连接对话管理器信号
	_connect_dialogue_signals()

	# 连接信任系统信号
	_connect_trust_signals()

	# 连接UI信号
	_connect_ui_signals()

	# 连接美术风格切换信号
	_connect_art_style_signals()

	# 生成地面和道路 (TileMap)
	_generate_ground_layer()
	_generate_roads_layer()
	_generate_borders_layer()
	_generate_decorations_layer()

	# 从美术风格系统生成建筑和装饰物
	_spawn_buildings_from_style()
	_spawn_decorations_from_style()

	# 生成村民
	_spawn_villagers()

	# 初始化事件触发系统
	_init_event_trigger_system()

	# 更新 UI
	_update_ui()

	# 初始化时间光照
	_update_time_overlay()

	# 检查每日事件
	EventManager.check_events(GameManager.current_day)

	print("[Village] 地图初始化完成 - 当前风格: %s" % ArtStyleManager.current_style)


# ==================== 信号连接 ====================

func _connect_game_manager_signals() -> void:
	GameManager.day_changed.connect(_on_day_changed)
	GameManager.action_points_changed.connect(_on_action_points_changed)


func _connect_trust_signals() -> void:
	TrustManager.trust_changed.connect(_on_trust_changed)
	TrustManager.secret_unlocked.connect(_on_secret_unlocked)


func _connect_dialogue_signals() -> void:
	DialogueManager.dialogue_line_spoken.connect(_on_dialogue_line)
	DialogueManager.choice_presented.connect(_on_choices_presented)
	DialogueManager.dialogue_ended.connect(_on_dialogue_ended)


func _connect_ui_signals() -> void:
	if menu_button:
		menu_button.pressed.connect(_on_menu_button_pressed)

	if pause_menu:
		pause_menu.resume_pressed.connect(_on_resume_pressed)
		pause_menu.save_pressed.connect(_on_save_pressed)
		pause_menu.load_pressed.connect(_on_load_pressed)
		pause_menu.quit_to_menu_pressed.connect(_on_quit_to_menu_pressed)
		pause_menu.hide()

	if save_load_ui:
		save_load_ui.save_completed.connect(_on_save_completed)
		save_load_ui.load_completed.connect(_on_load_completed)
		save_load_ui.cancelled.connect(_on_save_load_cancelled)
		save_load_ui.hide()


func _connect_art_style_signals() -> void:
	"""连接美术风格切换信号"""
	if ArtStyleManager:
		ArtStyleManager.style_changed.connect(_on_art_style_changed)


# ==================== 美术风格系统集成 ====================

func _spawn_buildings_from_style() -> void:
	"""从当前美术风格生成所有建筑 Sprite"""
	print("[Village] 从风格系统生成建筑...")

	var building_configs: Dictionary = {
		"blacksmith": Vector2(192, 512),
		"church": Vector2(832, 512),
		"tavern": Vector2(1280, 512),
		"merchant": Vector2(1280, 640),
		"school": Vector2(384, 832),
		"chenmo_hut": Vector2(320, 320),
		"baizhi_garden": Vector2(320, 960),
		"guard_post": Vector2(1280, 1152),
		"abandoned_warehouse": Vector2(1280, 320),
		"ying_home": Vector2(1600, 960),
	}

	var spawned_count = 0
	for building_id in building_configs:
		var pos = building_configs[building_id]
		var building_data = ArtStyleManager.get_resource_data("building", building_id)
		if building_data.is_empty():
			print("[Village] 跳过建筑 %s: 资源数据为空" % building_id)
			continue

		var texture_path = building_data.get("full_path", "")
		if texture_path.is_empty() or not ResourceLoader.exists(texture_path):
			print("[Village] 跳过建筑 %s: 纹理不存在 %s" % [building_id, texture_path])
			continue

		var texture = load(texture_path)
		if not texture:
			continue

		var offset = building_data.get("offset", [0, 0])
		var final_pos = pos + Vector2(offset[0], offset[1])

		var building_sprite = Sprite2D.new()
		building_sprite.name = building_id
		building_sprite.position = final_pos
		building_sprite.texture = texture
		building_sprite.z_index = 5  # 建筑在 Y-sort 中正确排序

		buildings_container.add_child(building_sprite)
		spawned_count += 1
		print("[Village] 生成建筑: %s at %s" % [building_id, final_pos])

	print("[Village] 建筑生成完成: %d/%d" % [spawned_count, building_configs.size()])


func _spawn_decorations_from_style() -> void:
	"""从当前美术风格生成装饰物 Sprite"""
	print("[Village] 从风格系统生成装饰物...")

	var decoration_configs: Array = [
		{"type": "tree_pine", "pos": Vector2(200, 200), "collision": true},
		{"type": "tree_pine", "pos": Vector2(400, 150), "collision": true},
		{"type": "tree_oak", "pos": Vector2(600, 250), "collision": true},
		{"type": "tree_oak", "pos": Vector2(800, 300), "collision": true},
		{"type": "tree_fruit", "pos": Vector2(1000, 350), "collision": true},
		{"type": "street_light", "pos": Vector2(500, 500), "collision": true},
		{"type": "street_light", "pos": Vector2(700, 600), "collision": true},
		{"type": "bench", "pos": Vector2(650, 520), "collision": true},
		{"type": "well", "pos": Vector2(750, 550), "collision": true},
		{"type": "flower_bed", "pos": Vector2(550, 480), "collision": false},
		{"type": "flower_bed", "pos": Vector2(850, 580), "collision": false},
		{"type": "barrel", "pos": Vector2(400, 700), "collision": false},
	]

	var spawned_count = 0
	for deco_cfg in decoration_configs:
		var deco_type = deco_cfg["type"]
		var pos = deco_cfg["pos"]
		var has_collision = deco_cfg.get("collision", false)

		var resource_data = ArtStyleManager.get_resource_data("decoration", deco_type)
		if resource_data.is_empty():
			continue

		var texture_path = resource_data.get("full_path", "")
		if texture_path.is_empty() or not ResourceLoader.exists(texture_path):
			continue

		var texture = load(texture_path)
		if not texture:
			continue

		var decoration: Node2D
		if has_collision:
			decoration = StaticBody2D.new()
			var sprite = Sprite2D.new()
			sprite.texture = texture
			decoration.add_child(sprite)

			var collision = CollisionShape2D.new()
			var shape = RectangleShape2D.new()
			var size = resource_data.get("size", [32, 32])
			shape.size = Vector2(size[0], size[1])
			collision.shape = shape
			decoration.add_child(collision)
		else:
			decoration = Sprite2D.new()
			decoration.texture = texture

		decoration.name = deco_type + "_" + str(spawned_count)
		decoration.position = pos
		objects_container.add_child(decoration)
		spawned_count += 1

	print("[Village] 装饰物生成完成: %d 个" % spawned_count)


func _on_art_style_changed(new_style: String) -> void:
	"""美术风格切换时的回调"""
	print("[Village] 风格切换到: %s，刷新建筑和装饰物..." % new_style)

	# 清除现有的建筑和装饰物
	for child in buildings_container.get_children():
		child.queue_free()
	for child in objects_container.get_children():
		child.queue_free()

	# 重新生成
	_spawn_buildings_from_style()
	_spawn_decorations_from_style()


# ==================== 事件触发系统 ====================

func _init_event_trigger_system() -> void:
	if not EventTriggerSystem:
		return

	EventTriggerSystem.set_player(player)
	EventTriggerSystem.load_triggers(TRIGGER_CONFIG_PATH)
	EventTriggerSystem.trigger_activated.connect(_on_trigger_activated)

	print("[Village] 事件触发系统初始化完成")


func _on_trigger_activated(trigger_id: String, trigger_data: Dictionary) -> void:
	print("[Village] 触发器激活: %s" % trigger_id)

	if trigger_data.get("auto_dialogue", false):
		var message = trigger_data.get("message", "")
		if not message.is_empty():
			print("[Village] 提示: %s" % message)


# ==================== 地图生成 (TileMap 仅用于地面) ====================

func _generate_ground_layer() -> void:
	"""生成草地层 - 按区域使用不同变体（中心明亮，边缘渐暗）"""
	if not ground_layer:
		return

	for x in range(MAP_WIDTH):
		for y in range(MAP_HEIGHT):
			var tile_variant: int

			# 村庄中心（广场周围）用明亮草地变体 (0-1)
			var dist_from_center = abs(x - 60) + abs(y - 48)
			if dist_from_center < 30:
				tile_variant = randi() % 2  # 0-1 明亮
			elif dist_from_center < 55:
				tile_variant = randi() % 4  # 0-3 混合
			else:
				# 边缘用深色变体 (2-3)
				tile_variant = 2 + randi() % 2

			ground_layer.set_cell(Vector2i(x, y), SOURCE_GRASS, Vector2i(tile_variant, 0))

	print("[Village] 草地层生成完成: %dx%d tiles (区域渐变)" % [MAP_WIDTH, MAP_HEIGHT])


func _generate_roads_layer() -> void:
	"""生成道路层 - 十字主干道 + 广场 + 支路 + 村南门"""
	if not roads_layer:
		print("[Village] ERROR: roads_layer is null!")
		return

	# 使用全部 4x4 = 16 种道路变体
	var road_variants = []
	for rx in range(4):
		for ry in range(4):
			road_variants.append(Vector2i(rx, ry))

	var road_square = Vector2i(1, 0)  # 广场用较宽变体

	# ===== 东西向主干道 (12 瓦片宽) =====
	for x in range(16, 105):
		for y in range(40, 52):
			var variant = road_variants[randi() % road_variants.size()]
			roads_layer.set_cell(Vector2i(x, y), SOURCE_ROADS, variant)

	# ===== 南北向主干道 (12 瓦片宽) =====
	for y in range(20, 81):
		for x in range(56, 68):
			var variant = road_variants[randi() % road_variants.size()]
			roads_layer.set_cell(Vector2i(x, y), SOURCE_ROADS, variant)

	# ===== 中央广场区域 =====
	for x in range(48, 73):
		for y in range(36, 57):
			roads_layer.set_cell(Vector2i(x, y), SOURCE_ROADS, road_square)

	# ===== 村南门（缩小为通道，非巨大方块） =====
	for x in range(54, 66):
		for y in range(82, 92):
			roads_layer.set_cell(Vector2i(x, y), SOURCE_ROADS, road_square)

	# ===== 支路连接 =====
	# 铁匠铺支路 (向西)
	for x in range(4, 17):
		for y in range(42, 50):
			var variant = road_variants[randi() % road_variants.size()]
			roads_layer.set_cell(Vector2i(x, y), SOURCE_ROADS, variant)

	# 酒馆/商人行会支路 (向东)
	for x in range(104, 117):
		for y in range(42, 50):
			var variant = road_variants[randi() % road_variants.size()]
			roads_layer.set_cell(Vector2i(x, y), SOURCE_ROADS, variant)

	# 学校支路 (向西南)
	for x in range(24, 36):
		for y in range(52, 60):
			var variant = road_variants[randi() % road_variants.size()]
			roads_layer.set_cell(Vector2i(x, y), SOURCE_ROADS, variant)

	# 药园支路 (向西)
	for x in range(4, 20):
		for y in range(60, 68):
			var variant = road_variants[randi() % road_variants.size()]
			roads_layer.set_cell(Vector2i(x, y), SOURCE_ROADS, variant)

	# 影的住所支路 (向东)
	for x in range(104, 117):
		for y in range(60, 68):
			var variant = road_variants[randi() % road_variants.size()]
			roads_layer.set_cell(Vector2i(x, y), SOURCE_ROADS, variant)

	# 废弃仓库支路 (向东北)
	for x in range(96, 117):
		for y in range(20, 28):
			var variant = road_variants[randi() % road_variants.size()]
			roads_layer.set_cell(Vector2i(x, y), SOURCE_ROADS, variant)

	print("[Village] 道路系统生成完成")


func _generate_borders_layer() -> void:
	"""生成边界层 - 按照设计文档 (树木边界)"""
	if not borders_layer:
		return

	var tree_tile = Vector2i(0, 1)  # 松树/边界树 (OpenRPG 瓦片)

	# ===== 北边界 =====
	# 行 0-7，密集树木（黑潮方向）
	for y in range(0, 8):
		for x in range(MAP_WIDTH):
			borders_layer.set_cell(Vector2i(x, y), SOURCE_GRASS, tree_tile)

	# ===== 西边界 =====
	# 列 0-7，树木边界
	for x in range(0, 8):
		for y in range(8, MAP_HEIGHT):
			borders_layer.set_cell(Vector2i(x, y), SOURCE_GRASS, tree_tile)

	# ===== 东边界 =====
	# 列 112-119，树木边界
	for x in range(MAP_WIDTH - 8, MAP_WIDTH):
		for y in range(8, MAP_HEIGHT):
			borders_layer.set_cell(Vector2i(x, y), SOURCE_GRASS, tree_tile)

	# ===== 南边界两侧 =====
	# 村南门两侧的边界（中间是道路出口）
	# 左侧 x=0-48, 右侧 x=72-119
	for x in range(0, 49):
		for y in range(MAP_HEIGHT - 8, MAP_HEIGHT):
			borders_layer.set_cell(Vector2i(x, y), SOURCE_GRASS, tree_tile)
	for x in range(72, MAP_WIDTH):
		for y in range(MAP_HEIGHT - 8, MAP_HEIGHT):
			borders_layer.set_cell(Vector2i(x, y), SOURCE_GRASS, tree_tile)

	print("[Village] 边界生成完成")


func _generate_decorations_layer() -> void:
	"""生成地面装饰层 - 按照设计文档"""
	if not ground_decoration_layer:
		return

	# 添加一些花朵装饰在广场周围
	var flower_tile = Vector2i(2, 0)
	# 广场周围的花朵
	for x in range(44, 76, 4):
		ground_decoration_layer.set_cell(Vector2i(x, 32), SOURCE_GRASS, flower_tile)
		ground_decoration_layer.set_cell(Vector2i(x, 60), SOURCE_GRASS, flower_tile)
	for y in range(32, 60, 4):
		ground_decoration_layer.set_cell(Vector2i(44, y), SOURCE_GRASS, flower_tile)
		ground_decoration_layer.set_cell(Vector2i(76, y), SOURCE_GRASS, flower_tile)

	print("[Village] 地面装饰层生成完成")


# ==================== 建筑系统 (等待美工 Sprite 资源) ====================

func spawn_building(building_id: String, pos: Vector2, sprite_path: String) -> void:
	"""动态生成建筑 Sprite - 供美工资源加载后使用"""
	var building_sprite = Sprite2D.new()
	building_sprite.name = building_id
	building_sprite.position = pos
	building_sprite.texture = load(sprite_path)
	# Y-sorting 自动处理遮挡
	buildings_container.add_child(building_sprite)
	print("[Village] 建筑生成: %s at %s" % [building_id, pos])


func spawn_decoration(decoration_id: String, pos: Vector2, sprite_path: String, has_collision: bool = false) -> void:
	"""动态生成装饰物 Sprite"""
	var decoration: Node2D
	if has_collision:
		decoration = StaticBody2D.new()
		var sprite = Sprite2D.new()
		sprite.texture = load(sprite_path)
		decoration.add_child(sprite)
		# TODO: 添加碰撞形状
	else:
		decoration = Sprite2D.new()
		decoration.texture = load(sprite_path)

	decoration.name = decoration_id
	decoration.position = pos
	objects_container.add_child(decoration)
	print("[Village] 装饰物生成: %s at %s" % [decoration_id, pos])


# ==================== 村民生成 ====================

func _spawn_villagers() -> void:
	for villager_id in VILLAGER_POSITIONS:
		var villager = VillagerScene.instantiate()
		villager.villager_id = villager_id
		villager.position = VILLAGER_POSITIONS[villager_id]
		villager.dialogue_started.connect(_on_villager_dialogue_started)
		villager.dialogue_ended.connect(_on_villager_dialogue_ended)
		villagers_container.add_child(villager)

	print("[Village] 已生成 %d 位村民" % VILLAGER_POSITIONS.size())


# ==================== 对话系统回调 ====================

func _on_villager_dialogue_started(villager_id: String) -> void:
	print("[Village] 村民 %s 开始对话" % villager_id)
	villager_selected.emit(villager_id)
	if dialogue_box:
		dialogue_box.show()
	daily_interactions += 1


func _on_villager_dialogue_ended() -> void:
	pass


func _consume_action_point() -> void:
	GameManager.action_points -= 1
	GameManager.action_points_changed.emit(GameManager.action_points)
	_update_ui()
	print("[Village] 消耗 1 行动点，剩余 %d" % GameManager.action_points)

	if GameManager.action_points <= 0:
		_show_day_summary_and_advance()


func _show_day_summary_and_advance() -> void:
	var completed_day = GameManager.current_day

	if day_summary:
		day_summary.show_summary(completed_day, daily_interactions, daily_trust_changes)
		await day_summary.continue_pressed

	_reset_daily_stats()
	GameManager.advance_day()
	_update_ui()
	EventManager.check_events(GameManager.current_day)


func _on_dialogue_line(_speaker: String, _text: String) -> void:
	pass


func _on_choices_presented(_choices: Array) -> void:
	pass


func _on_dialogue_ended(_villager_id: String) -> void:
	print("[Village] 对话结束 (DialogueManager)")
	if dialogue_box:
		dialogue_box.hide()
	_consume_action_point()


# ==================== UI 更新 ====================

func _update_ui() -> void:
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
	print("[Village] 进入第 %d 天" % new_day)
	current_time = TimeOfDay.DAY
	_update_ui()
	_update_time_overlay()
	EventManager.check_events(new_day)


func _reset_daily_stats() -> void:
	daily_interactions = 0
	daily_trust_changes.clear()


func _on_action_points_changed(new_points: int) -> void:
	_update_ui()
	_update_time_from_action_points(new_points)
	if new_points <= 0:
		print("[Village] 行动点耗尽，即将进入下一天")


func _update_time_overlay() -> void:
	if not time_overlay:
		return

	match current_time:
		TimeOfDay.DAY:
			time_overlay.color = Color(1.0, 1.0, 1.0, 1.0)
		TimeOfDay.TWILIGHT:
			time_overlay.color = Color(0.9, 0.7, 0.6, 1.0)
		TimeOfDay.NIGHT:
			time_overlay.color = Color(0.3, 0.3, 0.5, 1.0)


func _update_time_from_action_points(points: int) -> void:
	var max_points = GameManager.MAX_ACTION_POINTS
	var old_time = current_time

	if points > max_points * 0.6:
		current_time = TimeOfDay.DAY
	elif points > max_points * 0.3:
		current_time = TimeOfDay.TWILIGHT
	else:
		current_time = TimeOfDay.NIGHT

	if current_time != old_time:
		_update_time_overlay()


func _on_trust_changed(villager_id: String, _old_value: int, new_value: int) -> void:
	print("[Village] %s 信任值更新为 %d" % [villager_id, new_value])

	if not daily_trust_changes.has(villager_id):
		daily_trust_changes[villager_id] = 0
	daily_trust_changes[villager_id] += new_value - _old_value
	_update_villager_trust_display(villager_id, new_value)


func _on_secret_unlocked(villager_id: String, secret_id: String) -> void:
	print("[Village] 解锁 %s 的秘密: %s" % [villager_id, secret_id])


func _update_villager_trust_display(villager_id: String, trust_value: int) -> void:
	if villagers_container:
		for child in villagers_container.get_children():
			if child.villager_id == villager_id:
				child.set_trust_value(trust_value)


# ==================== 输入处理 ====================

func _input(event: InputEvent) -> void:
	if event.is_action_pressed("ui_cancel"):
		_on_menu_button_pressed()


func _on_menu_button_pressed() -> void:
	print("[Village] 打开菜单")
	_pause_game()
	if pause_menu:
		pause_menu.show_menu()


# ==================== 暂停菜单回调 ====================

func _pause_game() -> void:
	is_paused = true
	get_tree().paused = true


func _resume_game() -> void:
	is_paused = false
	get_tree().paused = false


func _on_resume_pressed() -> void:
	print("[Village] 继续游戏")
	_resume_game()
	if pause_menu:
		pause_menu.hide_menu()


func _on_save_pressed() -> void:
	print("[Village] 打开保存界面")
	if pause_menu:
		pause_menu.hide_menu()
	if save_load_ui:
		save_load_ui.show_save_mode()


func _on_load_pressed() -> void:
	print("[Village] 打开读取界面")
	if pause_menu:
		pause_menu.hide_menu()
	if save_load_ui:
		save_load_ui.show_load_mode()


func _on_quit_to_menu_pressed() -> void:
	print("[Village] 返回主菜单")
	_resume_game()
	var result = get_tree().change_scene_to_file("res://scenes/Main.tscn")
	if result != OK:
		push_error("[Village] 无法返回主菜单")


# ==================== 存档界面回调 ====================

func _on_save_completed(_slot_index: int) -> void:
	print("[Village] 存档完成")
	if save_load_ui:
		save_load_ui.hide()
	if pause_menu:
		pause_menu.show_menu()


func _on_load_completed(_slot_index: int) -> void:
	print("[Village] 读档完成")
	_resume_game()
	if save_load_ui:
		save_load_ui.hide()
	_update_ui()

	if GameManager.player_data.has("saved_position"):
		var saved_pos = GameManager.player_data.saved_position
		player.global_position = saved_pos
		print("[Village] 恢复玩家位置: %s" % str(saved_pos))
		GameManager.player_data.erase("saved_position")

	_spawn_villagers_after_load()


func _on_save_load_cancelled() -> void:
	print("[Village] 取消存档操作")
	if save_load_ui:
		save_load_ui.hide()
	if pause_menu:
		pause_menu.show_menu()


func _spawn_villagers_after_load() -> void:
	if villagers_container:
		for child in villagers_container.get_children():
			child.queue_free()
	_spawn_villagers()