#!/usr/bin/env python3
"""
v3_subagent.py - 迷你 Claude 代码：子代理机制 (~450 行)

核心哲学："通过上下文隔离实现分而治之"
=============================================================
v2 添加了规划功能。但对于像 "探索代码库然后重构认证" 这样的大型任务，
单个代理会遇到问题：

问题 - 上下文污染：
-------------------------------
    单代理历史：
      [探索中...] cat file1.py -> 500 行
      [探索中...] cat file2.py -> 300 行
      ... 15 个更多文件 ...
      [现在重构中...] "等等，file1 包含什么？"

模型的上下文充满了探索细节，几乎没有空间用于实际任务。这就是 "上下文污染"。

解决方案 - 具有隔离上下文的子代理：
----------------------------------------------
    主代理历史：
      [任务: 探索代码库]
        -> 子代理探索 20 个文件（在其自己的上下文中）
        -> 仅返回："认证在 src/auth/ 中，数据库在 src/models/ 中"
      [现在使用干净的上下文进行重构]

每个子代理都有：
  1. 自己全新的消息历史
  2. 过滤后的工具（探索代理不能写入）
  3. 专门的系统提示
  4. 仅向父代理返回最终摘要

关键洞察：
---------------
    进程隔离 = 上下文隔离

通过生成子任务，我们获得：
  - 主代理的干净上下文
  - 可能的并行探索
  - 自然的任务分解
  - 相同的代理循环，不同的上下文

代理类型注册表：
-------------------
    | 类型    | 工具               | 用途                     |
    |---------|---------------------|---------------------------- |
    | explore | bash, read_file     | 只读探索                  |
    | code    | 所有工具            | 完全实现访问              |
    | plan    | bash, read_file     | 设计而不修改              |

典型流程：
-------------  
    用户："将认证重构为使用 JWT"

    主代理：
      1. Task(explore)："查找所有与认证相关的文件"
         -> 子代理读取 10 个文件
         -> 返回："认证在 src/auth/login.py..."

      2. Task(plan)："设计 JWT 迁移策略"
         -> 子代理分析结构
         -> 返回："1. 添加 jwt 库 2. 创建工具函数..."

      3. Task(code)："实现 JWT 令牌"
         -> 子代理编写代码
         -> 返回："创建了 jwt_utils.py，更新了 login.py"

      4. 向用户总结更改

使用方法：
    python v3_subagent_cn.py
"""

import os
import subprocess
import sys
import time
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
# 代理类型注册表 - 子代理机制的核心
# =============================================================================

AGENT_TYPES = {
    # Explore: 用于搜索和分析的只读代理
    # 不能修改文件 - 安全用于广泛探索
    "explore": {
        "description": "用于探索代码、查找文件、搜索的只读代理",
        "tools": ["bash", "read_file"],  # 无写访问权限
        "prompt": "你是一个探索代理。搜索和分析，但永远不要修改文件。返回简洁的摘要。",
    },

    # Code: 用于实现的全功能代理
    # 拥有所有工具 - 用于实际编码工作
    "code": {
        "description": "用于实现功能和修复错误的完整代理",
        "tools": "*",  # 所有工具
        "prompt": "你是一个编码代理。高效地实现请求的更改。",
    },

    # Plan: 用于设计工作的分析代理
    # 只读，专注于生成计划和策略
    "plan": {
        "description": "用于设计实现策略的规划代理",
        "tools": ["bash", "read_file"],  # 只读
        "prompt": "你是一个规划代理。分析代码库并输出编号的实现计划。不要进行更改。",
    },
}


def get_agent_descriptions() -> str:
    """生成用于 Task 工具的代理类型描述。"""
    return "\n".join(
        f"- {name}: {cfg['description']}"
        for name, cfg in AGENT_TYPES.items()
    )


# =============================================================================
# TodoManager (来自 v2，未更改)
# =============================================================================

class TodoManager:
    """带有约束的任务列表管理器。详情见 v2。"""

    def __init__(self):
        self.items = []

    def update(self, items: list) -> str:
        validated = []
        in_progress = 0

        for i, item in enumerate(items):
            content = str(item.get("content", "")).strip()
            status = str(item.get("status", "pending")).lower()
            active = str(item.get("activeForm", "")).strip()

            if not content or not active:
                raise ValueError(f"项目 {i}: 需要 content 和 activeForm")
            if status not in ("pending", "in_progress", "completed"):
                raise ValueError(f"项目 {i}: 无效状态")
            if status == "in_progress":
                in_progress += 1

            validated.append({
                "content": content,
                "status": status,
                "activeForm": active
            })

        if in_progress > 1:
            raise ValueError("一次只能有一个任务处于 in_progress 状态")

        self.items = validated[:20]
        return self.render()

    def render(self) -> str:
        if not self.items:
            return "没有待办事项。"
        lines = []
        for t in self.items:
            mark = "[x]" if t["status"] == "completed" else \
                   "[>]" if t["status"] == "in_progress" else "[ ]"
            lines.append(f"{mark} {t['content']}")
        done = sum(1 for t in self.items if t["status"] == "completed")
        return "\n".join(lines) + f"\n({done}/{len(self.items)} 已完成)"


