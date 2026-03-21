from typing import List, Dict
from tools import ReactTools
from models import BaseModel

class BaseSkill:
    """
    技能的基类。每个技能都应该有自己的名称和描述。
    """
    name: str = "base_skill"
    description: str = "这是一个基础技能模板。"

    def __init__(self, model: BaseModel, tools: ReactTools):
        self.model = model
        self.tools = tools

    def __call__(self, *args, **kwargs) -> str:
        """
        让技能对象可以像函数一样被调用。
        """
        raise NotImplementedError("每个技能都必须实现 __call__ 方法")

class ResearchSkill(BaseSkill):
    """
    研究技能：对一个给定的主题进行深入研究，并生成一份总结报告。
    """
    name: str = "topic_researcher"
    description: str = "当需要对某个特定主题、概念或事件进行全面、深入的研究和总结时，使用此技能。例如：'帮我研究一下量子计算的最新进展'。"

    def __init__(self, model: BaseModel, tools: ReactTools):
        super().__init__(model, tools)
        self.research_system_prompt = self._build_system_prompt()
        
    def _build_system_prompt(self) -> str:
        # 这个 Prompt 专门指导模型如何扮演一个“研究员”
        return """你是一位顶级的互联网研究员。你的任务是根据用户给出的主题，通过谷歌搜索收集多方面的信息，然后整合这些信息，生成一份结构清晰、内容全面的总结报告。
            请遵循以下步骤：
            1. **分解主题**：将复杂主题分解成2-3个关键的搜索子问题。
            2. **执行搜索**：对每个子问题进行谷歌搜索。
            3. **整合信息**：阅读并理解所有搜索结果。
            4. **撰写报告**：基于所有信息，撰写一份最终的总结报告。
            """

    def __call__(self, topic: str) -> str:
        """
        执行研究技能。
        Args:
            topic: 需要研究的主题。
        """
        # 这里，技能内部自己实现了一个迷你的 Plan-and-Execute 流程
        
        # 1. 规划搜索关键词
        planner_prompt = f"我需要研究的主题是 '{topic}'。请为我分解出2个核心的谷歌搜索关键词，以JSON列表的格式返回。"
        keywords_response, _ = self.model.chat(
            prompt=planner_prompt, 
            system_prompt="你是一个善于规划搜索策略的助手。"
        )
        try:
            keywords = json5.loads(keywords_response)
        except:
            keywords = [topic] # 如果解析失败，就直接用原始主题

        # 2. 执行搜索
        all_observations = ""
        for keyword in keywords:
            observation = self.tools.google_search(keyword)
            all_observations += f"关于 '{keyword}' 的搜索结果:\n{observation}\n\n"

        # 3. 撰写报告
        summarizer_prompt = f"""请根据以下关于 '{topic}' 的搜索资料，为我撰写一份详细的研究报告。
            ---
            {all_observations}
            ---
            研究报告:"""
        
        final_report, _ = self.model.chat(
            prompt=summarizer_prompt,
            system_prompt=self.research_system_prompt
        )
        return final_report

# 未来可以添加更多技能...
# class CodeDebuggerSkill(BaseSkill): ...
