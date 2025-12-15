#!/usr/bin/env python3
"""
準備習語和俚語翻譯數據
"""
import json
from pathlib import Path

def create_idiom_dataset():
    """創建習語翻譯數據集"""
    
    # 常見英文習語及其意譯
    idioms_data = [
        # 祝福類
        ("Break a leg!", "祝你好運！"),
        ("Break a leg", "祝你好運"),
        ("Good luck!", "祝你好運！"),
        
        # 天氣相關
        ("It's raining cats and dogs.", "下大雨了。"),
        ("It's raining cats and dogs", "下大雨"),
        ("When it rains, it pours.", "禍不單行。"),
        
        # 時間相關
        ("The early bird catches the worm.", "早起的鳥兒有蟲吃。"),
        ("Better late than never.", "遲做總比不做好。"),
        ("Time flies.", "時光飛逝。"),
        
        # 身體狀況
        ("I'm feeling under the weather.", "我身體不太舒服。"),
        ("I'm under the weather", "我不舒服"),
        ("I'm on top of the world.", "我非常開心。"),
        
        # 行動相關
        ("Hit the nail on the head.", "一針見血。"),
        ("Bite the bullet.", "咬緊牙關。"),
        ("Let the cat out of the bag.", "洩露秘密。"),
        ("Spill the beans.", "說出秘密。"),
        
        # 困難相關
        ("It's a piece of cake.", "小菜一碟。"),
        ("It's not rocket science.", "這不難。"),
        ("Back to square one.", "回到起點。"),
        
        # 金錢相關
        ("Cost an arm and a leg.", "非常昂貴。"),
        ("Break the bank.", "花光積蓄。"),
        
        # 情緒相關
        ("On cloud nine.", "非常高興。"),
        ("Down in the dumps.", "情緒低落。"),
        ("Feeling blue.", "感到憂鬱。"),
        
        # 秘密相關
        ("In the dark.", "不知情。"),
        ("Keep it under wraps.", "保密。"),
        
        # 其他常用
        ("Beat around the bush.", "拐彎抹角。"),
        ("Cutting corners.", "走捷徑。"),
        ("Once in a blue moon.", "千載難逢。"),
        ("The ball is in your court.", "該你決定了。"),
        ("Barking up the wrong tree.", "找錯對象了。"),
    ]
    
    # 創建訓練數據
    output_dir = Path("idiom_training_data")
    output_dir.mkdir(exist_ok=True)
    
    train_file = output_dir / "train.jsonl"
    
    with open(train_file, 'w', encoding='utf-8') as f:
        for en, zh in idioms_data:
            # 使用與之前相同的格式
            item = {"text": f"{en} => {zh}"}
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
    
    print("="*60)
    print("習語訓練數據準備完成")
    print("="*60)
    print(f"數據文件: {train_file}")
    print(f"樣本數: {len(idioms_data)}")
    print("\n範例:")
    for i, (en, zh) in enumerate(idioms_data[:5]):
        print(f"  {i+1}. {en} => {zh}")
    
    print("\n下一步:")
    print("1. 在第一次微調的基礎上繼續訓練（推薦）")
    print("2. 或者混合 WMT 數據和習語數據重新訓練")
    
    return train_file

if __name__ == "__main__":
    create_idiom_dataset()