TODO = TodoManager()


# =============================================================================
# 系统提示
# =============================================================================

SYSTEM = f"""你是一名在 {WORKDIR} 工作的编码代理。

循环：计划 -> 使用工具行动 -> 报告。

你可以为复杂的子任务生成子代理：
{get_agent_descriptions()}

规则：
- 对需要集中探索或实现的子任务使用 Task 工具
- 使用 TodoWrite 跟踪多步骤工作
- 优先使用工具而非散文。行动，不要只解释。
- 完成后，总结所做的更改。"""


# =============================================================================
# 基础工具定义
# =============================================================================

BASE_TOOLS = [
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
        "description": "写入文件。",
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
        "description": "替换文件中的文本。",
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
    {
        "name": "TodoWrite",
        "description": "更新任务列表。",
        "input_schema": {
            "type": "object",
            "properties": {
                "items": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "content": {"type": "string"},
                            "status": {
                                "type": "string",
                                "enum": ["pending", "in_progress", "completed"]
                            },
                            "activeForm": {"type": "string"},
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
# Task 工具 - v3 中的核心新增功能
# =============================================================================

TASK_TOOL = {
    "name": "Task",
    "description": f"""为集中的子任务生成子代理。

子代理在隔离的上下文中运行 - 它们看不到父代理的历史。
使用此工具保持主对话干净。

代理类型：
{get_agent_descriptions()}

示例用法：
- Task(explore)："查找使用认证模块的所有文件"
- Task(plan)："设计数据库迁移策略"
- Task(code)："实现用户注册表单"
""",
    "input_schema": {
        "type": "object",
        "properties": {
            "description": {
                "type": "string",
                "description": "用于进度显示的短任务名称（3-5 个单词）"
            },
            "prompt": {
                "type": "string",
                "description": "给子代理的详细说明"
            },
            "agent_type": {
                "type": "string",
                "enum": list(AGENT_TYPES.keys()),
                "description": "要生成的代理类型"
            },
        },
        "required": ["description", "prompt", "agent_type"],
    },
}

# 主代理获取包括 Task 在内的所有工具
ALL_TOOLS = BASE_TOOLS + [TASK_TOOL]


def get_tools_for_agent(agent_type: str) -> list:
    """
    根据代理类型过滤工具。

    每种代理类型都有允许使用的工具白名单。
    '*' 表示所有工具（但子代理不会获得 Task 以防止无限递归）。
    """
    allowed = AGENT_TYPES.get(agent_type, {}).get("tools", "*")

    if allowed == "*":
        return BASE_TOOLS  # 所有基础工具，但不包括 Task（演示中无递归）

    return [t for t in BASE_TOOLS if t["name"] in allowed]


# =============================================================================
# 工具实现
# =============================================================================

def safe_path(p: str) -> Path:
    """确保路径保持在工作区内。"""
    path = (WORKDIR / p).resolve()
    if not path.is_relative_to(WORKDIR):
        raise ValueError(f"路径逃离了工作区: {p}")
    return path


def run_bash(cmd: str) -> str:
    """执行带有安全检查的 shell 命令。"""
    if any(d in cmd for d in ["rm -rf /", "sudo", "shutdown"]):
        return "错误: 危险命令"
    try:
        r = subprocess.run(
            cmd, shell=True, cwd=WORKDIR,
            capture_output=True, text=True, timeout=60
        )
        return ((r.stdout + r.stderr).strip() or "(无输出)")[:50000]
    except Exception as e:
        return f"错误: {e}"


def run_read(path: str, limit: int = None) -> str:
    """读取文件内容。"""
    try:
        lines = safe_path(path).read_text().splitlines()
        if limit:
            lines = lines[:limit]
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
        text = fp.read_text()
        if old_text not in text:
            return f"错误: 在 {path} 中未找到文本"
        fp.write_text(text.replace(old_text, new_text, 1))
        return f"已编辑 {path}"
    except Exception as e:
        return f"错误: {e}"


def run_todo(items: list) -> str:
    """更新待办事项列表。"""
    try:
        return TODO.update(items)
    except Exception as e:
        return f"错误: {e}"


# =============================================================================
# 子代理执行 - v3 的核心
# =============================================================================

def run_task(description: str, prompt: str, agent_type: str) -> str:
    """
    使用隔离的上下文执行子代理任务。

    这是子代理机制的核心：

    1. 创建隔离的消息历史（关键：无父上下文！）
    2. 使用代理特定的系统提示
    3. 根据代理类型过滤可用工具
    4. 运行与主代理相同的查询循环
    5. 仅返回最终文本（而非中间细节）

    父代理只看到摘要，保持其上下文清洁。

    进度显示：
    ----------------
    运行时，我们显示：
      [explore] 查找认证文件 ... 5 个工具，3.2s

    这提供了可见性，而不会污染主对话。
    """
    if agent_type not in AGENT_TYPES:
        return f"错误: 未知代理类型 '{agent_type}'"

    config = AGENT_TYPES[agent_type]

    # 代理特定的系统提示
    sub_system = f"""你是一名在 {WORKDIR} 工作的 {agent_type} 子代理。

{config["prompt"]}

完成任务并返回清晰、简洁的摘要。"""

    # 为此代理类型过滤工具
    sub_tools = get_tools_for_agent(agent_type)

    # 隔离的消息历史 - 这是关键！
    # 子代理从头开始，看不到父代理的对话
    sub_messages = [{"role": "user", "content": prompt}]

    # 进度跟踪
    print(f"  [{agent_type}] {description}")
    start = time.time()
    tool_count = 0

    # 运行与主代理相同的代理循环（静默 - 不打印到主聊天）
    while True:
        response = client.messages.create(
            model=MODEL,
            system=sub_system,
            messages=sub_messages,
            tools=sub_tools,
            max_tokens=8000,
        )

        if response.stop_reason != "tool_use":
            break

        tool_calls = [b for b in response.content if b.type == "tool_use"]
        results = []

        for tc in tool_calls:
            tool_count += 1
            output = execute_tool(tc.name, tc.input)
            results.append({
                "type": "tool_result",
                "tool_use_id": tc.id,
                "content": output
            })

            # 更新进度行（原地）
            elapsed = time.time() - start
            sys.stdout.write(
                f"\r  [{agent_type}] {description} ... {tool_count} 个工具，{elapsed:.1f}s"
            )
            sys.stdout.flush()

        sub_messages.append({"role": "assistant", "content": response.content})
        sub_messages.append({"role": "user", "content": results})

    # 最终进度更新
    elapsed = time.time() - start
    sys.stdout.write(
        f"\r  [{agent_type}] {description} - 完成 ({tool_count} 个工具，{elapsed:.1f}s)\n"
    )

    # 提取并仅返回最终文本
    # 这是父代理看到的 - 干净的摘要
    for block in response.content:
        if hasattr(block, "text"):
            return block.text

    return "(子代理未返回文本)"


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
    if name == "Task":
        return run_task(args["description"], args["prompt"], args["agent_type"])
    return f"未知工具: {name}"


# =============================================================================
# 主代理循环
# =============================================================================

def agent_loop(messages: list) -> list:
    """
    带有子代理支持的主代理循环。

    与 v1/v2 相同的模式，但现在包含 Task 工具。
    当模型调用 Task 时，它会生成具有隔离上下文的子代理。
    """
    while True:
        response = client.messages.create(
            model=MODEL,
            system=SYSTEM,
            messages=messages,
            tools=ALL_TOOLS,
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
        for tc in tool_calls:
            # Task 工具具有特殊的显示处理
            if tc.name == "Task":
                print(f"\n> Task: {tc.input.get('description', '子任务')}")
            else:
                print(f"\n> {tc.name}")

            output = execute_tool(tc.name, tc.input)

            # 不打印完整的 Task 输出（它自己管理显示）
            if tc.name != "Task":
                preview = output[:200] + "..." if len(output) > 200 else output
                print(f"  {preview}")

            results.append({
                "type": "tool_result",
                "tool_use_id": tc.id,
                "content": output
            })

        messages.append({"role": "assistant", "content": response.content})
        messages.append({"role": "user", "content": results})


# =============================================================================
# 主 REPL
# =============================================================================

def main():
    print(f"迷你 Claude Code v3 (带子代理) - {WORKDIR}")
    print(f"代理类型: {', '.join(AGENT_TYPES.keys())}")
    print("输入 'exit' 退出。\n")

    history = []

    while True:
        try:
            user_input = input("你: ").strip()
        except (EOFError, KeyboardInterrupt):
            break

        if not user_input or user_input.lower() in ("exit", "quit", "q"):
            break

        history.append({"role": "user", "content": user_input})

        try:
            agent_loop(history)
        except Exception as e:
            print(f"错误: {e}")

        print()


if __name__ == "__main__":
    main()