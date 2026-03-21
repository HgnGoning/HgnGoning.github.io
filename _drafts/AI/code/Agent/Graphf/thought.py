# thought.py

from typing import List, Optional
import uuid

class Thought:
    """
    表示 GoT 图中的一个节点。
    """
    def __init__(self, content: str, parent: Optional['Thought'] = None, score: float = 0.0):
        self.id = str(uuid.uuid4())
        self.content = content  # 节点的文本内容，即“想法”
        self.parent = parent    # 指向父节点
        self.children: List['Thought'] = [] # 指向子节点
        self.score = score      # 评估分数

    def add_child(self, child_thought: 'Thought'):
        """添加一个子节点"""
        self.children.append(child_thought)

    def __repr__(self):
        return f"Thought(id={self.id[:4]}..., score={self.score}, content='{self.content[:30]}...')"
