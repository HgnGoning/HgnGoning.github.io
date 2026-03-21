# main_got.py

from got_agent import GoTAgent
from models import Siliconflow, DashscopeModel
import os

# --- 你的 API Keys ---
DashscopeModel_API_KEY = "sk-c332af48e63a4c5a8e16671475399228"
# --------------------

def main():
    print("--- 初始化 GoT Agent ---")
    try:
        # GoT Agent 只需要一个“大脑”
        model = DashscopeModel(DashscopeModel_API_KEY)
        agent = GoTAgent(model=model)
        print("GoT Agent 初始化成功。")
    except Exception as e:
        print(f"Agent 初始化失败: {e}")
        return

    print("\n" + "="*50 + "\n")
    
    query = "深入分析一下‘远程工作’的利弊，并给求职者提出一些实用建议。"
    print(f"--- 开始处理复杂问题: '{query}' ---")
    
    final_answer = agent.run(query)
    
    print("\n" + "="*50)
    print("【GoT Agent 的最终答案】:")
    print(final_answer)

if __name__ == "__main__":
    main()
