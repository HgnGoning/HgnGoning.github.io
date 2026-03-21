#!/usr/bin/env python3
"""
v1_basic_agent_cn.py - 迷你 Claude 代码：模型即代理 (~200 行)

核心哲学："模型即代理"
=========================================
Claude Code、Cursor Agent、Codex CLI 的秘密？其实没有秘密。

去掉 CLI 修饰、进度条、权限系统，剩下的东西令人惊讶地简单：
一个让模型反复调用工具直到完成任务的循环。

传统助手：
    用户 -> 模型 -> 文本响应

代理系统：
    用户 -> 模型 -> [工具 -> 结果]* -> 响应
                          ^________|

星号 (*) 很重要！模型会**重复**调用工具，直到它认为任务完成。
这将聊天机器人转变为自主代理。

关键洞察：模型是决策者。代码只是提供工具并运行循环。
模型决定：
  - 调用哪些工具
  - 调用顺序
  - 何时停止

四个核心工具：
------------------------
Claude Code 有 ~20 个工具，但这 4 个涵盖了 90% 的使用场景：

    | 工具       | 用途                  | 示例                      |
    |------------|----------------------|----------------------------|
    | bash       | 运行任何命令          | npm install, git status    |
    | read_file  | 读取文件内容          | 查看 src/index.ts          |
    | write_file | 创建/覆盖文件         | 创建 README.md             |
    | edit_file  | 精确修改文件          | 替换一个函数               |

仅用这 4 个工具，模型就能：
  - 探索代码库 (bash: find, grep, ls)
  - 理解代码 (read_file)
  - 进行修改 (write_file, edit_file)
  - 运行任何东西 (bash: python, npm, make)

使用方法：
    python v1_basic_agent_cn.py
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
MODEL = os.getenv("MODEL_ID", "claude-sonnet-4-5-20250929")
client = Anthropic(base_url=os.getenv("ANTHROPIC_BASE_URL"))


# =============================================================================
# 系统提示 - 模型所需的唯一"配置"
# =============================================================================

SYSTEM = f"""你是一名在 {WORKDIR} 工作的编码代理。

循环：简要思考 -> 使用工具 -> 报告结果。

