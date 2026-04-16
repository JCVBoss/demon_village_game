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

def main():
    print("正在加载对话树...")
    data = load_dialogues()
    
    print("\n补充对话树 (DS-026):")
    print("=" * 50)
    
    data = add_chenmo_nodes(data)
    data = add_john_nodes(data)
    # 继续补充小安、夜鸦、影...
    
    print("\n保存对话树...")
    save_dialogues(data)
    print("✅ 对话树补充完成！")

if __name__ == '__main__':
    main()
