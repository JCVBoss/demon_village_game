<!-- [TAG] 所有者:PO|维护责任人:AliceDesigner|创建时间:2026-03-17|生效标记:✅|最后更新:2026-03-17|版本:v1.0 -->
# 陈默完整对话树

## 📋 对话树结构说明

**角色：** 陈默（逃兵/退休冒险者）  
**信任阶段：** 4 个阶段（警惕→中立→友好→信任）  
**对话模式：** 混合模式（固定文本 + LLM 生成）

---

## 🌳 对话树总览

```
初始对话 (信任 0-20)
├─ 友好打招呼 → 友好 greeting 分支
├─ 询问村子情况 → 村子信息分支
└─ 保持沉默离开 → 结束（信任 -2）

信任 21-40 对话
├─ 询问他的过去 → 回避分支
├─ 请求帮助 → 条件帮助分支
└─ 聊日常 → 日常对话分支

信任 41-60 对话
├─ 提及"逃兵"话题 → 冲突分支
├─ 询问小安 → 保护欲分支
└─ 邀请加入队伍 → 犹豫分支

信任 61-80 对话
├─ 坦白知道他的秘密 → 坦白分支 🔓
├─ 询问队长的事 → 回忆分支
└─ 请求并肩作战 → 决心分支
```

---

## 📍 阶段 1：警惕（信任 0-20）

### 初始对话节点

**触发条件：** 首次与陈默对话，信任值 0-20

```json
{
  "node_id": "chenmo_initial",
  "speaker": "chenmo",
  "lines": [
    {"speaker": "chenmo", "text": "......你是新来的？"},
    {"speaker": "chenmo", "text": "（他上下打量你，眼神警惕）"},
    {"speaker": "chenmo", "text": "我不认识你，也不想认识。没事的话，让开。"}
  ],
  "choices": [
    {
      "text": "友好地打招呼",
      "trust_change": 5,
      "next_node": "chenmo_friendly_greeting"
    },
    {
      "text": "直接询问村子情况",
      "trust_change": 0,
      "next_node": "chenmo_ask_village"
    },
    {
      "text": "保持沉默离开",
      "trust_change": -2,
      "next_node": "chenmo_leave_silently"
    }
  ]
}
```

### 分支 1：友好打招呼

```json
{
  "node_id": "chenmo_friendly_greeting",
  "speaker": "chenmo",
  "lines": [
    {"speaker": "player", "text": "你好，我叫勇者。听说村子需要帮忙？"},
    {"speaker": "chenmo", "text": "......帮忙？"},
    {"speaker": "chenmo", "text": "（沉默片刻）如果你真的想帮忙，去找大熊吧。"},
    {"speaker": "chenmo", "text": "酒馆在东边。他比我...更会说话。"}
  ],
  "choices": [
    {
      "text": "谢谢，我会去找他",
      "trust_change": 3,
      "next_node": null
    },
    {
      "text": "你为什么不去帮忙？",
      "trust_change": -3,
      "next_node": "chenmo_why_not_help"
    }
  ]
}
```

### 分支 2：询问村子情况

```json
{
  "node_id": "chenmo_ask_village",
  "speaker": "chenmo",
  "lines": [
    {"speaker": "player", "text": "请问这个村子是什么情况？"},
    {"speaker": "chenmo", "text": "......"},
    {"speaker": "chenmo", "text": "（他看向远处的魔王城，眼神复杂）"},
    {"speaker": "chenmo", "text": "自己去酒馆问。我还有事。"}
  ],
  "choices": [
    {
      "text": "好吧，打扰了",
      "trust_change": 0,
      "next_node": null
    }
  ]
}
```

### 分支 3：保持沉默离开

```json
{
  "node_id": "chenmo_leave_silently",
  "speaker": "chenmo",
  "lines": [
    {"speaker": "player", "text": "......"},
    {"speaker": "chenmo", "text": "（他看着你离开，没有说话）"}
  ],
  "choices": []
}
```

---

## 📍 阶段 2：中立（信任 21-40）

### 解锁新对话选项

**触发条件：** 信任值 21-40

```json
{
  "node_id": "chenmo_trust_21",
  "speaker": "chenmo",
  "lines": [
    {"speaker": "chenmo", "text": "......又是你。"},
    {"speaker": "chenmo", "text": "（态度稍有缓和）有事？"}
  ],
  "choices": [
    {
      "text": "询问他的过去",
      "trust_change": 0,
      "next_node": "chenmo_ask_past"
    },
    {
      "text": "请求帮助",
      "trust_change": 2,
      "next_node": "chenmo_ask_help"
    },
    {
      "text": "聊日常",
      "trust_change": 3,
      "next_node": "chenmo_small_talk"
    }
  ]
}
```

