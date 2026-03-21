#!/usr/bin/env python3
"""
v2_todo_agent.py - 迷你 Claude 代码：结构化规划 (~300 行)

核心哲学："让计划可见"
=====================================
v1 对于简单任务效果很好。但当你要求它 "重构认证、添加测试、更新文档" 时，
没有明确规划的模型会：
  - 随机跳转到不同任务
  - 忘记已完成的步骤
  - 中途失去焦点

问题 - "上下文淡化":
----------------------------
在 v1 中，计划只存在于模型的 "头脑" 中：

    v1: "我将先做 A，然后 B，然后 C" （不可见）
        10 次工具调用后："等等，我刚才在做什么？"

解决方案 - TodoWrite 工具:
----------------------------
v2 添加了一个新工具，从根本上改变了代理的工作方式：

    v2:
      [ ] 重构认证模块
      [>] 添加单元测试         <- 当前正在做这个
      [ ] 更新文档

现在你和模型都能看到计划。模型可以：
  - 工作时更新状态
  - 查看已完成和待完成的任务
  - 一次专注于一个任务

关键约束（不是随意的 - 这些是护栏）：
------------------------------------------------------
    | 规则              | 原因                              |
    |-------------------|----------------------------------|
    | 最多 20 个项目     | 防止无限任务列表                  |
    | 一次只能有一个进行中 | 强制一次专注于一件事             |
    | 必填字段           | 确保结构化输出                    |

深层洞察：
----------------
> "结构既约束又赋能。"

待办事项约束（最大项目数，一个进行中）赋能了（可见计划，跟踪进度）。

这种模式在代理设计中无处不在：
  - max_tokens 约束 -> 启用可管理的响应
  - 工具架构约束 -> 启用结构化调用
  - 待办事项约束 -> 启用复杂任务完成

良好的约束不是限制，而是脚手架。

使用方法：
    python v2_todo_agent_cn.py
"""

import os
import subprocess
import sys
from pathlib import Path

from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv(override=True)


# =============================================================================
# 配置
# =============================================================================

WORKDIR = Path.cwd()

client = Anthropic(base_url=os.getenv("ANTHROPIC_BASE_URL"))
MODEL = os.getenv("MODEL_ID", "claude-sonnet-4-5-20250929")


# =============================================================================
# TodoManager - v2 的核心新增功能
# =============================================================================

class TodoManager:
    """
    管理带有强制约束的结构化任务列表。

    关键设计决策：
    --------------------
    1. 最多 20 个项目：防止无限任务列表
    2. 一次只能有一个进行中：强制专注于一件事
    3. 必填字段：确保结构化输出

    activeForm 字段值得解释：
    - 它是正在发生的事情的现在时态形式
    - 当状态为 "in_progress" 时显示
    - 示例：content="添加测试", activeForm="正在添加单元测试..."

    这让代理正在做什么具有实时可见性。
    """

    def __init__(self):
        self.items = []

    def update(self, items: list) -> str:
        """
        验证并更新待办事项列表。

        模型每次发送一个完整的新列表。我们验证它，
        存储它，并返回模型将看到的渲染视图。

        验证规则：
        - 每个项目必须有：content, status, activeForm
        - 状态必须是：pending | in_progress | completed
        - 一次只能有一个项目处于 in_progress 状态
        - 最多允许 20 个项目

        返回：
            待办事项列表的渲染文本视图
        """
        validated = []
        in_progress_count = 0

        for i, item in enumerate(items):
            # 提取并验证字段
            content = str(item.get("content", "")).strip()
            status = str(item.get("status", "pending")).lower()
            active_form = str(item.get("activeForm", "")).strip()

            # 验证检查
            if not content:
                raise ValueError(f"项目 {i}: 需要 content")
            if status not in ("pending", "in_progress", "completed"):
                raise ValueError(f"项目 {i}: 无效状态 '{status}'")
            if not active_form:
                raise ValueError(f"项目 {i}: 需要 activeForm")

            if status == "in_progress":
                in_progress_count += 1

            validated.append({
                "content": content,
                "status": status,
                "activeForm": active_form
            })

        # 执行约束
        if len(validated) > 20:
            raise ValueError("最多允许 20 个待办事项")
        if in_progress_count > 1:
            raise ValueError("一次只能有一个任务处于 in_progress 状态")

        self.items = validated
        return self.render()

    def render(self) -> str:
        """
        将待办事项列表渲染为人类可读的文本。

        格式：
            [x] 已完成的任务
            [>] 进行中的任务 <- 正在做某事...
            [ ] 待处理的任务

            (2/3 已完成)

        这个渲染的文本是模型作为工具结果看到的。
        然后它可以根据当前状态更新列表。
        """
        if not self.items:
            return "没有待办事项。"

        lines = []
        for item in self.items:
            if item["status"] == "completed":
                lines.append(f"[x] {item['content']}")
            elif item["status"] == "in_progress":
                lines.append(f"[>] {item['content']} <- {item['activeForm']}")
            else:
                lines.append(f"[ ] {item['content']}")

        completed = sum(1 for t in self.items if t["status"] == "completed")
        lines.append(f"\n({completed}/{len(self.items)} 已完成)")

        return "\n".join(lines)


