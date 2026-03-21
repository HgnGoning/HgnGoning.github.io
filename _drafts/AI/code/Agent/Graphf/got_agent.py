# got_agent.py

import json5
from typing import List

# 导入我们项目中的其他模块
from models import BaseModel, Siliconflow
from thought import Thought

class GoTAgent:
    """
    一个简化的 Graph of Thoughts (GoT) Agent。
    """
    def __init__(self, model: BaseModel):
        self.model = model
        self.graph: Dict[str, Thought] = {} # 用字典存储所有 thought 节点，方便访问

    def _call_llm(self, prompt: str, system_prompt: str) -> str:
        """封装对大模型的调用"""
        response, _ = self.model.chat(prompt, system_prompt=system_prompt)
        return response

    def generate_thoughts(self, parent_thought: Thought, num_thoughts: int) -> List[Thought]:
        """
        【生成操作】从一个父节点生成多个并行的想法。
        """
        print(f"\n--- [Generator] Generating {num_thoughts} thoughts from: '{parent_thought.content}' ---")
        system_prompt = f"你是一个富有创造力的思想家。请根据以下主题，发散思维，生成 {num_thoughts} 个不同角度的、独立的观点或子主题。请以JSON格式的列表返回，例如：[\"观点1\", \"观点2\"]"
        
        prompt = f"主题：{parent_thought.content}"
        response = self._call_llm(prompt, system_prompt)
        
        try:
            new_contents = json5.loads(response)
            if not isinstance(new_contents, list): new_contents = [response]
        except:
            new_contents = [response] # 降级处理

        new_thoughts = []
        for content in new_contents[:num_thoughts]:
            child = Thought(content=content, parent=parent_thought)
            parent_thought.add_child(child)
            self.graph[child.id] = child
            new_thoughts.append(child)
            print(f"  -> Generated: {child}")
            
        return new_thoughts

    def evaluate_thoughts(self, thoughts: List[Thought], context: str):
        """
        【评估操作】对一组想法进行打分。
        """
        print(f"\n--- [Evaluator] Evaluating {len(thoughts)} thoughts... ---")
        system_prompt = """你是一个严谨的评论家。你的任务是根据一个总体目标，为下面给出的每个“想法”的相关性和质量打分。
请以JSON格式返回一个字典，key是想法内容，value是0到10的分数。例如：{"想法A": 8, "想法B": 5}"""
        
        # 将所有想法的内容组合成一个列表，让LLM一次性评估
        thoughts_content_list = [t.content for t in thoughts]
        prompt = f"总体目标：{context}\n\n请为以下想法列表打分：\n{thoughts_content_list}"
        response = self._call_llm(prompt, system_prompt)

        try:
            scores = json5.loads(response)
            for thought in thoughts:
                if thought.content in scores:
                    thought.score = scores[thought.content]
                    print(f"  -> Evaluated: {thought}")
        except Exception as e:
            print(f"  -> Evaluation failed: {e}")

    def aggregate_thoughts(self, thoughts_to_aggregate: List[Thought], context: str) -> Thought:
        """
        【聚合操作】将多个想法合并成一个更高级的想法。
        """
        print(f"\n--- [Aggregator] Aggregating {len(thoughts_to_aggregate)} thoughts... ---")
        system_prompt = "你是一个顶级的综合分析师。你的任务是将下面多个分散的观点或信息，提炼、整合成一个更全面、更深刻、更有条理的单一结论。"
        
        thoughts_content = "\n".join([f"- {t.content} (评分: {t.score})" for t in thoughts_to_aggregate])
        prompt = f"总体目标：{context}\n\n请整合以下观点：\n{thoughts_content}"
        
        aggregated_content = self._call_llm(prompt, system_prompt)
        
        aggregated_thought = Thought(content=aggregated_content)
        self.graph[aggregated_thought.id] = aggregated_thought
        print(f"  -> Aggregated into new thought: {aggregated_thought}")
        return aggregated_thought

    def run(self, initial_query: str) -> str:
        """
        执行 GoT 流程。
        """
        # 1. 初始化图
        root_thought = Thought(content=initial_query)
        self.graph[root_thought.id] = root_thought

        # 2. 【生成】第一层：从初始问题出发，生成多个分析角度
        initial_perspectives = self.generate_thoughts(root_thought, 3)
        self.evaluate_thoughts(initial_perspectives, initial_query)

        # 3. 【生成】第二层：对每个角度，生成具体的利弊分析
        all_pros_and_cons = []
        for perspective in initial_perspectives:
            # 我们为每个角度都生成2个具体的想法
            pros_and_cons = self.generate_thoughts(perspective, 2)
            all_pros_and_cons.extend(pros_and_cons)
        
        # 4. 【评估】对所有利弊分析进行统一评估
        self.evaluate_thoughts(all_pros_and_cons, "分析远程工作的具体利弊")

        # 5. 筛选出高质量的想法用于聚合
        high_quality_thoughts = [t for t in all_pros_and_cons if t.score >= 5]
        if not high_quality_thoughts:
            high_quality_thoughts = all_pros_and_cons # 如果都没有高分的，就全都用

        # 6. 【聚合】将所有高质量的利弊分析，聚合成一个“综合利弊分析”
        aggregated_analysis = self.aggregate_thoughts(high_quality_thoughts, "总结远程工作的利弊")

        # 7. 【改进/最终生成】基于聚合后的分析，生成最终建议
        print("\n--- [Finalizer] Generating final recommendations... ---")
        finalizer_system_prompt = "你是一位资深的职业规划导师。请根据以下对远程工作利弊的综合分析，为正在找工作的求职者提供具体、可行的建议。"
        final_prompt = f"综合分析:\n{aggregated_analysis.content}"
        final_answer = self._call_llm(final_prompt, finalizer_system_prompt)

        return final_answer
