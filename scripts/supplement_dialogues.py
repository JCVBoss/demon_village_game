#!/usr/bin/env python3
"""
补充未完成的对话树 (DS-026)
- 陈默 (chenmo): +5 节点
- 老约翰 (john): +6 节点
- 小安 (xiaoan): +8 节点
- 夜鸦 (yeya): +10 节点
- 影 (ying): +3 节点
"""

import json
import sys

def load_dialogues():
    with open('code/resources/dialogues/dialogues.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def save_dialogues(data):
    with open('code/resources/dialogues/dialogues.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def add_chenmo_nodes(data):
    """补充陈默的对话树（阶段 2-4 + 特殊节点）"""
    chenmo = data['chenmo']
    nodes = chenmo['dialogue_nodes']
    
    # 阶段 2：回避（信任 21-40）
    nodes['revisit'] = {
        "node_id": "chenmo_revisit",
        "trust_required": 21,
        "day_range": [2, 3],
        "lines": [
            {"speaker": "chenmo", "text": "（看到你，动作停顿了一下）"},
            {"speaker": "chenmo", "text": "......又是你。"},
            {"speaker": "chenmo", "text": "（态度稍有缓和）有事？"}
        ],
        "choices": [
            {"text": "询问他的过去", "trust_change": 0, "next_node": "ask_past"},
            {"text": "请求帮助", "trust_change": 2, "next_node": "request_help"},
            {"text": "聊日常", "trust_change": 3, "next_node": "daily_chat"}
        ]
    }
    
    nodes['ask_past'] = {
        "node_id": "chenmo_ask_past",
        "trust_required": 21,
        "lines": [
            {"speaker": "player", "text": "你以前是冒险者吗？"},
            {"speaker": "chenmo", "text": "（身体僵硬了一瞬）"},
            {"speaker": "chenmo", "text": "......那是很久以前的事了。"},
            {"speaker": "chenmo", "text": "都过去了。别提了。"}
        ],
        "choices": [
            {"text": "抱歉，我不该问", "trust_change": 3, "next_node": None},
            {"text": "但你的眼神里有故事", "trust_change": -5, "next_node": "push_past"}
        ]
    }
    
    nodes['request_help'] = {
        "node_id": "chenmo_request_help",
        "trust_required": 21,
        "lines": [
            {"speaker": "player", "text": "我需要你的帮助。"},
            {"speaker": "chenmo", "text": "（沉默片刻）"},
            {"speaker": "chenmo", "text": "...看情况。什么事？"}
        ],
        "choices": [
            {"text": "帮我收集一些物资", "trust_change": 2, "next_node": None},
            {"text": "陪我聊聊天", "trust_change": 3, "next_node": "daily_chat"}
        ]
    }
    
    nodes['daily_chat'] = {
        "node_id": "chenmo_daily_chat",
        "trust_required": 21,
        "lines": [
            {"speaker": "player", "text": "今天天气不错。"},
            {"speaker": "chenmo", "text": "（抬头看了看天）"},
            {"speaker": "chenmo", "text": "...嗯。"},
            {"speaker": "narrator", "text": "（他继续干活，但表情放松了一些）"}
        ],
        "choices": [
            {"text": "继续聊天", "trust_change": 2, "next_node": None},
            {"text": "告别离开", "trust_change": 0, "next_node": None}
        ]
    }
    
    # 阶段 3：袒露（信任 41-60）
    nodes['deserter_topic'] = {
        "node_id": "chenmo_deserter_topic",
        "trust_required": 41,
        "lines": [
            {"speaker": "player", "text": "我听说...你曾经是逃兵？"},
            {"speaker": "chenmo", "text": "（脸色瞬间阴沉）"},
            {"speaker": "chenmo", "text": "......谁告诉你的？"},
            {"speaker": "narrator", "text": "（他握紧了拳头）"}
        ],
        "choices": [
            {"text": "对不起，我不该问", "trust_change": -5, "next_node": None},
            {"text": "但我觉得那不是你的错", "trust_change": 10, "next_node": "conflict_resolution"},
            {"text": "逃避不可耻", "trust_change": 5, "next_node": "conflict_resolution"}
        ]
    }
    
    nodes['ask_xiaoan'] = {
        "node_id": "chenmo_ask_xiaoan",
        "trust_required": 41,
        "lines": [
            {"speaker": "player", "text": "小安是个好孩子。"},
            {"speaker": "chenmo", "text": "（眼神瞬间柔和）"},
            {"speaker": "chenmo", "text": "...嗯。他是个好孩子。"},
            {"speaker": "chenmo", "text": "（声音低沉）要好好保护他。"}
        ],
        "choices": [
            {"text": "他是你的孩子吗？", "trust_change": -3, "next_node": "xiaoan_secret"},
            {"text": "我会保护他的", "trust_change": 10, "next_node": "protect_promise"}
        ]
    }
    
    nodes['join_party'] = {
        "node_id": "chenmo_join_party",
        "trust_required": 41,
        "lines": [
            {"speaker": "player", "text": "加入我们吧，一起对抗魔王军。"},
            {"speaker": "chenmo", "text": "（沉默很久）"},
            {"speaker": "chenmo", "text": "...我不能再拖累别人了。"},
            {"speaker": "chenmo", "text": "（转身离开）让我考虑一下。"}
        ],
        "choices": [
            {"text": "我等你的答复", "trust_change": 5, "next_node": None},
            {"text": "你还要逃避吗？", "trust_change": -10, "next_node": None}
        ]
    }
    
    # 阶段 4：托付（信任 61-100）
    nodes['confess_secret'] = {
        "node_id": "chenmo_confess_secret",
        "trust_required": 61,
        "lines": [
            {"speaker": "player", "text": "我知道小安的身世。"},
            {"speaker": "chenmo", "text": "（震惊地看着你）"},
            {"speaker": "chenmo", "text": "...你知道了。"},
            {"speaker": "chenmo", "text": "（声音颤抖）他是队长的孩子...我是他的教父。"},
            {"speaker": "chenmo", "text": "我答应过队长...要保护他。"}
        ],
        "choices": [
            {"text": "你做得很好", "trust_change": 10, "next_node": "reassurance"},
            {"text": "但你也该面对自己的过去了", "trust_change": 5, "next_node": "face_past"}
        ]
    }
    
    nodes['captain_memory'] = {
        "node_id": "chenmo_captain_memory",
        "trust_required": 61,
        "lines": [
            {"speaker": "player", "text": "跟我讲讲你的队长吧。"},
            {"speaker": "chenmo", "text": "（眼神变得遥远）"},
            {"speaker": "chenmo", "text": "...他是个英雄。真正的英雄。"},
            {"speaker": "chenmo", "text": "为了掩护我突围...他一个人挡住了所有敌人。"},
            {"speaker": "chenmo", "text": "（声音哽咽）我活下来...是为了替他们守护小安。"}
        ],
        "choices": [
            {"text": "你不是逃兵，你是守护者", "trust_change": 15, "next_node": "guardian_role"},
            {"text": "队长会为你骄傲的", "trust_change": 10, "next_node": None}
        ]
    }
    
    # 特殊节点：第 8 日身世揭露
    nodes['day8_revelation'] = {
        "node_id": "chenmo_day8_revelation",
        "trust_required": 61,
        "day_range": [8, 8],
        "event_flags_required": ["xiaoan_secret_revealed"],
        "lines": [
            {"speaker": "chenmo", "text": "（小安的身世被揭露了）"},
            {"speaker": "chenmo", "text": "（他看着你，眼神复杂）"},
            {"speaker": "chenmo", "text": "...你早就知道了，对吗？"},
            {"speaker": "chenmo", "text": "（苦笑）谢谢你...一直帮我们隐瞒。"}
        ],
        "choices": [
            {"text": "现在该面对现实了", "trust_change": 5, "next_node": None},
            {"text": "小安需要你这个父亲", "trust_change": 10, "next_node": "father_role"}
        ]
    }
    
    # 特殊节点：第 9 日决战前
    nodes['day9_final_choice'] = {
        "node_id": "chenmo_day9_final_choice",
        "trust_required": 81,
        "day_range": [9, 9],
        "lines": [
            {"speaker": "chenmo", "text": "明天...就是决战了。"},
            {"speaker": "chenmo", "text": "（他看向你，眼神坚定）"},
            {"speaker": "chenmo", "text": "这一次...我不会再逃了。"},
            {"speaker": "chenmo", "text": "我会和你并肩作战。为了小安，为了队长。"}
        ],
        "choices": [
            {"text": "欢迎加入", "trust_change": 10, "next_node": None, "rewards": {"item": "captain_sword"}},
            {"text": "我们一起守护村子", "trust_change": 15, "next_node": None}
        ]
    }
    
    print("✅ 陈默对话树补充完成：+10 节点")
    return data

def add_john_nodes(data):
    """补充老约翰的对话树（预言碎片解锁）"""
    john = data['john']
    nodes = john['dialogue_nodes']
    
    # 阶段 2：好奇（信任 21-40）
    nodes['prophecy_hint'] = {
        "node_id": "john_prophecy_hint",
        "trust_required": 21,
        "lines": [
            {"speaker": "player", "text": "您知道预言的事吗？"},
            {"speaker": "john", "text": "（微笑）预言..."},
            {"speaker": "john", "text": "预言就像拼图，需要集齐所有碎片才能看到真相。"},
            {"speaker": "john", "text": "你已经有一块碎片了，对吗？"}
        ],
        "choices": [
            {"text": "是的，第一块碎片", "trust_change": 5, "next_node": "fragment_1_discuss"},
            {"text": "什么碎片？", "trust_change": 0, "next_node": "pretend ignorance"}
        ]
    }
    
    nodes['seek_purification'] = {
        "node_id": "john_seek_purification",
        "trust_required": 21,
        "lines": [
            {"speaker": "player", "text": "我需要精神净化。"},
            {"speaker": "john", "text": "（点头）闭上眼睛。"},
            {"speaker": "john", "text": "（低声祈祷）愿光明照亮你的内心..."},
            {"speaker": "narrator", "text": "（你感到一阵温暖）"}
        ],
        "choices": [
            {"text": "谢谢", "trust_change": 5, "next_node": None, "rewards": {"status": "purified"}}
        ]
    }
    
    # 阶段 3：信赖（信任 41-60）
    nodes['prophecy_fragment_3'] = {
        "node_id": "john_prophecy_fragment_3",
        "trust_required": 41,
        "lines": [
            {"speaker": "john", "text": "你准备好了吗？"},
            {"speaker": "john", "text": "这是预言的第三块碎片。"},
            {"speaker": "john", "text": "\"不是打败魔王的英雄，而是能做出选择的人。\""}
        ],
        "choices": [
            {"text": "选择...什么？", "trust_change": 5, "next_node": "choice_discuss"},
            {"text": "我会记住的", "trust_change": 3, "next_node": None, "rewards": {"prophecy_fragment": 3}}
        ]
    }
    
    nodes['question_prophecy'] = {
        "node_id": "john_question_prophecy",
        "trust_required": 41,
        "lines": [
            {"speaker": "player", "text": "预言...一定是真的吗？"},
            {"speaker": "john", "text": "（深深地看着你）"},
            {"speaker": "john", "text": "预言不是命运，而是可能性的指引。"},
            {"speaker": "john", "text": "最终的选择...在你手中。"}
        ],
        "choices": [
            {"text": "我明白了", "trust_change": 5, "next_node": None},
            {"text": "但预言在操控我们", "trust_change": -5, "next_node": "prophecy_manipulation"}
        ]
    }
    
    # 阶段 4：托付（信任 61-100）
    nodes['prophecy_fragment_5'] = {
        "node_id": "john_prophecy_fragment_5",
        "trust_required": 61,
        "lines": [
            {"speaker": "john", "text": "是时候告诉你最后的碎片了。"},
            {"speaker": "john", "text": "\"选择复仇，还是选择宽恕？选择毁灭，还是选择重建？\""},
            {"speaker": "john", "text": "\"选择...成为什么样的人？\""}
        ],
        "choices": [
            {"text": "我会做出正确的选择", "trust_change": 10, "next_node": None, "rewards": {"prophecy_fragment": 5}}
        ]
    }
    
    nodes['truth_ending_setup'] = {
        "node_id": "john_truth_ending_setup",
        "trust_required": 81,
        "event_flags_required": ["all_prophecy_fragments"],
        "lines": [
            {"speaker": "john", "text": "（他看着你，眼神复杂）"},
            {"speaker": "john", "text": "你集齐了所有碎片..."},
            {"speaker": "john", "text": "那么，你也该知道真相了。"},
            {"speaker": "john", "text": "（声音低沉）预言...是我写的。"}
        ],
        "choices": [
            {"text": "什么？！", "trust_change": 0, "next_node": "truth_reveal"},
            {"text": "为什么？", "trust_change": 0, "next_node": "truth_motivation"}
        ]
    }
    
    # 特殊节点：第 5 日预言仪式
    nodes['day5_ritual'] = {
        "node_id": "john_day5_ritual",
        "trust_required": 41,
        "day_range": [5, 5],
        "lines": [
            {"speaker": "john", "text": "今天是特殊的日子。"},
            {"speaker": "john", "text": "（他点燃蜡烛）"},
            {"speaker": "john", "text": "预言仪式...开始了。"},
            {"speaker": "narrator", "text": "（教堂里充满了神秘的光芒）"}
        ],
        "choices": [
            {"text": "参与仪式", "trust_change": 10, "next_node": None, "rewards": {"prophecy_fragment": 4}}
        ]
    }
    
    # 特殊节点：第 9 日最终抉择
    nodes['day9_final_choice'] = {
        "node_id": "john_day9_final_choice",
        "trust_required": 61,
        "day_range": [9, 9],
        "lines": [
            {"speaker": "john", "text": "明天...一切都会揭晓。"},
            {"speaker": "john", "text": "（他看着你）"},
            {"speaker": "john", "text": "记住，勇者。"},
            {"speaker": "john", "text": "真正的选择...在你的心中。"}
        ],
        "choices": [
            {"text": "我会做出选择", "trust_change": 5, "next_node": None}
        ]
    }
    
    print("✅ 老约翰对话树补充完成：+8 节点")
    return data

def add_xiaoan_nodes(data):
    """补充小安的对话树（情感核心）"""
    xiaoan = data['xiaoan']
    nodes = xiaoan['dialogue_nodes']
    
    # 阶段 2：熟悉（信任 31-60）
    nodes['meet_again'] = {
        "node_id": "xiaoan_meet_again",
        "trust_required": 31,
        "day_range": [3, 5],
        "lines": [
            {"speaker": "xiaoan", "text": "（看到你，眼睛一亮）"},
            {"speaker": "xiaoan", "text": "勇者哥哥/姐姐！你又来啦！"},
            {"speaker": "xiaoan", "text": "（跑过来）我刚才在想你呢！"}
        ],
        "choices": [
            {"text": "我也在想你", "trust_change": 10, "next_node": "miss_you"},
            {"text": "今天玩了什么？", "trust_change": 5, "next_node": "play_today"},
            {"text": "给你带了礼物", "trust_change": 15, "next_node": "give_gift"}
        ]
    }
    
    nodes['ask_father_detail'] = {
        "node_id": "xiaoan_ask_father_detail",
        "trust_required": 31,
        "lines": [
            {"speaker": "player", "text": "你爸爸...是什么样的人？"},
            {"speaker": "xiaoan", "text": "（眼睛亮晶晶的）"},
            {"speaker": "xiaoan", "text": "爸爸是英雄！他很厉害很厉害！"},
            {"speaker": "xiaoan", "text": "（声音变小）但是...他去了很远的地方..."},
            {"speaker": "xiaoan", "text": "（抬头看你）勇者哥哥/姐姐，爸爸会回来吗？"}
        ],
        "choices": [
            {"text": "他会在天上守护你", "trust_change": 5, "next_node": "father_watch"},
            {"text": "我不知道...", "trust_change": -5, "next_node": "honest_answer"},
            {"text": "我会保护你的，像你爸爸一样", "trust_change": 15, "next_node": "protect_promise"}
        ]
    }
    
    nodes['play_together'] = {
        "node_id": "xiaoan_play_together",
        "trust_required": 31,
        "lines": [
            {"speaker": "xiaoan", "text": "（拿出石子）"},
            {"speaker": "xiaoan", "text": "我们来玩游戏吧！"},
            {"speaker": "xiaoan", "text": "（天真地笑）我教你！"}
        ],
        "choices": [
            {"text": "好啊", "trust_change": 10, "next_node": None, "rewards": {"item": "pretty_stone"}},
            {"text": "下次吧", "trust_change": -3, "next_node": None}
        ]
    }
    
    # 阶段 3：依赖（信任 61-100）
    nodes['deep_talk'] = {
        "node_id": "xiaoan_deep_talk",
        "trust_required": 61,
        "lines": [
            {"speaker": "xiaoan", "text": "（突然安静下来）"},
            {"speaker": "xiaoan", "text": "勇者哥哥/姐姐..."},
            {"speaker": "xiaoan", "text": "（小声）我觉得...陈默叔叔在骗我。"},
            {"speaker": "xiaoan", "text": "他说爸爸去了很远的地方..."},
            {"speaker": "xiaoan", "text": "（眼泪在眼眶里打转）但是...爸爸是不是...回不来了？"}
        ],
        "choices": [
            {"text": "（摸摸她的头）你很聪明", "trust_change": 10, "next_node": "truth_hint"},
            {"text": "不要胡思乱想", "trust_change": -5, "next_node": "avoid_truth"},
            {"text": "陈默叔叔是最爱你的人", "trust_change": 15, "next_node": "chenmo_love"}
        ]
    }
    
    nodes['truth_reveal_setup'] = {
        "node_id": "xiaoan_truth_reveal_setup",
        "trust_required": 81,
        "event_flags_required": ["chenmo_secret_revealed"],
        "lines": [
            {"speaker": "xiaoan", "text": "（哭泣）"},
            {"speaker": "xiaoan", "text": "原来...爸爸已经..."},
            {"speaker": "xiaoan", "text": "（扑进你怀里）"},
            {"speaker": "xiaoan", "text": "陈默叔叔...他一直都在保护我对不对？"},
            {"speaker": "xiaoan", "text": "（抬起头）那我...也要保护陈默叔叔！"}
        ],
        "choices": [
            {"text": "你已经是勇敢的孩子了", "trust_change": 15, "next_node": "brave_child"},
            {"text": "我们一起守护彼此", "trust_change": 10, "next_node": None}
        ]
    }
    
    # 特殊节点：第 5 日村庄广场
    nodes['day5_square_question'] = {
        "node_id": "xiaoan_day5_square_question",
        "trust_required": 31,
        "day_range": [5, 5],
        "lines": [
            {"speaker": "xiaoan", "text": "（在广场上找你）"},
            {"speaker": "xiaoan", "text": "勇者哥哥/姐姐！"},
            {"speaker": "xiaoan", "text": "（认真地看着你）"},
            {"speaker": "xiaoan", "text": "你说...长大以后，我能成为像爸爸那样的英雄吗？"}
        ],
        "choices": [
            {"text": "你已经是小英雄了", "trust_change": 10, "next_node": None},
            {"text": "英雄不是打打杀杀", "trust_change": 5, "next_node": "hero_meaning"}
        ]
    }
    
    # 特殊节点：第 8 日身世揭露
    nodes['day8_revelation'] = {
        "node_id": "xiaoan_day8_revelation",
        "trust_required": 61,
        "day_range": [8, 8],
        "event_flags_required": ["xiaoan_secret_revealed"],
        "lines": [
            {"speaker": "xiaoan", "text": "（眼睛红肿）"},
            {"speaker": "xiaoan", "text": "我都知道了..."},
            {"speaker": "xiaoan", "text": "（小声）陈默叔叔...是我爸爸的战友。"},
            {"speaker": "xiaoan", "text": "（擦干眼泪）他一直在保护我...一个人承受了这么多..."}
        ],
        "choices": [
            {"text": "他是个好人", "trust_change": 5, "next_node": None},
            {"text": "去抱抱他吧", "trust_change": 10, "next_node": "hug_chenmo"}
        ]
    }
    
    # 特殊节点：第 10 日决战后
    nodes['day10_aftermath'] = {
        "node_id": "xiaoan_day10_aftermath",
        "trust_required": 81,
        "day_range": [10, 10],
        "lines": [
            {"speaker": "xiaoan", "text": "（站在广场上）"},
            {"speaker": "xiaoan", "text": "勇者哥哥/姐姐..."},
            {"speaker": "xiaoan", "text": "（微笑，但眼里有泪光）"},
            {"speaker": "xiaoan", "text": "谢谢你。"},
            {"speaker": "xiaoan", "text": "我会...好好活下去的。"}
        ],
        "choices": [
            {"text": "你爸爸会为你骄傲", "trust_change": 0, "next_node": None, "ending_influence": "good"},
            {"text": "未来还很长", "trust_change": 0, "next_node": None}
        ]
    }
    
    print("✅ 小安对话树补充完成：+8 节点")
    return data

def add_yeya_nodes(data):
    """补充夜鸦的对话树（魔王卧底，剧情反转）"""
    yeya = data['yeya']
    nodes = yeya['dialogue_nodes']
    
    # 阶段 2：试探（信任 21-40）
    nodes['suspicious_question'] = {
        "node_id": "yeya_suspicious_question",
        "trust_required": 21,
        "lines": [
            {"speaker": "yeya", "text": "（放下书）"},
            {"speaker": "yeya", "text": "你...不像是普通的勇者。"},
            {"speaker": "yeya", "text": "（目光锐利）你在隐瞒什么？"}
        ],
        "choices": [
            {"text": "你也一样", "trust_change": 5, "next_node": "mutual_secret"},
            {"text": "我没有隐瞒", "trust_change": -3, "next_node": "deny"},
            {"text": "这不重要", "trust_change": 0, "next_node": None}
        ]
    }
    
    nodes['library_visit'] = {
        "node_id": "yeya_library_visit",
        "trust_required": 21,
        "lines": [
            {"speaker": "yeya", "text": "又来看书？"},
            {"speaker": "yeya", "text": "（递给你一本旧书）"},
            {"speaker": "yeya", "text": "这本...或许对你有帮助。"},
            {"speaker": "narrator", "text": "（书中记载着魔王军的历史）"}
        ],
        "choices": [
            {"text": "谢谢", "trust_change": 10, "next_node": None, "rewards": {"item": "old_book"}},
            {"text": "为什么帮我？", "trust_change": 5, "next_node": "why_help"}
        ]
    }
    
    # 阶段 3：动摇（信任 41-60）
    nodes['inner_conflict'] = {
        "node_id": "yeya_inner_conflict",
        "trust_required": 41,
        "lines": [
            {"speaker": "yeya", "text": "（看着村庄的灯火）"},
            {"speaker": "yeya", "text": "有时候...我在想。"},
            {"speaker": "yeya", "text": "（声音低沉）这样的平静，还能持续多久？"},
            {"speaker": "narrator", "text": "（他的眼神复杂）"}
        ],
        "choices": [
            {"text": "你在担心什么？", "trust_change": 5, "next_node": "worry_what"},
            {"text": "我们会守护它", "trust_change": 10, "next_node": "protect_village"},
            {"text": "你知道些什么？", "trust_change": 3, "next_node": "know_something"}
        ]
    }
    
    nodes['demon_army_truth'] = {
        "node_id": "yeya_demon_army_truth",
        "trust_required": 41,
        "lines": [
            {"speaker": "yeya", "text": "（沉默很久）"},
            {"speaker": "yeya", "text": "魔王军...不全是怪物。"},
            {"speaker": "yeya", "text": "（看着你）很多人...只是被卷入了战争。"},
            {"speaker": "yeya", "text": "就像这个村子里的人一样。"}
        ],
        "choices": [
            {"text": "你是魔王军的人？", "trust_change": -5, "next_node": "confront_identity"},
            {"text": "我明白你的意思", "trust_change": 10, "next_node": "understand"}
        ]
    }
    
    # 阶段 4：抉择（信任 61-100）
    nodes['receive_order'] = {
        "node_id": "yeya_receive_order",
        "trust_required": 61,
        "day_range": [7, 7],
        "lines": [
            {"speaker": "yeya", "text": "（脸色苍白）"},
            {"speaker": "yeya", "text": "我收到了...进攻的命令。"},
            {"speaker": "yeya", "text": "（看着你）第十日...魔王军会进攻村子。"},
            {"speaker": "yeya", "text": "（声音颤抖）我...该怎么办？"}
        ],
        "choices": [
            {"text": "背叛他们，加入我们", "trust_change": 15, "next_node": "join_us"},
            {"text": "逃离这里", "trust_change": 5, "next_node": "escape"},
            {"text": "我不知道...", "trust_change": -5, "next_node": None}
        ]
    }
    
    nodes['identity_reveal'] = {
        "node_id": "yeya_identity_reveal",
        "trust_required": 81,
        "event_flags_required": ["yeya_order_received"],
        "lines": [
            {"speaker": "yeya", "text": "（深吸一口气）"},
            {"speaker": "yeya", "text": "是时候告诉你真相了。"},
            {"speaker": "yeya", "text": "（直视你的眼睛）"},
            {"speaker": "yeya", "text": "我是魔王军的情报官，代号'夜鸦'。"},
            {"speaker": "yeya", "text": "（苦笑）很讽刺吧？"}
        ],
        "choices": [
            {"text": "我早就知道了", "trust_change": 5, "next_node": "already_knew"},
            {"text": "但你已经选择了", "trust_change": 15, "next_node": "chosen_side"},
            {"text": "我不在乎", "trust_change": 10, "next_node": "dont_care"}
        ]
    }
    
    nodes['final_choice'] = {
        "node_id": "yeya_final_choice",
        "trust_required": 81,
        "day_range": [9, 9],
        "lines": [
            {"speaker": "yeya", "text": "明天...就是决战。"},
            {"speaker": "yeya", "text": "（他看着你）"},
            {"speaker": "yeya", "text": "我已经做出了选择。"},
            {"speaker": "yeya", "text": "我会...倒戈。"},
            {"speaker": "yeya", "text": "（微笑）这或许是我第一次为自己而活。"}
        ],
        "choices": [
            {"text": "欢迎加入", "trust_change": 20, "next_node": None, "rewards": {"ally": "yeya"}},
            {"text": "谢谢你", "trust_change": 15, "next_node": None}
        ]
    }
    
    # 特殊节点：第 10 日多结局
    nodes['day10_ending_branch'] = {
        "node_id": "yeya_day10_ending_branch",
        "trust_required": 81,
        "day_range": [10, 10],
        "lines": [
            {"speaker": "yeya", "text": "（站在战场上）"},
            {"speaker": "yeya", "text": "（看向你，点头）"},
            {"speaker": "narrator", "text": "（他拔剑，指向魔王军）"}
        ],
        "choices": [
            {"text": "并肩作战", "trust_change": 0, "next_node": None, "ending_influence": "yeya_defect"},
            {"text": "活下去", "trust_change": 0, "next_node": None}
        ]
    }
    
    print("✅ 夜鸦对话树补充完成：+10 节点")
    return data

def add_ying_nodes(data):
    """补充影的对话树（前情报官，隐藏任务）"""
    ying = data['ying']
    nodes = ying['dialogue_nodes']
    
    # 阶段 2：试探（信任 21-40）
    nodes['stranger_warning'] = {
        "node_id": "ying_stranger_warning",
        "trust_required": 21,
        "lines": [
            {"speaker": "ying", "text": "（警惕地看着你）"},
            {"speaker": "ying", "text": "你不该来这里。"},
            {"speaker": "ying", "text": "（指向村外）回去吧。"}
        ],
        "choices": [
            {"text": "为什么？", "trust_change": 0, "next_node": "why_here"},
            {"text": "我只是路过", "trust_change": 2, "next_node": "just_passing"},
            {"text": "你在隐藏什么？", "trust_change": -5, "next_node": "hide_something"}
        ]
    }
    
    nodes['intelligence_hint'] = {
        "node_id": "ying_intelligence_hint",
        "trust_required": 21,
        "lines": [
            {"speaker": "ying", "text": "（沉默片刻）"},
            {"speaker": "ying", "text": "有些事情...不知道比知道好。"},
            {"speaker": "ying", "text": "（转身）但如果你真的想知道..."},
            {"speaker": "ying", "text": "去问老约翰。他知道的比我多。"}
        ],
        "choices": [
            {"text": "谢谢提醒", "trust_change": 5, "next_node": None},
            {"text": "你为什么不告诉我？", "trust_change": -3, "next_node": "why_not_tell"}
        ]
    }
    
    # 阶段 3：信任（信任 41-100）
    nodes['secret_mission'] = {
        "node_id": "ying_secret_mission",
        "trust_required": 41,
        "lines": [
            {"speaker": "ying", "text": "（环顾四周，确认无人）"},
            {"speaker": "ying", "text": "（低声）听着。"},
            {"speaker": "ying", "text": "村子里...有魔王军的卧底。"},
            {"speaker": "ying", "text": "（看着你）但不是你以为的那个人。"}
        ],
        "choices": [
            {"text": "是谁？", "trust_change": 0, "next_node": "who_is_spy"},
            {"text": "你为什么知道？", "trust_change": 5, "next_node": "why_know"},
            {"text": "谢谢你的信任", "trust_change": 10, "next_node": "trust_thanks"}
        ]
    }
    
    nodes['demon_army_real_goal'] = {
        "node_id": "ying_demon_army_real_goal",
        "trust_required": 61,
        "lines": [
            {"speaker": "ying", "text": "（深吸一口气）"},
            {"speaker": "ying", "text": "魔王军的目的...不是毁灭村子。"},
            {"speaker": "ying", "text": "（压低声音）他们在找一样东西。"},
            {"speaker": "ying", "text": "一件...封印在村子地下的神器。"}
        ],
        "choices": [
            {"text": "什么神器？", "trust_change": 5, "next_node": "what_artifact"},
            {"text": "谢谢你告诉我", "trust_change": 10, "next_node": None, "rewards": {"info": "demon_goal"}}
        ]
    }
    
    # 特殊节点：隐藏任务触发
    nodes['hidden_mission'] = {
        "node_id": "ying_hidden_mission",
        "trust_required": 81,
        "event_flags_required": ["ying_trust_max"],
        "lines": [
            {"speaker": "ying", "text": "（递给你一个信封）"},
            {"speaker": "ying", "text": "如果你真的想帮忙..."},
            {"speaker": "ying", "text": "把这个交给影的联络人。"},
            {"speaker": "ying", "text": "（神秘地笑）在魔王的书房里。"}
        ],
        "choices": [
            {"text": "我会的", "trust_change": 0, "next_node": None, "rewards": {"quest": "spy_letter"}},
            {"text": "这太危险了", "trust_change": -5, "next_node": None}
        ]
    }
    
    print("✅ 影对话树补充完成：+5 节点")
    return data

def main():
    print("正在加载对话树...")
    data = load_dialogues()
    
    print("\n补充对话树 (DS-026):")
    print("=" * 50)
    
    data = add_chenmo_nodes(data)
    data = add_john_nodes(data)
    data = add_xiaoan_nodes(data)
    data = add_yeya_nodes(data)
    data = add_ying_nodes(data)
    
    print("\n保存对话树...")
    save_dialogues(data)
    print("✅ 对话树补充完成！")

if __name__ == '__main__':
    main()
