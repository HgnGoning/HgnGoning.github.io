# agent_with_skills.py

from typing import List, Dict
import time
import re
import json
import json5
import os

# 导入我们项目中的其他模块
from models import Siliconflow, BaseModel,DashscopeModel
from tools import ReactTools
from skills import BaseSkill, ResearchSkill # 导入技能相关的类

class SkillBasedAgent:
    """
    一个基于“技能”分层决策的智能体。
    其主要职责是作为总调度官，选择并执行最合适的技能。
    """
    def __init__(self, dashscope_api_key: str, serper_api_key: str) -> None:
        """
        初始化 Agent，加载大脑、工具箱和所有可用技能。
        """
        self.model: BaseModel = DashscopeModel(dashscope_api_key)
        self.tools: ReactTools = ReactTools(serper_api_key=serper_api_key)
        # 核心改动：加载所有技能，并以字典形式存储
        self.skills: Dict[str, BaseSkill] = self._load_skills()
        
        # 核心改动：系统提示现在是用来指导“技能选择”的
        self.system_prompt: str = self._build_system_prompt()
        
        print("技能型 Agent 初始化完成。")
        print(f"已加载技能: {list(self.skills.keys())}")

    def _load_skills(self) -> Dict[str, BaseSkill]:
        """
        加载所有可用的技能。
        这是一个“技能注册”中心，所有新建的技能都需要在这里实例化。
        """
        # 我们在这里手动“注册”所有技能
        available_skills = [
            ResearchSkill(model=self.model, tools=self.tools),
            # 以后可以继续添加, 例如:
            # CodeDebuggerSkill(model=self.model, tools=self.tools),
        ]
        return {skill.name: skill for skill in available_skills}

    def _build_system_prompt(self) -> str:
        """
        构建一个描述可用【技能】及其用途的系统提示。
        这个提示的目标是让大模型能做出正确的“技能选择”决策。
        """
        # 将每个技能的名称和描述格式化，供模型阅读
        skill_descriptions = "\n".join(
            [f"- 技能名称: `{skill.name}`\n  技能描述: {skill.description}" for name, skill in self.skills.items()]
        )
        
        prompt_template = f"""你是一个能力强大的AI总调度官（Agent Dispatcher）。你的唯一任务是根据用户的请求，从下面的技能列表中选择一个最合适的【技能】来完成任务。

--- 可用技能列表 ---
{skill_descriptions}
--------------------

请严格遵循以下JSON格式输出你的决策，不要包含任何额外的解释或文字：
{{
  "skill": "你选择的技能名称",
  "args": {{
    "参数名1": "参数值1",
    "参数名2": "参数值2"
  }}
}}

- "skill"字段的值必须是可用技能列表中的一个技能名称。
- "args"字段是一个包含该技能所需所有参数的字典。请从用户请求中提取参数值。
- 如果用户的请求与所有技能的描述都不匹配，请在 "skill" 字段中返回 "no_skill_found"，并将 "args" 设为空字典。
"""
        return prompt_template
    
    def run(self, query: str, verbose: bool = True) -> str:
        """
        运行 Agent 的主流程：
        1. 让大模型根据 query 和 system_prompt 决定使用哪个技能。
        2. 解析大模型的决策。
        3. 执行被选中的技能。
        """
        if verbose:
            print(f"\n[Agent Dispatcher] 收到新请求: '{query}'")

        # === 阶段 1: 技能选择 ===
        # 调用大模型，让它做出决策
        decision_response, _ = self.model.chat(
            prompt=query,
            history=[],
            system_prompt=self.system_prompt
        )
        
        if verbose:
            print(f"[Agent Dispatcher] 大脑决策（原始输出）:\n{decision_response}")

        # === 阶段 2: 决策解析 ===
        try:
            # 尝试从模型返回的文本中提取出JSON部分
            json_match = re.search(r"\{.*\}", decision_response, re.DOTALL)
            if not json_match:
                raise ValueError("模型返回的响应中未找到有效的JSON对象。")
            
            decision_str = json_match.group(0)
            decision = json5.loads(decision_str)
            
            skill_name = decision.get("skill")
            skill_args = decision.get("args", {})
        except Exception as e:
            if verbose:
                print(f"[Agent Dispatcher] 解析决策失败: {e}。将尝试直接回答。")
            # 如果解析失败，退回到一个简单的直接回答模式，作为降级方案
            return self.model.chat(query, [])[0]

        # === 阶段 3: 技能执行 ===
        if skill_name and skill_name in self.skills:
            selected_skill = self.skills[skill_name]
            if verbose:
                print(f"[Agent Dispatcher] 决策结果: 准备调用技能 '{skill_name}' | 参数: {skill_args}")
            
            try:
                # 使用 **skill_args 将字典解包为关键字参数，传递给技能的 __call__ 方法
                result = selected_skill(**skill_args)
                return result
            except TypeError as e:
                # 捕获参数不匹配的错误
                return f"执行技能 '{skill_name}' 时发生参数错误: {e}。请检查 'args' 是否与技能要求匹配。"
            except Exception as e:
                return f"执行技能 '{skill_name}' 时发生未知错误: {e}"
        
        elif skill_name == "no_skill_found":
            if verbose:
                print("[Agent Dispatcher] 大脑决策: 无合适技能。将尝试直接回答。")
            return self.model.chat(query, [])[0]

        else:
            if verbose:
                print(f"[Agent Dispatcher] 决策了一个未知的技能: '{skill_name}'。将尝试直接回答。")
            return self.model.chat(query, [])[0]
