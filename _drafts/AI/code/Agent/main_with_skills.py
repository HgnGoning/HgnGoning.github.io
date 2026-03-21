# main_with_skills.py

# 注意，我们现在导入的是 SkillBasedAgent
from agent_with_skills import SkillBasedAgent
import os

# --- 你的 API Keys ---
SERPER_API_KEY = "9f48397378341b480763b6081b3711007c884c88"
DashscopeModel_API_KEY = "sk-c332af48e63a4c5a8e16671475399228"
# --------------------

def main():
    print("--- 初始化技能型 Agent ---")
    try:
        # 确保实例化的是新的 Agent 类
        agent = SkillBasedAgent(
            dashscope_api_key=DashscopeModel_API_KEY,
            serper_api_key=SERPER_API_KEY
        )
    except Exception as e:
        print(f"Agent 初始化失败: {e}")
        return

    print("\n" + "="*50 + "\n")
    
    print("--- 测试 1: 触发研究技能 ---")
    query_research = "帮我深入研究一下“大型语言模型中的上下文长度（Context Length）”这个概念，包括它的定义、重要性以及目前有哪些突破性技术。"
    response = agent.run(query_research, verbose=True)
    
    print("\n" + "="*50)
    print("【最终研究报告】:")
    print(response)

    print("\n" + "="*80 + "\n")

    print("--- 测试 2: 不触发任何技能 ---")
    query_chat = "你好，今天天气怎么样？"
    response_chat = agent.run(query_chat, verbose=True)

    print("\n" + "="*50)
    print("【直接回答】:")
    print(response_chat)


if __name__ == "__main__":
    main()
