## ArtStyleIntegration - 美术风格集成辅助
## 提供使用 ArtStyleManager 的便捷函数
extends Node

## 建筑位置配置
const BUILDING_POSITIONS: Dictionary = {
	"chenmo_hut": Vector2(352, 352),
	"leishu": Vector2(352, 672),
	"blacksmith": Vector2(352, 672),
	"jinling": Vector2(1440, 800),
	"merchant": Vector2(1440, 800),
	"baizhi": Vector2(352, 992),
	"baizhi_garden": Vector2(352, 992),
	"john": Vector2(992, 672),
	"church": Vector2(992, 672),
	"daxiong": Vector2(1440, 672),
	"tavern": Vector2(1440, 672),
	"ying": Vector2(1632, 992),
	"ying_home": Vector2(1632, 992),
	"xiaoan": Vector2(544, 992),
	"school": Vector2(544, 992),
	"ahu": Vector2(1312, 1184),
	"guard_post": Vector2(1312, 1184),
	"yeya": Vector2(1632, 352),
	"abandoned_warehouse": Vector2(1632, 352),
}

## 装饰物示例位置
const DECORATION_EXAMPLES: Array = [
	{"type": "tree_pine", "pos": Vector2(200, 200)},
	{"type": "tree_oak", "pos": Vector2(400, 300)},
	{"type": "street_light", "pos": Vector2(600, 400)},
	{"type": "bench", "pos": Vector2(800, 500)},
	{"type": "well", "pos": Vector2(1000, 600)},
]

func spawn_buildings_from_style(buildings_container: Node2D) -> void:
	"""从当前风格生成所有建筑"""
	print("[ArtStyleIntegration] 开始生成建筑...")
	
	var building_ids = [
		"blacksmith", "church", "tavern", "merchant", "school",
		"chenmo_hut", "baizhi_garden", "guard_post", 
		"abandoned_warehouse", "ying_home"
	]
	
	for building_id in building_ids:
		var building_data = ArtStyleManager.get_resource_data("building", building_id)
		
		if building_data.is_empty():
			continue
		
		var texture_path = building_data.get("full_path", "")
		if texture_path.is_empty() or not ResourceLoader.exists(texture_path):
			continue
		
		var pos = BUILDING_POSITIONS.get(building_id, Vector2(500, 500))
		var offset = building_data.get("offset", Vector2(0, 0))
		
		# 创建建筑 Sprite
		var building_sprite = Sprite2D.new()
		building_sprite.name = building_id
		building_sprite.position = pos + Vector2(offset[0], offset[1])
		building_sprite.texture = load(texture_path)
		
		buildings_container.add_child(building_sprite)
		print("[ArtStyleIntegration] 生成建筑: %s" % building_id)

func spawn_decorations_from_style(objects_container: Node2D) -> void:
	"""从当前风格生成示例装饰物"""
	print("[ArtStyleIntegration] 开始生成装饰物...")
	
	for deco_data in DECORATION_EXAMPLES:
		var deco_type = deco_data["type"]
		var pos = deco_data["pos"]
		
		var resource_data = ArtStyleManager.get_resource_data("decoration", deco_type)
		
		if resource_data.is_empty():
			continue
		
		var texture_path = resource_data.get("full_path", "")
		if texture_path.is_empty() or not ResourceLoader.exists(texture_path):
			continue
		
		var has_collision = resource_data.get("has_collision", false)
		
		var decoration: Node2D
		if has_collision:
			decoration = StaticBody2D.new()
			var sprite = Sprite2D.new()
			sprite.texture = load(texture_path)
			decoration.add_child(sprite)
			
			# 添加碰撞形状
			var collision = CollisionShape2D.new()
			var shape = RectangleShape2D.new()
			var size = resource_data.get("size", [32, 32])
			shape.size = Vector2(size[0], size[1])
			collision.shape = shape
			decoration.add_child(collision)
		else:
			decoration = Sprite2D.new()
			decoration.texture = load(texture_path)
		
		decoration.name = deco_type
		decoration.position = pos
		objects_container.add_child(decoration)
		
		print("[ArtStyleIntegration] 生成装饰物: %s" % deco_type)
