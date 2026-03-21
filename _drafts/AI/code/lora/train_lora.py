import torch
from datasets import load_dataset
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    TrainingArguments,
    Trainer,
)
from peft import get_peft_model, LoraConfig

# 添加 ModelScope 支持
try:
    from modelscope import snapshot_download
    from modelscope.hub.snapshot_download import snapshot_download
    MODELSCOPE_AVAILABLE = True
except ImportError:
    MODELSCOPE_AVAILABLE = False

model_name = "Qwen/Qwen2.5-7B-Instruct"

# 尝试从 ModelScope 下载模型
def get_model_path(model_name):
    if MODELSCOPE_AVAILABLE:
        try:
            print("正在从 ModelScope 下载模型...")
            model_path = snapshot_download(model_name, cache_dir="./models")
            return model_path
        except Exception as e:
            print(f"ModelScope 下载失败: {e}, 尝试从 HuggingFace 下载")
    
    # 如果 ModelScope 不可用或下载失败，则使用原始方法
    return model_name

# 获取模型路径
model_path = get_model_path(model_name)

tokenizer = AutoTokenizer.from_pretrained(model_path, use_fast=False)
tokenizer.pad_token = tokenizer.eos_token

dataset = load_dataset("json", data_files="train.json")

def preprocess(example):
    text = f"""### 指令:
{example['instruction']}

### 输入:
{example['input']}

### 输出:
{example['output']}"""
    tokenized = tokenizer(
        text,
        truncation=True,
        padding="max_length",
        max_length=512,
    )
    tokenized["labels"] = tokenized["input_ids"].copy()
    return tokenized

dataset = dataset.map(preprocess, remove_columns=dataset["train"].column_names)

model = AutoModelForCausalLM.from_pretrained(
    model_path,
    torch_dtype=torch.float16,
    device_map="auto"
)

lora_config = LoraConfig(
    r=8,
    lora_alpha=32,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)

model = get_peft_model(model, lora_config)

training_args = TrainingArguments(
    output_dir="./lora-qwen",
    per_device_train_batch_size=2,
    gradient_accumulation_steps=4,
    learning_rate=2e-4,
    num_train_epochs=3,
    fp16=True,
    logging_steps=10,
    save_steps=45,
    save_total_limit=2,
    report_to="none"
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset["train"]
)

# 启动训练
print("--- 开始训练 ---")
trainer.train()
print("--- 训练结束 ---")

# ！！！确保下面这行代码绝对存在！！！
print("--- 正在保存最终模型 ---")
trainer.save_model()
print("--- 模型保存完毕 ---")
