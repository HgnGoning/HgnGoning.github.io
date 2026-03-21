from typing import List, Dict, Tuple
from openai import OpenAI
import dashscope
from http import HTTPStatus

class BaseModel:
    """
    模型客户端的基类，定义了通用的 chat 接口。
    """
    def __init__(self, api_key: str = '') -> None:
        self.api_key = api_key

    def chat(self, prompt: str, history: List[Dict[str, str]], system_prompt: str = "") -> Tuple[str, List[Dict[str, str]]]:
        """
        基础聊天接口。子类需要实现这个方法。
        
        Args:
            prompt: 当前的用户输入。
            history: 之前的对话历史。
            system_prompt: 系统提示，用于指导模型的行为。
            
        Returns:
            一个元组，包含 (模型响应文本, 更新后的完整对话历史)。
        """
        # 这个 pass 语句意味着基类本身不做任何事，等待子类来实现具体逻辑。
        pass

class Siliconflow(BaseModel):
    """
    使用 Siliconflow 平台 API 的模型客户端。
    """
    def __init__(self, api_key: str):
        super().__init__(api_key)
        # 初始化 OpenAI 客户端，但指向 Siliconflow 的 URL
        self.client = OpenAI(api_key=self.api_key, base_url="https://api.siliconflow.cn/v1")

    def chat(self, prompt: str, history: List[Dict[str, str]] = [], system_prompt: str = "") -> Tuple[str, List[Dict[str, str]]]:
        """
        与 Siliconflow 上的 Qwen 模型进行聊天。
        """
        # 1. 构建消息列表，这是与 OpenAI 兼容 API 对话的标准格式
        messages = [
            # 系统提示总是放在最前面
            {"role": "system", "content": system_prompt or "You are a helpful assistant."}
        ]
        
        # 2. 添加历史消息（如果存在）
        if history:
            messages.extend(history)
        
        # 3. 添加当前的用户消息
        messages.append({"role": "user", "content": prompt})

        # 4. 调用 API
        response = self.client.chat.completions.create(
            model="Qwen/Qwen3-30B-A3B-Instruct-2507",  # 指定要使用的模型
            messages=messages,
            temperature=0.6,    # 控制输出的随机性，0.6 是一个比较均衡的值
            max_tokens=2000,    # 限制模型一次最多生成多少 token
        )

        # 5. 提取模型返回的文本内容
        model_response = response.choices[0].message.content
        
        # 6. 更新对话历史，为下一次对话做准备
        # 这里创建了一个新的列表，包含了本次对话的所有内容（旧历史+新问答）
        # 注意：这里教程的实现是每次都从头构建 history，我们在 agent 中会看到另一种方式
        updated_history = messages[1:] # 去掉 system prompt，只保留对话
        updated_history.append({"role": "assistant", "content": model_response})

        return model_response, updated_history


class DashscopeModel(BaseModel):
    """
    使用阿里云 Dashscope 平台 API 的模型客户端。
    """

    def __init__(self, api_key: str):
        super().__init__(api_key)
        # 设置你的 Dashscope API Key
        dashscope.api_key = self.api_key

    def chat(self, prompt: str, history: List[Dict[str, str]] = [], system_prompt: str = "") -> Tuple[
        str, List[Dict[str, str]]]:
        """
        与 Dashscope 上的通义千问模型进行聊天。
        """
        messages = [
            {'role': 'system', 'content': system_prompt or 'You are a helpful assistant.'}
        ]
        if history:
            messages.extend(history)
        messages.append({'role': 'user', 'content': prompt})

        # 调用 Dashscope 的 API
        response = dashscope.Generation.call(
            model='qwen-long',  # 或者其他你偏好的通义千问模型，如 'qwen-max'
            messages=messages,
            result_format='message',  # 让返回结果包含 message 格式
        )

        # 检查请求是否成功
        if response.status_code == HTTPStatus.OK:
            model_response = response.output.choices[0].message.content

            # 更新历史
            updated_history = messages[1:]
            updated_history.append({'role': 'assistant', 'content': model_response})

            return model_response, updated_history
        else:
            # 如果失败，返回错误信息
            error_message = f"请求失败: Code: {response.status_code}, Message: {response.message}"
            return error_message, history