# 全局待办事项管理器实例
TODO = TodoManager()


# =============================================================================
# 系统提示 - 为 v2 更新
# =============================================================================

SYSTEM = f"""你是一名在 {WORKDIR} 工作的编码代理。

循环：计划 -> 使用工具行动 -> 更新待办事项 -> 报告。

规则：
- 使用 TodoWrite 跟踪多步骤任务
- 在开始前将任务标记为 in_progress，完成后标记为 completed
- 优先使用工具而非散文。行动，不要只解释。
- 完成后，总结所做的更改。"""


# =============================================================================
# 系统提醒 - 鼓励使用待办事项的软提示
# =============================================================================

# 在对话开始时显示
INITIAL_REMINDER = "<reminder>对于多步骤任务，请使用 TodoWrite。</reminder>"

# 如果模型很久没有更新待办事项，则显示
NAG_REMINDER = "<reminder>10+ 轮次没有更新待办事项。请更新待办事项。</reminder>"


# =============================================================================
# 工具定义 (v1 工具 + TodoWrite)
# =============================================================================

TOOLS = [
    # v1 工具（未更改）
    {
        "name": "bash",
        "description": "运行 shell 命令。",
        "input_schema": {
            "type": "object",
            "properties": {"command": {"type": "string"}},
            "required": ["command"],
        },
    },
    {
        "name": "read_file",
        "description": "读取文件内容。",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string"},
                "limit": {"type": "integer"}
            },
            "required": ["path"],
        },
    },
    {
        "name": "write_file",
        "description": "将内容写入文件。",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string"},
                "content": {"type": "string"}
            },
            "required": ["path", "content"],
        },
    },
    {
        "name": "edit_file",
        "description": "替换文件中的精确文本。",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string"},
                "old_text": {"type": "string"},
                "new_text": {"type": "string"},
            },
            "required": ["path", "old_text", "new_text"],
        },
    },

    # v2 新增：TodoWrite
    # 这是实现结构化规划的关键新增功能
    {
        "name": "TodoWrite",
        "description": "更新任务列表。用于规划和跟踪进度。",
        "input_schema": {
            "type": "object",
            "properties": {
                "items": {
                    "type": "array",
                    "description": "完整的任务列表（替换现有列表）",
                    "items": {
                        "type": "object",
                        "properties": {
                            "content": {
                                "type": "string",
                                "description": "任务描述"
                            },
                            "status": {
                                "type": "string",
                                "enum": ["pending", "in_progress", "completed"],
                                "description": "任务状态"
                            },
                            "activeForm": {
                                "type": "string",
                                "description": "现在时态动作，例如 '正在读取文件'"
                            },
                        },
                        "required": ["content", "status", "activeForm"],
                    },
                }
            },
            "required": ["items"],
        },
    },
]


# =============================================================================
# 工具实现 (v1 + TodoWrite)
# =============================================================================

def safe_path(p: str) -> Path:
    """确保路径保持在工作区范围内。"""
    path = (WORKDIR / p).resolve()
    if not path.is_relative_to(WORKDIR):
        raise ValueError(f"路径逃离了工作区: {p}")
    return path


def run_bash(cmd: str) -> str:
    """执行带有安全检查的 shell 命令。"""
    dangerous = ["rm -rf /", "sudo", "shutdown", "reboot"]
    if any(d in cmd for d in dangerous):
        return "错误: 危险命令被阻止"
    try:
        result = subprocess.run(
            cmd, shell=True, cwd=WORKDIR,
            capture_output=True, text=True, timeout=60
        )
        output = (result.stdout + result.stderr).strip()
        return output[:50000] if output else "(无输出)"
    except subprocess.TimeoutExpired:
        return "错误: 超时"
    except Exception as e:
        return f"错误: {e}"


def run_read(path: str, limit: int = None) -> str:
    """读取文件内容。"""
    try:
        text = safe_path(path).read_text()
        lines = text.splitlines()
        if limit and limit < len(lines):
            lines = lines[:limit] + [f"... (还有 {len(text.splitlines()) - limit} 行)"]
        return "\n".join(lines)[:50000]
    except Exception as e:
        return f"错误: {e}"


