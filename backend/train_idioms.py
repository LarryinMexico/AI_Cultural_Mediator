#!/usr/bin/env python3
"""
在第一次微調的基礎上繼續訓練習語
這會在現有 adapter 基礎上優化，而不是創建新的 adapter
"""
import subprocess
from pathlib import Path

print("="*60)
print("第二次微調：習語專門訓練")
print("="*60)

config = {
    "model": "Qwen/Qwen2.5-3B-Instruct",
    "data": "idiom_training_data",  # 習語數據
    "resume_adapter": "adapters/translation/adapters.safetensors",  # 從第一次微調結果繼續
    "adapter_path": "adapters/translation_v2",  # 保存到新位置（保留 v1）
    "iters": 200,  # 習語數據較少，200次就夠
    "learning_rate": 5e-5,  # 較小的學習率，避免忘記之前學到的
    "batch_size": 2,
    "steps_per_report": 20,
    "save_every": 50,
    "num_layers": 16,
}

print("\n📋 訓練配置：")
for key, value in config.items():
    print(f"  {key}: {value}")

print("\n⚠️  重要說明：")
print("  • 這是在第一次微調基礎上繼續訓練")
print("  • 會保留原有的翻譯能力")
print("  • 額外學習習語的意譯")
print("  • 原 adapter 保留在 adapters/translation/")
print("  • 新 adapter 保存到 adapters/translation_v2/")

response = input("\n是否開始訓練？(y/n): ")
if response.lower() != 'y':
    print("已取消")
    exit(0)

print("\n🚀 開始訓練...")

cmd = [
    "python", "-m", "mlx_lm", "lora",
    "--model", config["model"],
    "--train",
    "--data", config["data"],
    "--resume-adapter-file", config["resume_adapter"],
    "--adapter-path", config["adapter_path"],
    "--iters", str(config["iters"]),
    "--learning-rate", str(config["learning_rate"]),
    "--num-layers", str(config["num_layers"]),
    "--batch-size", str(config["batch_size"]),
    "--steps-per-report", str(config["steps_per_report"]),
    "--save-every", str(config["save_every"]),
]

print("\n執行命令:")
print(" ".join(cmd))
print()

result = subprocess.run(cmd)

if result.returncode == 0:
    print("\n" + "="*60)
    print("✅ 第二次微調完成！")
    print("="*60)
    print(f"\n新 Adapter: {config['adapter_path']}")
    print("\n現在你有兩個版本:")
    print("  • V1 (adapters/translation/): 基礎翻譯")
    print("  • V2 (adapters/translation_v2/): 基礎翻譯 + 習語")
    print("\n測試方法:")
    print("  python test_models_sequential.py finetuned  # V1")
    print("  # 修改腳本 adapter_path 為 translation_v2 測試 V2")
else:
    print("\n❌ 訓練失敗")
