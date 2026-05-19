## DynamicTileSetManager - 动态瓦片集管理器
## 从风格目录动态创建和管理 TileSet
extends Node
class_name DynamicTileSetManager

## 瓦片集缓存
var tile_sets: Dictionary = {}

## 瓦片源 ID 映射
var tile_source_ids: Dictionary = {}

func _ready() -> void:
	print("[DynamicTileSetManager] 初始化动态瓦片集管理器")

func create_tile_set_from_style() -> TileSet:
	"""从当前风格创建 TileSet"""
	var tile_set = TileSet.new()
	
	# 获取瓦片集配置
	var manifest = ArtStyleManager.load_style_manifest(ArtStyleManager.current_style)
	var tilesets_config = manifest.get("tilesets", {})
	
	var source_id = 0
	
	# 为每个瓦片集创建 TileSetAtlasSource
	for tileset_name in tilesets_config:
		var tileset_data = tilesets_config[tileset_name]
		var texture_path = ArtStyleManager.get_resource_path("tileset", tileset_name)
		
		if texture_path.is_empty() or not ResourceLoader.exists(texture_path):
			push_warning("[DynamicTileSetManager] 瓦片集纹理不存在: %s" % tileset_name)
			continue
		
		var texture = load(texture_path)
		if not texture:
			continue
		
		# 创建 TileSetAtlasSource
		var atlas_source = TileSetAtlasSource.new()
		atlas_source.texture = texture
		
		# 获取瓦片尺寸和排列
		var columns = tileset_data.get("columns", 4)
		var rows = tileset_data.get("rows", 1)
		var tile_size = ArtStyleManager.get_tile_size()
		
		atlas_source.texture_region_size = Vector2i(tile_size, tile_size)
		
		# 添加瓦片
		for y in range(rows):
			for x in range(columns):
				var atlas_coord = Vector2i(x, y)
				atlas_source.create_tile(atlas_coord)
		
		# 添加到 TileSet
		tile_set.add_source(atlas_source, source_id)
		
		# 记录源 ID
		tile_source_ids[tileset_name] = source_id
		
		source_id += 1
	
	print("[DynamicTileSetManager] 创建 TileSet 完成，%d 个源" % source_id)
	return tile_set

func get_tile_source_id(tileset_name: String) -> int:
	"""获取瓦片集的源 ID"""
	if tile_source_ids.has(tileset_name):
		return tile_source_ids[tileset_name]
	return -1

func apply_tile_set_to_layers(tile_map: TileMap, layers_config: Dictionary) -> void:
	"""将 TileSet 应用到 TileMap 的图层"""
	var tile_set = create_tile_set_from_style()
	
	for layer_name in layers_config:
		var layer_data = layers_config[layer_name]
		var layer = tile_map.get_layer_by_name(layer_name)
		if layer:
			layer.tile_set = tile_set
			print("[DynamicTileSetManager] 应用 TileSet 到图层: %s" % layer_name)

func clear_cache() -> void:
	"""清除缓存"""
	tile_sets.clear()
	tile_source_ids.clear()
