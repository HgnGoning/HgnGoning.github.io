from typing import List, Dict
import time
import re
import json5  # 使用 json5 库来增强对不规范 JSON 的解析能力
import json
import os

# 导入我们自己创建的模块
from models import Siliconflow
from models import DashscopeModel
from tools import ReactTools

class ReactAgent:
    def __init__(self, dashscope_api_key: str, serper_api_key: str) -> None:
        """
        初始化 React Agent。
        Args:
            dashscope_api_key: 用于大模型的 API Key。
            siliconflow_api_key: 用于大模型的 API Key。
            serper_api_key: 用于 Google 搜索的 API Key。
        """
        self.tools = ReactTools(serper_api_key=serper_api_key)
        self.model = DashscopeModel(dashscope_api_key)
        self.system_prompt = self._build_system_prompt()
        self.planner_system_prompt = self._build_planner_system_prompt()
        self.log_dir = "agent_logs"
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
    
    def _build_system_prompt(self) -> str:
        """
        构建 ReAct 模式的系统提示。
        """
        # 获取格式化的工具描述
        tool_descriptions = self.tools.get_tool_description()
        # --- 重要的修改：让工具列表动态化 ---
        available_tools_names = ', '.join(self.tools.get_available_tools())
        
        # 这是 Agent 的“行为准则”
        prompt_template = f"""现在时间是 {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}。
            你是一位智能助手，可以使用以下工具来回答问题：
            
            {tool_descriptions}
            
            请严格遵循以下 ReAct 模式，一步一步地思考：
            
            思考：首先，分析用户的问题，判断是否需要使用工具。如果需要，思考应该使用哪个工具，以及如何组织工具的输入参数。如果不需要工具，就直接思考最终答案。
            行动：如果你在上一步决定要使用工具，请在这里指定工具名称。工具名称必须是 [{available_tools_names}] 中的一个。
            行动输入：提供在上一步中选择的工具所需的参数，格式为 JSON。
            观察：这是工具执行后返回的结果。你不需要填写这一步，系统会自动填充。
            
            ---
            在每一轮循环中，你都必须输出“思考”、“行动”和“行动输入”。
            如果你已经获得了足够的信息来回答用户的问题，请在“行动”部分填写 `最终答案`，然后在“行动输入”中直接给出最终的、完整的答案。
            ---
            
            开始！"""
        return prompt_template

    def _build_planner_system_prompt(self) -> str:
            """构建一个专门用于生成计划的系统提示。"""
            return """你是一位顶级的任务规划专家。你的任务是分析用户的复杂问题，并将其分解成一个有序的、可执行的步骤列表。
            每个步骤都应该是一个清晰、独立的子任务。
            请以JSON格式的列表输出你的计划，每个步骤包含 'step' 和 'task' 两个字段。
            例如：[{"step": 1, "task": "查询A的生日"}, {"step": 2, "task": "查询B的生日"}, {"step": 3, "task": "比较两个生日的早晚"}]
            """

    def _generate_plan(self, query: str, verbose: bool = True) -> List[Dict]:
            """为给定的查询生成一个分步计划。"""
            if verbose:
                print("[Planner] 正在为问题生成计划...")

            # 调用大模型，但使用 planner_system_prompt
            response, _ = self.model.chat(
                prompt=f"请为以下问题制定一个详细的行动计划：{query}",
                history=[],
                system_prompt=self.planner_system_prompt
            )

            if verbose:
                print(f"[Planner] 生成的计划:\n{response}")

            try:
                # 解析模型返回的JSON计划
                plan = json5.loads(response)
                if isinstance(plan, list):
                    return plan
                else:
                    return []
            except Exception:
                return []

    def _parse_action(self, text: str, verbose: bool = False) -> tuple[str, dict]:
        """
        从模型返回的文本中解析出“行动”和“行动输入”。
        """
        # 正则表达式，用于匹配“行动”和“行动输入”
        action_pattern = r"行动[:：]\s*(\w+)"
        action_input_pattern = r"行动输入[:：]\s*({.*?}|[^\n]*)" # 匹配 JSON 或单行文本
        
        action_match = re.search(action_pattern, text, re.IGNORECASE)
        action_input_match = re.search(action_input_pattern, text, re.DOTALL) # DOTALL 允许 . 匹配换行符
        
        action = action_match.group(1).strip() if action_match else ""
        action_input_str = action_input_match.group(1).strip() if action_input_match else ""

        if verbose:
            print(f"DEBUG: Parsed Action: {action}")
            print(f"DEBUG: Parsed Action Input String: '{action_input_str}'")
        
        action_input_dict = {}
        if action_input_str:
            try:
                # 优先尝试使用 json5 解析，它对格式要求更宽松
                action_input_dict = json5.loads(action_input_str)
            except Exception:
                # 如果解析失败，把它当作一个简单的字符串参数处理
                # 这主要为了兼容模型可能直接返回 `特朗普生日` 而不是 `{"search_query": "特朗普生日"}` 的情况
                action_input_dict = {"search_query": action_input_str.strip('"\' ')}

        return action, action_input_dict
    
    def _execute_action(self, action: str, action_input: dict) -> str:
        """
        根据行动名称，调用对应的工具函数。
        """
        if action == "google_search":
            # 从参数字典中获取 search_query
            query = action_input.get("search_query", "")
            if query:
                return self.tools.google_search(query)
            else:
                return "错误：google_search 需要 'search_query' 参数。"
        elif action == "mcp_tool":
            expression = action_input.get("expression", "")
            if expression:
                return self.tools.mcp_tool(expression)
            else:
                return "错误：mcp_tool 需要 'expression' 参数。"
        else:
            return f"错误：未知的行动 '{action}'。"
        
    def _format_response(self, text: str) -> str:
        """
        从模型的最终响应中提取“最终答案”。
        """
        # 尝试从“行动输入”中提取最终答案
        final_answer_match = re.search(r"行动输入[:：]\s*(.*)", text, re.DOTALL)
        if final_answer_match:
            return final_answer_match.group(1).strip()
        # 如果找不到，返回模型的原始输出作为备用
        return text

    def _original_react_run(self, prompt: str, max_iterations: int, verbose: bool) -> str:
        """
        原始的 ReAct 循环，现在作为“执行者”来完成单个任务。
        Args:
            prompt: 需要执行的任务描述，可能包含上下文。
        """
        # ---【并且修改这里】---
        # 不再是 query，而是通用的 prompt
        current_prompt = f"问题：{prompt}"
        history = []

        for i in range(max_iterations):
            if verbose:
                print(f"\n[ReAct Executor] 第 {i + 1} 次思考...")
                print(f"DEBUG: Sending to model:\n---\n{current_prompt}\n---")

            # 1. 思考 (调用大模型)
            response_text, history = self.model.chat(current_prompt, history, self.system_prompt)

            if verbose:
                print(f"[ReAct Executor] 模型响应:\n{response_text}")

            # 2. 解析行动
            action, action_input = self._parse_action(response_text, verbose)

            # 3. 检查是否结束
            if action.lower() == "最终答案":
                if verbose:
                    print("[ReAct Executor] 子任务完成，获得最终答案。")
                return self._format_response(response_text)

            if not action:
                if verbose:
                    print("[ReAct Executor] 未能解析出有效行动，将返回当前响应。")
                return response_text

            # 4. 行动 & 观察
            if verbose:
                print(f"[ReAct Executor] 执行行动: {action} | 参数: {action_input}")
            observation = self._execute_action(action, action_input)
            last_observation = observation

            # 检查观察结果是否是“坏”的
            if "错误：" in observation or "失败：" in observation:
                # 如果失败，则进入反思步骤
                reflection_text = self._reflect(response_text, observation, verbose)
                # 将反思的结果作为下一轮的输入
                current_prompt = reflection_text
                continue  # 直接进入下一轮循环

            if verbose:
                print(f"[ReAct Executor] 观察结果:\n{observation}")

            # 5. 准备下一轮的输入
            current_prompt = f"{response_text}\n观察: {observation}"

        print("[ReAct Executor] 达到最大迭代次数，将返回最后的响应。")
        return last_observation if last_observation else self._format_response(response_text)

    def run(self, query: str, max_iterations: int = 5, use_plan: bool = True, verbose: bool = True) -> str:
        """
        运行 Agent。可以选择是否使用“规划-执行”模式。
        """

        # 使用当前时间戳为这次运行创建一个独一无二的日志文件名
        session_id = f"run_{time.strftime('%Y%m%d_%H%M%S')}"
        log_file_path = os.path.join(self.log_dir, f"{session_id}.log")
        print(f"[Agent] 本次运行的完整日志将保存在: {log_file_path}")

        if not use_plan:
            # 对于非规划模式，我们也可以记录简单的日志
            result = self._original_react_run(query, max_iterations=5, verbose=verbose)  # 假设 max_iterations=5
            with open(log_file_path, 'w', encoding='utf-8') as f:
                f.write(f"原始问题:\n{query}\n\n执行过程与结果:\n{result}")
            return result

        # --- 规划-执行模式 ---
        # 1. 规划阶段
        plan = self._generate_plan(query, verbose)
        if not plan:
            print("[Agent] 未能生成有效计划，将尝试直接回答。")
            return self._original_react_run(query, 1, verbose)  # 尝试一次 ReAct

        # 2. 执行阶段
        # context 用于存储每一步的执行结果，作为后续步骤的参考
        # context = f"原始问题: {query}\n行动计划:\n{json.dumps(plan, indent=2, ensure_ascii=False)}\n"

        context = f"Session ID: {session_id}\n"
        context += f"Start Time: {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
        context += f"Original Query: {query}\n\n"
        context += f"Generated Plan:\n{json.dumps(plan, indent=2, ensure_ascii=False)}\n"
        context += "=" * 50 + "\n\n"

        # 将初始上下文写入日志文件
        with open(log_file_path, 'w', encoding='utf-8') as f:
            f.write(context)

        for step_info in plan:
            step_num = step_info.get("step")
            task = step_info.get("task")
            if verbose:
                print(f"\n[Executor] === 正在执行步骤 {step_num}: {task} ===")

            with open(log_file_path, 'a', encoding='utf-8') as f:
                f.write(step_header)

            # 将当前步骤的任务和之前所有步骤的结果一起交给 ReAct 循环去完成
            # _original_react_run 现在扮演了“执行者”的角色
            # 我们限制它只为当前子任务进行短期迭代
            step_result = self._original_react_run(
                prompt=f"基于以下上下文，请完成当前任务：\n上下文:\n{context}\n\n当前任务: {task}",
                max_iterations=max_iterations,  # 允许子任务内部多次 ReAct
                verbose=verbose
            )
            step_result_content = execution_result["content"]
            step_context = f"Step {step_num} ({task}) Result:\n{step_result_content}\n\n"
            context += step_context  # 更新内存中的 context

            with open(log_file_path, 'a', encoding='utf-8') as f:
                f.write(step_context)  # 追加到文件

        # 3. 最终总结
        if verbose:
            print("\n[Summarizer] === 所有步骤已执行完毕，正在生成最终总结 ===")

        final_summary_prompt = f"""基于以下完整的执行过程和结果，请为用户的原始问题生成一个最终的、全面的答案。
            ---
            {context}
            ---
            最终答案:"""

        final_answer, _ = self.model.chat(prompt=final_summary_prompt, history=[],
                                          system_prompt="你是一个善于总结的助手。")

        final_summary_context = f"End Time: {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
        final_summary_context += "=" * 50 + "\n\n"
        final_summary_context += f"Final Summary:\n{final_answer}\n"

        with open(log_file_path, 'a', encoding='utf-8') as f:
            f.write(final_summary_context)

        return final_answer

    def _reflect(self, failed_prompt: str, observation: str, verbose: bool = True) -> str:
        """
        生成反思和修正计划。
        """
        if verbose:
            print("[Reflector] 检测到执行失败或结果不佳，正在进行反思...")

        reflection_prompt = f"""你正在执行一个任务，但上一步的行动失败或结果不理想。
            ---
            你的思考和行动:
            {failed_prompt}
            ---
            观察到的坏结果:
            {observation}
            ---
            请深刻反思失败的原因，并提出一个具体的、修正后的行动计划（新的“思考”、“行动”、“行动输入”）。
            反思:"""

        reflection, _ = self.model.chat(prompt=reflection_prompt, history=[],
                                        system_prompt="你是一个善于反思和纠错的AI。")

        if verbose:
            print(f"[Reflector] 反思结果:\n{reflection}")

        return reflection