### 分支 1：询问他的过去

```json
{
  "node_id": "chenmo_ask_past",
  "speaker": "chenmo",
  "lines": [
    {"speaker": "player", "text": "你以前是冒险者吗？"},
    {"speaker": "chenmo", "text": "（身体僵硬了一瞬）"},
    {"speaker": "chenmo", "text": "......那是很久以前的事了。"},
    {"speaker": "chenmo", "text": "都过去了。别提了。"}
  ],
  "choices": [
    {
      "text": "抱歉，我不该问",
      "trust_change": 3,
      "next_node": null
    },
    {
      "text": "但你的眼神里有故事",
      "trust_change": -5,
      "next_node": "chenmo_push_past"
    }
  ]
}
```

### 分支 2：请求帮助

```json
{
  "node_id": "chenmo_ask_help",
  "speaker": "chenmo",
  "lines": [
    {"speaker": "player", "text": "我需要一些装备，听说你能帮忙？"},
    {"speaker": "chenmo", "text": "......"},
    {"speaker": "chenmo", "text": "（他看了看自己的手）"},
    {"speaker": "chenmo", "text": "我打不了铁了。去找雷叔吧。"},
    {"speaker": "chenmo", "text": "铁匠铺在村子西边。"}
  ],
  "choices": [
    {
      "text": "谢谢，我去找他",
      "trust_change": 2,
      "next_node": null
    }
  ]
}
```

---

## 📍 阶段 3：友好（信任 41-60）

### 解锁新对话选项

**触发条件：** 信任值 41-60

```json
{
  "node_id": "chenmo_trust_41",
  "speaker": "chenmo",
  "lines": [
    {"speaker": "chenmo", "text": "（看到你，他点了点头）"},
    {"speaker": "chenmo", "text": "...最近还好吗？"}
  ],
  "choices": [
    {
      "text": "提及'逃兵'话题",
      "trust_change": -10,
      "next_node": "chenmo_deserter_topic"
    },
    {
      "text": "询问小安的情况",
      "trust_change": 8,
      "next_node": "chenmo_ask_xiaoan"
    },
    {
      "text": "邀请他加入队伍",
      "trust_change": 5,
      "next_node": "chenmo_invite_join"
    }
  ]
}
```

### 分支 1：提及"逃兵"话题（危险）

```json
{
  "node_id": "chenmo_deserter_topic",
  "speaker": "chenmo",
  "lines": [
    {"speaker": "player", "text": "我听说...你曾经是逃兵？"},
    {"speaker": "chenmo", "text": "（脸色瞬间阴沉）"},
    {"speaker": "chenmo", "text": "......谁告诉你的？"},
    {"speaker": "chenmo", "text": "（转身要走）别再来找我。"}
  ],
  "choices": [
    {
      "text": "对不起，我不该说",
      "trust_change": -5,
      "next_node": null
    }
  ],
  "trust_threshold": "若信任<50，后续对话锁定 3 天"
}
```

### 分支 2：询问小安的情况

```json
{
  "node_id": "chenmo_ask_xiaoan",
  "speaker": "chenmo",
  "lines": [
    {"speaker": "player", "text": "小安那孩子...最近怎么样？"},
    {"speaker": "chenmo", "text": "（眼神柔和了一瞬）"},
    {"speaker": "chenmo", "text": "...他很好。很聪明。"},
    {"speaker": "chenmo", "text": "（轻声）他父亲...会为他骄傲的。"}
  ],
  "choices": [
    {
      "text": "你很像他的父亲",
      "trust_change": 10,
      "next_node": "chenmo_father_figure"
    },
    {
      "text": "他父亲是谁？",
      "trust_change": -3,
      "next_node": "chenmo_father_identity"
    }
  ]
}
```

---

## 📍 阶段 4：信任（信任 61-80）

### 解锁新对话选项

**触发条件：** 信任值 61-80

```json
{
  "node_id": "chenmo_trust_61",
  "speaker": "chenmo",
  "lines": [
    {"speaker": "chenmo", "text": "（看到你，他露出罕见的笑容）"},
    {"speaker": "chenmo", "text": "...坐吧。有些事，我想告诉你。"}
  ],
  "choices": [
    {
      "text": "坦白知道他的秘密",
      "trust_change": 15,
      "next_node": "chenmo_confess_secret"
    },
    {
      "text": "询问队长的事",
      "trust_change": 10,
      "next_node": "chenmo_captain_story"
    },
    {
      "text": "请求并肩作战",
      "trust_change": 12,
      "next_node": "chenmo_fight_together"
    }
  ]
}
```

