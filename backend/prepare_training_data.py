#!/usr/bin/env python3
"""
下載和準備 WMT 翻譯訓練數據
"""
import os
import json
from datasets import load_dataset
from pathlib import Path

def download_wmt_data():
    """下載 WMT19 英中翻譯數據"""
    print("=" * 60)
    print("下載 WMT19 英中翻譯數據集")
    print("=" * 60)
    
    try:
        print("\n正在下載數據集... (這可能需要幾分鐘)")
        # WMT19 中英翻譯數據
        dataset = load_dataset("wmt19", "zh-en", split="train", trust_remote_code=True)
        
        print(f"數據集下載完成!")
        print(f"   總樣本數: {len(dataset)}")
        
        # 顯示範例
        print("\n數據範例：")
        for i in range(min(3, len(dataset))):
            translation = dataset[i]['translation']
            print(f"\n  {i+1}. EN: {translation['en']}")
            print(f"     ZH: {translation['zh']}")
        
        return dataset
        
    except Exception as e:
        print(f"\n下載失敗: {e}")
        print("\n嘗試替代數據集...")
        return download_opus_data()

def download_opus_data():
    """下載 OPUS-100 作為備選"""
    print("\n正在下載 OPUS-100 數據集...")
    try:
        dataset = load_dataset("Helsinki-NLP/opus-100", "en-zh", split="train")
        print(f"數據集下載完成!")
        print(f"   總樣本數: {len(dataset)}")
        
        # 顯示範例
        print("\n數據範例：")
        for i in range(min(3, len(dataset))):
            translation = dataset[i]['translation']
            print(f"\n  {i+1}. EN: {translation['en']}")
            print(f"     ZH: {translation['zh']}")
        
        return dataset
    except Exception as e:
        print(f"下載失敗: {e}")
        return None

def prepare_training_data(dataset, output_file, max_samples=10000):
    """將數據轉換為 MLX 訓練格式"""
    print(f"\n準備訓練數據 (限制 {max_samples} 樣本)...")
    
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    count = 0
    with open(output_path, 'w', encoding='utf-8') as f:
        for item in dataset:
            if count >= max_samples:
                break
            
            # 獲取翻譯對
            translation = item['translation']
            en_text = translation['en'].strip()
            zh_text = translation['zh'].strip()
            
            # 過濾太長或太短的句子
            if len(en_text) < 5 or len(en_text) > 200:
                continue
            if len(zh_text) < 2 or len(zh_text) > 200:
                continue
            
            # 創建訓練格式 - MLX LoRA 需要 'text' 字段
            training_item = {
                "text": f"{en_text} => {zh_text}"
            }
            
            f.write(json.dumps(training_item, ensure_ascii=False) + '\n')
            count += 1
    
    print(f"訓練數據已保存到: {output_path}")
    print(f"   共 {count} 個樣本")
    
    return output_path

def create_validation_data(dataset, output_file, num_samples=500):
    """創建驗證數據集"""
    print(f"\n準備驗證數據...")
    
    output_path = Path(output_file)
    
    count = 0
    with open(output_path, 'w', encoding='utf-8') as f:
        # 從後面取樣本作為驗證集
        start_idx = len(dataset) - num_samples - 100
        for i in range(start_idx, start_idx + num_samples):
            if i >= len(dataset):
                break
                
            translation = dataset[i]['translation']
            en_text = translation['en'].strip()
            zh_text = translation['zh'].strip()
            
            if len(en_text) < 5 or len(en_text) > 200:
                continue
            if len(zh_text) < 2 or len(zh_text) > 200:
                continue
            
            validation_item = {
                "prompt": f"Translate this English text to Traditional Chinese (繁體中文). Output ONLY the translation, nothing else.\n\nEnglish: {en_text}\nTraditional Chinese (繁體中文):",
                "completion": zh_text
            }
            
            f.write(json.dumps(validation_item, ensure_ascii=False) + '\n')
            count += 1
    
    print(f"驗證數據已保存到: {output_path}")
    print(f"   共 {count} 個樣本")

def main():
    print("開始下載和準備訓練數據")
    print()
    
    # 1. 下載數據集
    dataset = download_wmt_data()
    
    if dataset is None:
        print("\n無法下載數據集，請檢查網路連接")
        return
    
    # 2. 準備訓練數據
    train_file = prepare_training_data(
        dataset, 
        "training_data/translation_train.jsonl",
        max_samples=10000  # 先用 1萬個樣本測試
    )
    
    # 3. 準備驗證數據
    create_validation_data(
        dataset,
        "training_data/translation_valid.jsonl",
        num_samples=500
    )
    
    print("\n" + "=" * 60)
    print("數據準備完成！")
    print("=" * 60)
    print("\n下一步：")
    print("1. 先測試 3B 模型的翻譯效果")
    print("2. 運行微調訓練：python train_translation.py")
    print("3. 評估微調後的模型")
    print()
    print("文件位置：")
    print(f"  訓練數據: training_data/translation_train.jsonl")
    print(f"  驗證數據: training_data/translation_valid.jsonl")

if __name__ == "__main__":
    main()
