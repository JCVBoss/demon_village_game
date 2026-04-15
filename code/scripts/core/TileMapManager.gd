## TileMapManager - TileMap 地图管理器
## 负责加载地图配置、生成 TileMap、管理碰撞和区域切换
extends Node
class_name TileMapManager

# ==================== 信号 ====================
signal map_loaded(map_name: String)
signal transition_triggered(transition_id: String, target_scene: String)

# ==================== 导出变量 ====================
@export var map_config_path: String = "res://resources/maps/village_map_config.json"

# ==================== 节点引用 ====================
@onready var ground_layer: TileMapLayer = $Ground
@onready var roads_layer: TileMapLayer = $Roads
@onready var buildings_layer: TileMapLayer = $Buildings
@onready var decorations_layer: TileMapLayer = $Decorations
@onready var water_layer: TileMapLayer = $Water
@onready var borders_layer: TileMapLayer = $Borders

# ==================== 状态 ====================
var map_config: Dictionary = {}
var map_name: String = ""
var map_size: Vector2i = Vector2i.ZERO
var tile_size: int = 64

# TileSet 源索引
const SOURCE_GRASS: int = 0
const SOURCE_ROADS: int = 1
const SOURCE_BUILDINGS: int = 2
const SOURCE_WATER: int = 3
const SOURCE_BORDERS: int = 4


func _ready() -> void:
	print("[TileMapManager] 初始化地图管理器")
	load_map_config(map_config_path)


# ==================== 配置加载 ====================

func load_map_config(path: String) -> bool:
	"""加载地图配置文件"""
	if not ResourceLoader.exists(path):
		push_error("[TileMapManager] 配置文件不存在: %s" % path)
		return false

	var file = FileAccess.open(path, FileAccess.READ)
	if file == null:
		push_error("[TileMapManager] 无法打开配置文件: %s" % path)
		return false

	var json_text = file.get_as_text()
	file.close()

	var json = JSON.new()
	var error = json.parse(json_text)
	if error != OK:
		push_error("[TileMapManager] JSON 解析错误: %s" % json.get_error_message())
		return false

	map_config = json.data
	map_name = map_config.get("map_name", "Unknown")
	map_size = Vector2i(
		map_config.get("map_width", 30),
		map_config.get("map_height", 25)
	)
	tile_size = map_config.get("tile_size", 64)

	print("[TileMapManager] 加载地图配置: %s (%dx%d)" % [map_name, map_size.x, map_size.y])

	# 生成默认地图
	generate_default_map()

	map_loaded.emit(map_name)
	return true


# ==================== 地图生成 ====================

func generate_default_map() -> void:
	"""生成默认村庄地图布局"""
	# 清除现有瓦片
	clear_all_layers()

	# 生成草地底图
	_generate_ground_layer()

	# 生成道路
	_generate_roads_layer()

	# 生成边界树木
	_generate_borders()

	print("[TileMapManager] 默认地图生成完成")


func clear_all_layers() -> void:
	"""清除所有图层"""
	if ground_layer:
		ground_layer.clear()
	if roads_layer:
		roads_layer.clear()
	if buildings_layer:
		buildings_layer.clear()
	if decorations_layer:
		decorations_layer.clear()
	if water_layer:
		water_layer.clear()
	if borders_layer:
		borders_layer.clear()


func _generate_ground_layer() -> void:
	"""生成草地层"""
	if not ground_layer:
		return

	# 填充整个地图为草地
	for x in range(map_size.x):
		for y in range(map_size.y):
			# 使用随机草地瓦片增加变化
			var tile_coords = Vector2i(randi() % 4, 0)
			ground_layer.set_cell(Vector2i(x, y), SOURCE_GRASS, tile_coords)


func _generate_roads_layer() -> void:
	"""生成道路层"""
	if not roads_layer:
		return

	# 主干道：东西向 (y=12, 13)
	for x in range(4, 26):
		roads_layer.set_cell(Vector2i(x, 12), SOURCE_ROADS, Vector2i(0, 0))
		roads_layer.set_cell(Vector2i(x, 13), SOURCE_ROADS, Vector2i(1, 0))

	# 主干道：南北向 (x=14, 15)
	for y in range(14, 24):
		roads_layer.set_cell(Vector2i(14, y), SOURCE_ROADS, Vector2i(0, 0))
		roads_layer.set_cell(Vector2i(15, y), SOURCE_ROADS, Vector2i(1, 0))

	# 广场区域 (中心)
	for x in range(12, 18):
		for y in range(10, 14):
			roads_layer.set_cell(Vector2i(x, y), SOURCE_ROADS, Vector2i(2, 0))


func _generate_borders() -> void:
	"""生成边界（树木）"""
	if not borders_layer:
		return

	# 北边界
	for x in range(map_size.x):
		borders_layer.set_cell(Vector2i(x, 0), SOURCE_BORDERS, Vector2i(0, 0))
		borders_layer.set_cell(Vector2i(x, 1), SOURCE_BORDERS, Vector2i(1, 0))

	# 南边界
	for x in range(map_size.x):
		borders_layer.set_cell(Vector2i(x, map_size.y - 1), SOURCE_BORDERS, Vector2i(0, 0))

	# 西边界
	for y in range(map_size.y):
		borders_layer.set_cell(Vector2i(0, y), SOURCE_BORDERS, Vector2i(0, 0))
		borders_layer.set_cell(Vector2i(1, y), SOURCE_BORDERS, Vector2i(1, 0))

	# 东边界
	for y in range(map_size.y):
		borders_layer.set_cell(Vector2i(map_size.x - 1, y), SOURCE_BORDERS, Vector2i(0, 0))


# ==================== 建筑生成 ====================

func place_building(_building_id: String, pos: Vector2i, size: Vector2i, _has_collision: bool = true) -> void:
	"""放置建筑"""
	if not buildings_layer:
		return

	for x in range(size.x):
		for y in range(size.y):
			var tile_pos = Vector2i(pos.x + x, pos.y + y)
			var tile_coords = Vector2i(x % 4, y % 4)
			buildings_layer.set_cell(tile_pos, SOURCE_BUILDINGS, tile_coords)


# ==================== 查询功能 ====================

func get_pixel_size() -> Vector2:
	"""获取地图像素尺寸"""
	return Vector2(map_size.x * tile_size, map_size.y * tile_size)


func tile_to_pixel(tile_pos: Vector2i) -> Vector2:
	"""瓦片坐标转像素坐标"""
	return Vector2(tile_pos.x * tile_size + tile_size / 2, tile_pos.y * tile_size + tile_size / 2)


func pixel_to_tile(pixel_pos: Vector2) -> Vector2i:
	"""像素坐标转瓦片坐标"""
	return Vector2i(int(pixel_pos.x / tile_size), int(pixel_pos.y / tile_size))


func is_valid_tile(tile_pos: Vector2i) -> bool:
	"""检查瓦片坐标是否有效"""
	return tile_pos.x >= 0 and tile_pos.x < map_size.x and tile_pos.y >= 0 and tile_pos.y < map_size.y


func get_map_bounds() -> Rect2:
	"""获取地图边界"""
	return Rect2(Vector2.ZERO, get_pixel_size())