### 分支 1：坦白知道他的秘密 🔓 秘密解锁

```json
{
  "node_id": "chenmo_confess_secret",
  "speaker": "chenmo",
  "lines": [
    {"speaker": "player", "text": "陈默...我知道你的秘密。"},
    {"speaker": "chenmo", "text": "（身体僵硬）...你知道什么？"},
    {"speaker": "player", "text": "小安是队长的孩子，对吗？"},
    {"speaker": "chenmo", "text": "（长久沉默）"},
    {"speaker": "chenmo", "text": "...你是什么时候发现的？"},
    {"speaker": "chenmo", "text": "（苦笑）我藏了这么多年..."},
    {"speaker": "chenmo", "text": "（看着你）听着。小安...他不需要知道真相。"},
    {"speaker": "chenmo", "text": "他父亲是英雄。而我...只是个逃兵。"},
    {"speaker": "chenmo", "text": "（眼神坚定）但如果战火燃起..."},
    {"speaker": "chenmo", "text": "这一次，我不会再逃。"}
  ],
  "choices": [
    {
      "text": "你不是逃兵，你是守护者",
      "trust_change": 20,
      "next_node": null,
      "secret_unlocked": "chenmo_secret"
    }
  ],
  "trust_unlock": 80
}
```

### 分支 2：询问队长的事

```json
{
  "node_id": "chenmo_captain_story",
  "speaker": "chenmo",
  "lines": [
    {"speaker": "player", "text": "能告诉我...队长的故事吗？"},
    {"speaker": "chenmo", "text": "（沉默良久）"},
    {"speaker": "chenmo", "text": "...他是个傻瓜。"},
    {"speaker": "chenmo", "text": "明明可以撤退，却选择掩护我们。"},
    {"speaker": "chenmo", "text": "（声音颤抖）他说'活下去，保护小安'。"},
    {"speaker": "chenmo", "text": "可我...连自己都保护不了。"},
    {"speaker": "chenmo", "text": "（看着你）你能理解吗？活着的...比死去的更痛苦。"}
  ],
  "choices": [
    {
      "text": "活着才有机会赎罪",
      "trust_change": 10,
      "next_node": null
    },
    {
      "text": "队长不会希望你这样",
      "trust_change": 15,
      "next_node": null
    }
  ]
}
```

---

## 🎯 最终章对话（第 9-10 日）

### 决战前对话

**触发条件：** 第 9 日，信任值≥70

```json
{
  "node_id": "chenmo_final_day9",
  "speaker": "chenmo",
  "lines": [
    {"speaker": "chenmo", "text": "（他正在擦拭一把旧剑）"},
    {"speaker": "chenmo", "text": "明天...魔王军就会抵达。"},
    {"speaker": "chenmo", "text": "（抬头看你）你做好选择了吗？"},
    {"speaker": "player", "text": "你呢？"},
    {"speaker": "chenmo", "text": "（微笑）我逃过一次。"},
    {"speaker": "chenmo", "text": "这一次...（握紧剑柄）我不会再逃。"},
    {"speaker": "chenmo", "text": "小安需要看到一个...值得尊敬的成年人。"},
    {"speaker": "chenmo", "text": "（站起身）明天，并肩作战吧。"}
  ],
  "choices": [
    {
      "text": "并肩作战",
      "trust_change": 10,
      "next_node": null,
      "ally_joined": true
    }
  ]
}
```

---

## 💡 LLM 动态生成规则

### 固定文本 vs LLM 生成

| 对话类型 | 模式 | 说明 |
|----------|------|------|
| 关键剧情节点 | 固定文本 | 秘密解锁、最终章等核心剧情 |
| 日常对话 | LLM 生成 | 根据人格卡动态生成 |
| 信任值变化对话 | 混合 | 框架固定，细节 LLM 填充 |

### LLM 生成提示词

```
你扮演陈默，暮色村的"万能工"。

【当前状态】
- 信任值：{trust_value}
- 信任等级：{trust_level}
- 游戏日期：{current_day}
- 已知秘密：{known_secrets}

【说话风格】
- 沉默寡言，话少但有力
- 避免眼神接触（低信任时）
- 提及过去时会停顿/沉默
- 对小安话题格外温柔

【对话历史】
{dialogue_history}

【当前情境】
{current_context}

请根据以上信息生成陈默的回应，保持角色一致性。
关键剧情节点请使用固定文本（见对话树文档）。
```

---

*文档创建：2026-03-20*
*AliceCoder · 对话树系列*