规则：
- 优先使用工具而非散文。行动，不要只解释。
- 永远不要编造文件路径。如果不确定，先用 bash ls/find。
- 做最小的更改。不要过度设计。
- 完成后，总结所做的更改。"""


# =============================================================================
# 工具定义 - 4 个工具覆盖 90% 的编码任务
# =============================================================================

TOOLS = [
    # 工具 1: Bash - 通向一切的门户
    # 可以运行任何命令：git, npm, python, curl 等
    {
        "name": "bash",
        "description": "运行 shell 命令。用于：ls, find, grep, git, npm, python 等。",
        "input_schema": {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": "要执行的 shell 命令"
                }
            },
            "required": ["command"],
        },
    },

    # 工具 2: Read File - 用于理解现有代码
    # 返回文件内容，可选择限制行数（用于大文件）
    {
        "name": "read_file",
        "description": "读取文件内容。返回 UTF-8 文本。",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "文件的相对路径"
                },
                "limit": {
                    "type": "integer",
                    "description": "最大读取行数（默认：全部）"
                },
            },
            "required": ["path"],
        },
    },

    # 工具 3: Write File - 用于创建新文件或完全重写
    # 自动创建父目录
    {
        "name": "write_file",
        "description": "将内容写入文件。如果需要，会创建父目录。",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "文件的相对路径"
                },
                "content": {
                    "type": "string",
                    "description": "要写入的内容"
                },
            },
            "required": ["path", "content"],
        },
    },

    # 工具 4: Edit File - 用于对现有代码进行精确修改
    # 使用精确字符串匹配进行精准编辑
    {
        "name": "edit_file",
        "description": "替换文件中的精确文本。用于精确编辑。",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "文件的相对路径"
                },
                "old_text": {
                    "type": "string",
                    "description": "要查找的精确文本（必须完全匹配）"
                },
                "new_text": {
                    "type": "string",
                    "description": "替换文本"
                },
            },
            "required": ["path", "old_text", "new_text"],
        },
    },
]


# =============================================================================
# 工具实现
# =============================================================================

def safe_path(p: str) -> Path:
    """
    确保路径保持在工作区范围内（安全措施）。

    防止模型访问项目目录外的文件。
    解析相对路径并检查它们不会通过 '../' 逃离工作区。
    """
    path = (WORKDIR / p).resolve()
    if not path.is_relative_to(WORKDIR):
        raise ValueError(f"路径逃离了工作区: {p}")
    return path


def run_bash(command: str) -> str:
    """
    执行带有安全检查的 shell 命令。

    安全：阻止明显危险的命令。
    超时：60 秒，防止挂起。
    输出：截断为 50KB，防止上下文溢出。
    """
    # 基本安全 - 阻止危险模式
    dangerous = ["rm -rf /", "sudo", "shutdown", "reboot", "> /dev/"]
    if any(d in command for d in dangerous):
        return "错误: 危险命令被阻止"

    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=WORKDIR,
            capture_output=True,
            text=True,
            timeout=60
        )
        output = (result.stdout + result.stderr).strip()
        return output[:50000] if output else "(无输出)"

    except subprocess.TimeoutExpired:
        return "错误: 命令超时 (60s)"
    except Exception as e:
        return f"错误: {e}"


def run_read(path: str, limit: int = None) -> str:
    """
    读取文件内容，可选择限制行数。

    对于大文件，使用 limit 只读取前 N 行。
    输出截断为 50KB，防止上下文溢出。
    """
    try:
        text = safe_path(path).read_text()
        lines = text.splitlines()

        if limit and limit < len(lines):
            lines = lines[:limit]
            lines.append(f"... (还有 {len(text.splitlines()) - limit} 行)")

        return "\n".join(lines)[:50000]

    except Exception as e:
        return f"错误: {e}"


def run_write(path: str, content: str) -> str:
    """
    将内容写入文件，如果需要，创建父目录。

    这用于完整的文件创建/覆盖。
    对于部分编辑，使用 edit_file 代替。
    """
    try:
        fp = safe_path(path)
        fp.parent.mkdir(parents=True, exist_ok=True)
        fp.write_text(content)
        return f"已写入 {len(content)} 字节到 {path}"

    except Exception as e:
        return f"错误: {e}"


def run_edit(path: str, old_text: str, new_text: str) -> str:
    """
    替换文件中的精确文本（精确编辑）。

    使用精确字符串匹配 - old_text 必须完全匹配。
    只替换第一个匹配项，防止意外的大量更改。
    """
    try:
        fp = safe_path(path)
        content = fp.read_text()

        if old_text not in content:
            return f"错误: 在 {path} 中未找到文本"

        # 仅替换第一个匹配项以确保安全
        new_content = content.replace(old_text, new_text, 1)
        fp.write_text(new_content)
        return f"已编辑 {path}"

    except Exception as e:
        return f"错误: {e}"


def execute_tool(name: str, args: dict) -> str:
    """
    将工具调用分发到相应的实现。

    这是模型的工具调用和实际执行之间的桥梁。
    每个工具返回一个字符串结果，该结果会返回给模型。
    """
    if name == "bash":
        return run_bash(args["command"])
    if name == "read_file":
        return run_read(args["path"], args.get("limit"))
    if name == "write_file":
        return run_write(args["path"], args["content"])
    if name == "edit_file":
        return run_edit(args["path"], args["old_text"], args["new_text"])
    return f"未知工具: {name}"


# =============================================================================
# 代理循环 - 这是一切的核心
# =============================================================================

def agent_loop(messages: list) -> list:
    """
    一个函数中的完整代理。

    这是所有编码代理共享的模式：

        while True:
            response = model(messages, tools)
            if 没有工具调用: return
            执行工具，追加结果，继续循环

    模型控制循环：
      - 持续调用工具，直到 stop_reason != "tool_use"
      - 结果成为上下文（作为 "user" 消息反馈）
      - 记忆是自动的（messages 列表累积历史记录）

    为什么这有效：
      1. 模型决定使用哪些工具、顺序以及何时停止
      2. 工具结果为下一个决定提供反馈
      3. 对话历史在轮次间保持上下文
    """
    while True:
        # 步骤 1: 调用模型
        response = client.messages.create(
            model=MODEL,
            system=SYSTEM,
            messages=messages,
            tools=TOOLS,
            max_tokens=8000,
        )

        # 步骤 2: 收集所有工具调用并打印文本输出
        tool_calls = []
        for block in response.content:
            if hasattr(block, "text"):
                print(block.text)
            if block.type == "tool_use":
                tool_calls.append(block)

        # 步骤 3: 如果没有工具调用，任务完成
        if response.stop_reason != "tool_use":
            messages.append({"role": "assistant", "content": response.content})
            return messages

        # 步骤 4: 执行每个工具并收集结果
        results = []
        for tc in tool_calls:
            # 显示正在执行的内容
            print(f"\n> {tc.name}: {tc.input}")

            # 执行并显示结果预览
            output = execute_tool(tc.name, tc.input)
            preview = output[:200] + "..." if len(output) > 200 else output
            print(f"  {preview}")

            # 收集结果给模型
            results.append({
                "type": "tool_result",
                "tool_use_id": tc.id,
                "content": output,
            })

        # 步骤 5: 追加到对话并继续
        # 注意：我们先追加助手的响应，然后是用户的工具结果
        # 这保持了交替的 user/assistant 模式
        messages.append({"role": "assistant", "content": response.content})
        messages.append({"role": "user", "content": results})


# =============================================================================
# 主 REPL
# =============================================================================

def main():
    """
    用于交互使用的简单 Read-Eval-Print Loop。

    history 列表在轮次间维护对话上下文，
    允许带有记忆的多轮对话。
    """
    print(f"迷你 Claude Code v1 - {WORKDIR}")
    print("输入 'exit' 退出。\n")

    history = []

    while True:
        try:
            user_input = input("你: ").strip()
        except (EOFError, KeyboardInterrupt):
            break

        if not user_input or user_input.lower() in ("exit", "quit", "q"):
            break

        # 将用户消息添加到历史记录
        history.append({"role": "user", "content": user_input})

        try:
            # 运行代理循环
            agent_loop(history)
        except Exception as e:
            print(f"错误: {e}")

        print()  # 轮次之间的空行


if __name__ == "__main__":
    main()