# 导入我们刚刚创建的 Agent
from agent_framework import ReactAgent
from tools import ReactTools

# --- 替换成你自己的 API Keys ---
SILICONFLOW_API_KEY = "sk-frfnmxuysboznagyubkzpnrojehqwpbcwfgvvwdqjsnfekak"
SERPER_API_KEY = "9f48397378341b480763b6081b3711007c884c88"
DashscopeModel_API_KEY = "sk-c332af48e63a4c5a8e16671475399228"
# ---------------------------------

def test_simple_query(agent: ReactAgent):
    """测试简单查询（无需工具）"""
    print("--- 2. 简单查询测试 (无需工具) ---")
    response_simple = agent.run("你好，请用中文做个自我介绍", use_plan=False, max_iterations=1, verbose=False)
    print(f"简单查询结果:\n{response_simple}")


def test_react_mode(agent: ReactAgent):
    """测试原始的 ReAct 模式"""
    print("\n" + "=" * 50 + "\n")
    print("--- 3. 复杂查询测试 (ReAct 模式) ---")
    query = "美国最近一次国庆阅兵是什么时候，主要原因有哪些？"
    # 使用 use_plan=False 来强制使用旧的 ReAct 模式
    response_complex = agent.run(query, use_plan=False, max_iterations=3, verbose=True)
    print("\n" + "=" * 50)
    print("ReAct 模式最终答案:")
    print(response_complex)


def test_plan_and_execute_mode(agent: ReactAgent):
    """测试新的“规划-执行”模式"""
    print("\n" + "=" * 50 + "\n")
    print("--- 4. 新架构测试: 规划-执行模式 ---")

    # 设计一个需要多步才能解决的复杂问题
    query = "请先搜索苹果公司（Apple Inc.）的创始人是谁，然后再搜索这位创始人的出生日期。"

    # use_plan=True (或者不写，因为它是默认值)
    response = agent.run(query, max_iterations=2, verbose=True)  # max_iterations 作用于每个子任务

    print("\n" + "=" * 50)
    print("“规划-执行”模式的最终答案:")
    print(response)


def test_reflection_mode(agent: ReactAgent):
    """测试“反思”模式"""
    print("\n" + "=" * 50 + "\n")
    print("--- 5. 新架构测试: 反思模式 ---")

    # 设计一个故意会出错的问题。
    # 我们不直接提供数学表达式，而是让模型自己去构造，它第一次很可能会构造错。
    # 比如，它可能会生成 "mcp_tool(100+200)"，这在我们的实现里会因为缺少引号而失败。
    query = "用 mcp_tool 计算 100 加 200 的和。"

    # 在这个场景下，我们使用原始的 ReAct 模式来更清晰地观察反思过程
    response = agent.run(query, use_plan=False, max_iterations=3, verbose=True)

    print("\n" + "=" * 50)
    print("“反思”模式的最终答案:")
    print(response)


def main():
    print("--- 1. Agent 初始化 ---")
    try:
        agent = ReactAgent(
            dashscope_api_key=DashscopeModel_API_KEY,
            serper_api_key=SERPER_API_KEY
        )
        print("Agent 初始化成功。")
    except Exception as e:
        print(f"Agent 初始化失败: {e}")
        return

    # --- 你可以选择运行所有测试，或者只注释掉不想运行的部分 ---

    # test_simple_query(agent)
    # test_react_mode(agent)
    test_plan_and_execute_mode(agent)
    test_reflection_mode(agent)

if __name__ == "__main__":
    main()
