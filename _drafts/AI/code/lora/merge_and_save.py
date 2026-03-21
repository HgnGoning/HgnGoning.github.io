import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
import os

# --- 1. 定义模型路径 ---
# 基础模型路径 (必须是你本地下载好的路径)
base_model_path = "./models/Qwen/Qwen2.5-7B-Instruct"
# 你训练好的 LoRA 适配器权重路径
lora_adapter_path = "./lora-qwen"
# 定义合并后新模型的保存路径
merged_model_path = "./merged_qwen_model"

print("--- 开始加载基础模型和分词器 ---")
# 加载基础模型
model = AutoModelForCausalLM.from_pretrained(
    base_model_path,
    torch_dtype=torch.float16,
    device_map="auto",
    trust_remote_code=True
)
# 加载分词器
tokenizer = AutoTokenizer.from_pretrained(base_model_path, trust_remote_code=True)

print("--- 开始加载并融合 LoRA 适配器 ---")
# 使用 PeftModel 加载适配器
model = PeftModel.from_pretrained(model, lora_adapter_path)

# --- 核心步骤：合并 LoRA 权重并卸载 ---
print("--- 正在合并 LoRA 权重... ---")
model = model.merge_and_unload()
print("--- 权重合并完成 ---")


# --- 保存合并后的完整模型和分词器 ---
print(f"--- 正在将完整模型保存到 '{merged_model_path}' ---")
if not os.path.exists(merged_model_path):
    os.makedirs(merged_model_path)

model.save_pretrained(merged_model_path)
tokenizer.save_pretrained(merged_model_path)

print("--- 恭喜！模型已成功合并并保存。---")
print(f"现在你可以在 '{merged_model_path}' 文件夹中找到一个独立的、可直接用于推理的模型。")

