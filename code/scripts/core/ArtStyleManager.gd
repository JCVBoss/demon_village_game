## ArtStyleManager - 美术风格管理器
## 管理美术风格切换和资源加载
extends Node
class_name ArtStyleManager
signal style_changed(new_style: String)

## 当前激活的风格
var current_style: String = "default"

## 风格清单缓存
var style_manifests: Dictionary = {}

## 风格基础路径
const STYLES_BASE_PATH: String = "res://assets/styles"

func _ready() -> void:
	print("[ArtStyleManager] 初始化美术风格管理器")
	load_style_manifest(current_style)

func get_available_styles() -> Array:
	"""获取可用的风格列表"""
	var styles: Array = []
	
	# 检查 styles 目录下的子文件夹
	# 注意：在导出的游戏中需要使用 DirAccess
	var dir = DirAccess.open(STYLES_BASE_PATH)
	if dir:
		dir.list_dir_begin()
		var file_name = dir.get_next()
		while file_name != "":
			if dir.current_is_dir() and not file_name.begins_with("."):
				styles.append(file_name)
			file_name = dir.get_next()
	
	if styles.is_empty():
		styles.append("default")
	
	return styles

func load_style_manifest(style_name: String) -> Dictionary:
	"""加载风格清单文件"""
	if style_manifests.has(style_name):
		return style_manifests[style_name]
	
	var manifest_path = "%s/%s/manifest.json" % [STYLES_BASE_PATH, style_name]
	
	if not ResourceLoader.exists(manifest_path):
		push_error("[ArtStyleManager] 风格清单不存在: %s" % manifest_path)
		# 回退到默认风格
		if style_name != "default":
			return load_style_manifest("default")
		return {}
	
	var file = FileAccess.open(manifest_path, FileAccess.READ)
	if file == null:
		push_error("[ArtStyleManager] 无法打开风格清单: %s" % manifest_path)
		return {}
	
	var json_text = file.get_as_text()
	file.close()
	
	var json = JSON.new()
	var error = json.parse(json_text)
	if error != OK:
		push_error("[ArtStyleManager] JSON 解析错误: %s" % json.get_error_message())
		return {}
	
	var manifest = json.data
	style_manifests[style_name] = manifest
	
	print("[ArtStyleManager] 加载风格清单: %s" % style_name)
	return manifest

func switch_style(style_name: String) -> bool:
	"""切换美术风格"""
	if style_name == current_style:
		return true
	
	if not is_style_available(style_name):
		push_error("[ArtStyleManager] 风格不可用: %s" % style_name)
		return false
	
	current_style = style_name
	load_style_manifest(style_name)
	
	print("[ArtStyleManager] 切换到风格: %s" % style_name)
	style_changed.emit(style_name)
	
	return true

func is_style_available(style_name: String) -> bool:
	"""检查风格是否可用"""
	var styles = get_available_styles()
	return styles.has(style_name)

func get_resource_path(resource_type: String, resource_name: String) -> String:
	"""获取资源的完整路径"""
	var manifest = load_style_manifest(current_style)
	
	if manifest.is_empty():
		return ""
	
	# 根据资源类型查找
	var resource_map: Dictionary
	match resource_type:
		"tileset":
			resource_map = manifest.get("tilesets", {})
		"building":
			resource_map = manifest.get("buildings", {})
		"decoration":
			resource_map = manifest.get("decorations", {})
		"character":
			resource_map = manifest.get("characters", {})
		"ui":
			resource_map = manifest.get("ui", {})
		"background":
			resource_map = manifest.get("backgrounds", {})
		_:
			return ""
	
	if not resource_map.has(resource_name):
		# 尝试从默认风格获取
		if current_style != "default":
			var old_style = current_style
			current_style = "default"
			var path = get_resource_path(resource_type, resource_name)
			current_style = old_style
			return path
		return ""
	
	var resource_data = resource_map[resource_name]
	var relative_path: String
	
	if typeof(resource_data) == TYPE_DICTIONARY:
		relative_path = resource_data.get("path", "")
	else:
		relative_path = resource_data
	
	if relative_path.is_empty():
		return ""
	
	return "%s/%s/%s" % [STYLES_BASE_PATH, current_style, relative_path]

func get_resource_data(resource_type: String, resource_name: String) -> Dictionary:
	"""获取资源的完整数据（包含尺寸、偏移等）"""
	var manifest = load_style_manifest(current_style)
	
	if manifest.is_empty():
		return {}
	
	var resource_map: Dictionary
	match resource_type:
		"tileset":
			resource_map = manifest.get("tilesets", {})
		"building":
			resource_map = manifest.get("buildings", {})
		"decoration":
			resource_map = manifest.get("decorations", {})
		"character":
			resource_map = manifest.get("characters", {})
		_:
			return {}
	
	if not resource_map.has(resource_name):
		# 尝试从默认风格获取
		if current_style != "default":
			var old_style = current_style
			current_style = "default"
			var data = get_resource_data(resource_type, resource_name)
			current_style = old_style
			return data
		return {}
	
	var resource_data = resource_map[resource_name]
	if typeof(resource_data) == TYPE_DICTIONARY:
		# 添加完整路径
		var result = resource_data.duplicate()
		if result.has("path"):
			result["full_path"] = "%s/%s/%s" % [STYLES_BASE_PATH, current_style, result["path"]]
		return result
	
	return {}

func get_tile_size() -> int:
	"""获取当前风格的瓦片大小"""
	var manifest = load_style_manifest(current_style)
	return manifest.get("tile_size", 64)
