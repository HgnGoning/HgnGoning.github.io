from typing import List, Dict, Any
import json
import requests

class ReactTools:
    """
    React Agent 工具类。
    管理所有可用的工具，提供描述信息和执行方法。
    """
    def __init__(self, serper_api_key: str) -> None:
        """
        初始化工具类。
        Args:
            serper_api_key: 用于 Google 搜索的 Serper API Key。
        """
        self.serper_api_key = serper_api_key
        # 在初始化时，就构建好所有工具的配置信息
        self.tool_config = self._build_tool_config()
    
    def _build_tool_config(self) -> List[Dict[str, Any]]:
        """
        构建所有工具的描述信息，这是给大模型“阅读”的。
        """
        # 目前只有一个工具，但设计成了列表，方便未来扩展
        return [
            {
                'name_for_human': '谷歌搜索',
                'name_for_model': 'google_search',
                'description_for_model': '谷歌搜索是一个通用搜索引擎，可用于访问互联网、查询百科知识、了解时事新闻等。当你需要最新的信息或不确定的知识时，应该使用它。',
                'parameters': [
                    {
                        'name': 'search_query',
                        'description': '需要搜索的关键词或问题。',
                        'required': True,
                        'schema': {'type': 'string'},
                    }
                ],
            },
            # --- 新增的 Mcp 工具描述 ---
            {
                'name_for_human': '数学计算器',
                'name_for_model': 'mcp_tool',
                'description_for_model': '一个简单的数学计算工具，可以执行加、减、乘、除等基本的数学运算。',
                'parameters': [
                    {'name': 'expression', 'description': '要计算的数学表达式字符串，例如 "100 * (2 + 5)"。', 'required': True, 'schema': {'type': 'string'}},
                ],
            }
        ]

    def google_search(self, search_query: str) -> str:
        """
        执行谷歌搜索的实际函数。
        """
        url = "https://google.serper.dev/search"
        # 构造请求体和头部
        payload = json.dumps({"q": search_query})
        headers = {
            'X-API-KEY': self.serper_api_key,
            'Content-Type': 'application/json'
        }
        
        try:
            response = requests.request("POST", url, headers=headers, data=payload)
            response.raise_for_status() # 如果请求失败（如4XX, 5XX错误），会抛出异常
            
            # 解析返回的JSON数据
            search_results = response.json()
            
            # 提取和格式化搜索结果，让模型更容易理解
            # 我们只提取关键信息，避免太多无关内容干扰模型
            if "organic" in search_results:
                snippets = []
                for result in search_results["organic"][:5]: # 只取前5个结果
                    snippets.append(f"- 标题: {result.get('title', 'N/A')}\n  链接: {result.get('link', 'N/A')}\n  摘要: {result.get('snippet', 'N/A')}")
                return "\n".join(snippets)
            else:
                return "没有找到相关的搜索结果。"
        except requests.exceptions.RequestException as e:
            return f"搜索请求失败: {e}"
        except json.JSONDecodeError:
            return "解析搜索结果失败，返回的不是有效的JSON格式。"

    # --- 新增的 Mcp 工具实现 ---
    def mcp_tool(self, expression: str) -> str:
        """
        执行数学表达式计算。
        警告：eval() 函数存在安全风险，此处仅为教学演示。
        在生产环境中，应使用更安全的数学表达式解析库。
        """
        try:
            # 使用 Python 的 eval 函数直接计算表达式字符串
            result = eval(expression)
            return f"计算结果是: {result}"
        except Exception as e:
            return f"数学表达式计算错误: {e}"

    def get_available_tools(self) -> List[str]:
        """
        获取所有可用工具的名称列表。
        """
        return [tool['name_for_model'] for tool in self.tool_config]

    def get_tool_description(self) -> str:
        """
        生成所有工具的格式化描述字符串，用于插入到 System Prompt 中。
        """
        # 使用 json.dumps 来确保格式是标准的 JSON，模型更容易解析
        return json.dumps(self.tool_config, indent=2, ensure_ascii=False)
