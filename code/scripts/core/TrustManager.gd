## Trust Manager - 信任系统管理器
## 负责管理玩家与村民之间的信任关系
extends Node

# ==================== 信号 ====================
signal trust_changed(villager_id: String, old_value: int, new_value: int)
signal trust_threshold_reached(villager_id: String, threshold: int)
signal secret_unlocked(villager_id: String, secret_id: String)

# ==================== 信任等级定义 ====================
enum TrustLevel {
	HOSTILE,		# 0-20: 敌对/警惕
	NEUTRAL,		# 21-40: 中立
	FRIENDLY,		# 41-60: 友好
	TRUSTED,		# 61-80: 信任
	DEVOTED		# 81-100: 忠诚
}

# ==================== 信任数据 ====================
var trust_data: Dictionary = {}

# ==================== 村民秘密定义 ====================
# 信任值达到一定程度后可解锁的秘密
var villager_secrets: Dictionary = {
	"chenmo": {
		"secret_id": "chenmo_secret",
		"description": "陈默是逃兵，队长的孩子就在村子里",
		"unlock_trust": 80,
		"unlocked": false
	},
	"yeya": {
		"secret_id": "yeya_secret",
		"description": "夜鸦是魔王军的卧底",
		"unlock_trust": 85,
		"unlocked": false
	},
	"jinling": {
		"secret_id": "jinling_secret",
		"description": "金铃曾是盗贼团的二把手",
		"unlock_trust": 70,
		"unlocked": false
	}
}


func _ready() -> void:
	print("[TrustManager] 信任系统初始化完成")
	_init_trust_data()


# ==================== 初始化 ====================

## 初始化信任数据
func _init_trust_data() -> void:
	var villagers = [
		"chenmo", "leishu", "jinling", "baizhi", "john",
		"daxiong", "ying", "xiaoan", "ahu", "yeya"
	]

	for villager in villagers:
		trust_data[villager] = {
			"value": 0,
			"history": [],		# 信任变化历史
			"unlocked_secrets": []
		}


# ==================== 信任值操作 ====================

## 获取信任值
func get_trust(villager_id: String) -> int:
	if trust_data.has(villager_id):
		return trust_data[villager_id].value
	return 0


## 获取信任等级
func get_trust_level(villager_id: String) -> TrustLevel:
	var trust = get_trust(villager_id)

	if trust <= 20:
		return TrustLevel.HOSTILE
	elif trust <= 40:
		return TrustLevel.NEUTRAL
	elif trust <= 60:
		return TrustLevel.FRIENDLY
	elif trust <= 80:
		return TrustLevel.TRUSTED
	else:
		return TrustLevel.DEVOTED


## 获取信任等级名称
func get_trust_level_name(villager_id: String) -> String:
	var level = get_trust_level(villager_id)
	match level:
		TrustLevel.HOSTILE: return "警惕"
		TrustLevel.NEUTRAL: return "中立"
		TrustLevel.FRIENDLY: return "友好"
		TrustLevel.TRUSTED: return "信任"
		TrustLevel.DEVOTED: return "忠诚"
		_: return "未知"


## 修改信任值
func modify_trust(villager_id: String, amount: int, reason: String = "") -> void:
	if not trust_data.has(villager_id):
		print("[TrustManager] 未找到村民: %s" % villager_id)
		return

	var old_value = trust_data[villager_id].value
	var new_value = clamp(old_value + amount, 0, 100)
	trust_data[villager_id].value = new_value

	# 记录历史
	trust_data[villager_id].history.append({
		"change": amount,
		"reason": reason,
		"timestamp": Time.get_unix_time_from_system(),
		"day": GameManager.current_day
	})

	trust_changed.emit(villager_id, old_value, new_value)

	# 检查信任阈值
	_check_trust_thresholds(villager_id, old_value, new_value)

	print("[TrustManager] %s 信任值: %d -> %d (%+d) %s" % [
		villager_id, old_value, new_value, amount, reason
	])


## 设置信任值（直接设置，用于存档加载）
func set_trust(villager_id: String, value: int) -> void:
	if trust_data.has(villager_id):
		trust_data[villager_id].value = clamp(value, 0, 100)


# ==================== 信任阈值检测 ====================

## 检查信任阈值
func _check_trust_thresholds(villager_id: String, old_value: int, new_value: int) -> void:
	var thresholds = [20, 40, 60, 80, 100]

	for threshold in thresholds:
		if old_value < threshold and new_value >= threshold:
			trust_threshold_reached.emit(villager_id, threshold)
			print("[TrustManager] %s 达到信任阈值 %d" % [villager_id, threshold])

	# 检查是否解锁秘密
	_check_secret_unlock(villager_id, new_value)


## 检查秘密解锁
func _check_secret_unlock(villager_id: String, trust_value: int) -> void:
	if villager_secrets.has(villager_id):
		var secret = villager_secrets[villager_id]
		if not secret.unlocked and trust_value >= secret.unlock_trust:
			secret.unlocked = true
			trust_data[villager_id].unlocked_secrets.append(secret.secret_id)
			secret_unlocked.emit(villager_id, secret.secret_id)
			print("[TrustManager] 解锁 %s 的秘密: %s" % [villager_id, secret.description])


# ==================== 对话影响 ====================

## 获取信任值对话影响
## 返回对话态度修正
func get_dialogue_attitude_modifier(villager_id: String) -> Dictionary:
	var level = get_trust_level(villager_id)

	match level:
		TrustLevel.HOSTILE:
			return {
				"response_length": "short",
				"willingness_to_help": false,
				"info_sharing": "minimal"
			}
		TrustLevel.NEUTRAL:
			return {
				"response_length": "normal",
				"willingness_to_help": false,
				"info_sharing": "basic"
			}
		TrustLevel.FRIENDLY:
			return {
				"response_length": "normal",
				"willingness_to_help": true,
				"info_sharing": "moderate"
			}
		TrustLevel.TRUSTED:
			return {
				"response_length": "detailed",
				"willingness_to_help": true,
				"info_sharing": "extensive"
			}
		TrustLevel.DEVOTED:
			return {
				"response_length": "detailed",
				"willingness_to_help": true,
				"info_sharing": "full"
			}
		_:
			return {}


# ==================== 存档支持 ====================

## 获取存档数据
func get_save_data() -> Dictionary:
	return {
		"trust_data": trust_data.duplicate(true),
		"villager_secrets": villager_secrets.duplicate(true)
	}


## 加载存档数据
func load_save_data(data: Dictionary) -> void:
	if data.has("trust_data"):
		trust_data = data.trust_data
	if data.has("villager_secrets"):
		villager_secrets = data.villager_secrets