def run_write(path: str, content: str) -> str:
    """将内容写入文件。"""
    try:
        fp = safe_path(path)
        fp.parent.mkdir(parents=True, exist_ok=True)
        fp.write_text(content)
        return f"已写入 {len(content)} 字节到 {path}"
    except Exception as e:
        return f"错误: {e}"


def run_edit(path: str, old_text: str, new_text: str) -> str:
    """替换文件中的精确文本。"""
    try:
        fp = safe_path(path)
        content = fp.read_text()
        if old_text not in content:
            return f"错误: 在 {path} 中未找到文本"
        fp.write_text(content.replace(old_text, new_text, 1))
        return f"已编辑 {path}"
    except Exception as e:
        return f"错误: {e}"


def run_todo(items: list) -> str:
    """
    更新待办事项列表。

    模型发送一个完整的新列表（不是差异）。
    我们验证它并返回渲染视图。
    """
    try:
        return TODO.update(items)
    except Exception as e:
        return f"错误: {e}"


def execute_tool(name: str, args: dict) -> str:
    """将工具调用分发到实现。"""
    if name == "bash":
        return run_bash(args["command"])
    if name == "read_file":
        return run_read(args["path"], args.get("limit"))
    if name == "write_file":
        return run_write(args["path"], args["content"])
    if name == "edit_file":
        return run_edit(args["path"], args["old_text"], args["new_text"])
    if name == "TodoWrite":
        return run_todo(args["items"])
    return f"未知工具: {name}"


# =============================================================================
# 代理循环（带有待办事项跟踪）
# =============================================================================

# 跟踪自上次更新待办事项以来的轮次数
rounds_without_todo = 0


def agent_loop(messages: list) -> list:
    """
    带有待办事项使用跟踪的代理循环。

    与 v1 相同的核心循环，但现在我们跟踪模型
    是否正在使用待办事项。如果它太长时间没有更新，
    我们会在下一条用户消息（工具结果）中注入提醒。
    """
    global rounds_without_todo

    while True:
        response = client.messages.create(
            model=MODEL,
            system=SYSTEM,
            messages=messages,
            tools=TOOLS,
            max_tokens=8000,
        )

        tool_calls = []
        for block in response.content:
            if hasattr(block, "text"):
                print(block.text)
            if block.type == "tool_use":
                tool_calls.append(block)

        if response.stop_reason != "tool_use":
            messages.append({"role": "assistant", "content": response.content})
            return messages

        results = []
        used_todo = False

        for tc in tool_calls:
            print(f"\n> {tc.name}")
            output = execute_tool(tc.name, tc.input)
            preview = output[:300] + "..." if len(output) > 300 else output
            print(f"  {preview}")

            results.append({
                "type": "tool_result",
                "tool_use_id": tc.id,
                "content": output,
            })

            # 跟踪待办事项使用情况
            if tc.name == "TodoWrite":
                used_todo = True

        # 更新计数器：如果使用了待办事项则重置，否则递增
        if used_todo:
            rounds_without_todo = 0
        else:
            rounds_without_todo += 1

        messages.append({"role": "assistant", "content": response.content})

        # 如果模型长时间没有使用待办事项，则将 NAG_REMINDER 注入到用户消息中
        # 这发生在代理循环内部，因此模型在任务执行过程中会看到它
        if rounds_without_todo > 10:
            results.insert(0, {"type": "text", "text": NAG_REMINDER})

        messages.append({"role": "user", "content": results})


# =============================================================================
# 主 REPL
# =============================================================================

def main():
    """
    带有提醒注入的 REPL。

    v2 关键新增功能：我们注入 "提醒" 消息来鼓励
    使用待办事项，而不强制要求。这是一个软约束。

    - INITIAL_REMINDER: 在对话开始时注入
    - NAG_REMINDER: 当 10+ 轮次没有更新待办事项时在 agent_loop 中注入
    """
    global rounds_without_todo

    print(f"迷你 Claude Code v2 (带待办事项) - {WORKDIR}")
    print("输入 'exit' 退出。\n")

    history = []
    first_message = True

    while True:
        try:
            user_input = input("你: ").strip()
        except (EOFError, KeyboardInterrupt):
            break

        if not user_input or user_input.lower() in ("exit", "quit", "q"):
            break

        # 构建用户消息内容
        content = []

        if first_message:
            # 对话开始时的温和提醒
            content.append({"type": "text", "text": INITIAL_REMINDER})
            first_message = False

        content.append({"type": "text", "text": user_input})
        history.append({"role": "user", "content": content})

        try:
            agent_loop(history)
        except Exception as e:
            print(f"错误: {e}")

        print()


if __name__ == "__main__":
    main()