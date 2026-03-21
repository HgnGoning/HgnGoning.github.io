import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

# --- 1. 定义模型路径 ---
# 原始基础模型的路径 (HuggingFace Hub 或本地缓存)
base_model_path = "./models/Qwen/Qwen2.5-7B-Instruct"
# 你训练好的 LoRA 适配器权重路径
lora_adapter_path = "./lora-qwen"

# --- 2. 加载分词器和基础模型 ---
print("正在加载分词器和基础模型...")
tokenizer = AutoTokenizer.from_pretrained(base_model_path, use_fast=False, trust_remote_code=True)
# 确保 pad_token 设置正确
tokenizer.pad_token = tokenizer.eos_token

model = AutoModelForCausalLM.from_pretrained(
    base_model_path,
    torch_dtype=torch.float16,
    device_map="auto", # 自动将模型加载到 GPU
    trust_remote_code=True
)
print("基础模型加载完毕。")

# --- 3. 加载并融合 LoRA 适配器 ---
print(f"正在从 '{lora_adapter_path}' 加载 LoRA 适配器...")
# 使用 PeftModel 加载适配器
model = PeftModel.from_pretrained(model, lora_adapter_path)
print("LoRA 适配器加载完毕。")

# (推荐) 合并模型，提升推理速度
# 这会将 LoRA 权重与基础模型权重合并，之后它就是一个标准的 Transformers 模型
print("正在合并 LoRA 权重...")
model = model.merge_and_unload()
print("权重合并完成。")


# --- 4. 准备输入并进行推理 ---
# !!! 关键：必须使用和训练时完全一样的提示词模板 !!!
instruction = "我是中国人"
# 假设你的任务不需要额外的输入，可以留空
input_text = "" 

# 构造最终的输入文本
prompt = f"""### 指令: {instruction}

### 输入: {input_text}

### 输出: """

print("\n--- 开始推理 ---")
print(f"输入内容:\n{prompt}")

# 使用分词器将文本转换为模型输入
inputs = tokenizer(prompt, return_tensors="pt")
# 将输入数据移动到模型所在的设备 (GPU)
inputs = inputs.to(model.device)

# 生成文本
outputs = model.generate(
    **inputs,
    max_new_tokens=256,      # 最大生成新词元数量
    repetition_penalty=1.1,  # 重复惩罚因子，防止模型重复说话
    do_sample=True,          # 开启采样，让回答更多样
    temperature=0.3,         # 温度，值越低回答越确定，越高越随机
    top_p=0.85,              # Top-p 采样
    top_k=50                 # Top-k 采样
)

# 解码生成的文本
# `outputs[0]` 包含了输入和输出，`skip_special_tokens=True` 会去掉特殊符号
response_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

print("\n--- 推理结果 ---")
# 为了只显示模型新生成的内容，我们可以截取掉输入的部分
# 这种方法更精确
output_only = tokenizer.decode(outputs[0][inputs.input_ids.shape[1]:], skip_special_tokens=True)
print(output_only)

