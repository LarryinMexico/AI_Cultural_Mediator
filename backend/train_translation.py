#!/usr/bin/env python3
"""
使用 MLX LoRA 微調翻譯模型
"""
import os
import json
import mlx.core as mx
import mlx_lm
from pathlib import Path
import logging
from datetime import datetime
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TrainingLogger:
    """記錄訓練過程以便後續視覺化"""
    def __init__(self, log_dir="training_logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # 創建時間戳
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = self.log_dir / f"training_{timestamp}.jsonl"
        self.summary_file = self.log_dir / f"summary_{timestamp}.json"
        
        self.start_time = time.time()
        self.logs = []
        
        logger.info(f"📊 訓練日誌將保存到: {self.log_file}")
    
    def log_step(self, step, loss, learning_rate, **kwargs):
        """記錄訓練步驟"""
        log_entry = {
            "step": step,
            "loss": float(loss),
            "learning_rate": float(learning_rate),
            "timestamp": datetime.now().isoformat(),
            "elapsed_time": time.time() - self.start_time,
            **kwargs
        }
        
        self.logs.append(log_entry)
        
        # 即時寫入
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry) + '\n')
    
    def save_summary(self, config, final_metrics):
        """保存訓練摘要"""
        summary = {
            "config": config,
            "final_metrics": final_metrics,
            "total_time": time.time() - self.start_time,
            "num_steps": len(self.logs),
            "start_time": datetime.fromtimestamp(self.start_time).isoformat(),
            "end_time": datetime.now().isoformat()
        }
        
        with open(self.summary_file, 'w', encoding='utf-8') as f:
            json.dumps(summary, f, indent=2, ensure_ascii=False)
        
        logger.info(f"✅ 訓練摘要已保存: {self.summary_file}")

def train_translation_model():
    """使用 MLX LoRA 微調模型"""
    
    print("=" * 60)
    print("開始微調翻譯模型")
    print("=" * 60)
    
    # 配置
    config = {
        "model": "Qwen/Qwen2.5-3B-Instruct",
        "data": "training_data_dir",  # 目錄路徑
        "adapter_path": "adapters/translation",
        "iters": 1000,  # 迭代次數（可調整）
        "learning_rate": 1e-4,
        "steps_per_report": 50,
        "save_every": 100,
        "lora_layers": 16,  # LoRA 層數
        "batch_size": 2,    # 批次大小（3B 模型建議用小批次）
    }
    
    print("\n📋 訓練配置：")
    for key, value in config.items():
        print(f"  {key}: {value}")
    
    # 檢查數據目錄
    if not Path(config["data"]).exists():
        print(f"\n❌ 找不到訓練數據目錄: {config['data']}")
        print("請先運行: python prepare_training_data.py")
        return
    
    # 創建輸出目錄
    Path(config["adapter_path"]).parent.mkdir(parents=True, exist_ok=True)
    
    print("\n🚀 開始訓練...")
    print("⏰ 預計時間: 1-2 小時 (取決於硬體)")
    print()
    
    try:
        # 使用 MLX LoRA 訓練
        # 這裡需要使用 mlx-lm 的 CLI 或 API
        # 由於 mlx-lm 主要通過 CLI 使用，我們用 subprocess
        import subprocess
        
        cmd = [
            "python", "-m", "mlx_lm", "lora",
            "--model", config["model"],
            "--train",
            "--data", config["data"],
            "--iters", str(config["iters"]),
            "--learning-rate", str(config["learning_rate"]),
            "--num-layers", str(config["lora_layers"]),
            "--batch-size", str(config["batch_size"]),
            "--steps-per-report", str(config["steps_per_report"]),
            "--save-every", str(config["save_every"]),
            "--adapter-path", config["adapter_path"],
        ]
        
        # MLX LoRA 不支持 valid-data，移除此部分
        # if Path(config["valid_data"]).exists():
        #     cmd.extend(["--valid-data", config["valid_data"]])
        #     cmd.extend(["--val-batches", str(config["val_batches"])])
        
        print("執行命令:")
        print(" ".join(cmd))
        print()
        
        result = subprocess.run(cmd)
        
        if result.returncode == 0:
            print("\n" + "=" * 60)
            print("✅ 訓練完成！")
            print("=" * 60)
            print(f"\nAdapter 已保存到: {config['adapter_path']}")
            print("\n下一步：")
            print("1. 測試微調後的模型")
            print("2. 整合到專案中")
        else:
            print("\n❌ 訓練失敗")
            
    except Exception as e:
        logger.error(f"訓練錯誤: {e}")
        print("\n如果遇到問題，可以手動運行：")
        print(f"python -m mlx_lm.lora --model {config['model']} --train --data {config['data']} --iters {config['iters']}")

def test_finetuned_model():
    """測試微調後的模型"""
    print("\n測試微調後的模型...")
    
    adapter_path = "adapters/translation"
    if not Path(adapter_path).exists():
        print(f"❌ 找不到 adapter: {adapter_path}")
        return
    
    # 載入模型和 adapter
    print("載入模型...")
    model, tokenizer = mlx_lm.load("Qwen/Qwen2.5-3B-Instruct")
    
    # TODO: 載入 adapter
    # 這需要 mlx-lm 的 adapter 載入功能
    
    # 測試翻譯
    test_texts = [
        "Hello, how are you?",
        "Break a leg!",
        "It's raining cats and dogs.",
    ]
    
    for text in test_texts:
        prompt = f"Translate this English text to Traditional Chinese (繁體中文). Output ONLY the translation, nothing else.\n\nEnglish: {text}\nTraditional Chinese (繁體中文):"
        
        response = mlx_lm.generate(model, tokenizer, prompt=prompt, max_tokens=50, verbose=False)
        
        print(f"\nEN: {text}")
        print(f"ZH: {response.strip()}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test_finetuned_model()
    else:
        train_translation_model()
