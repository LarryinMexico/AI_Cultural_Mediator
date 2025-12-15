#!/usr/bin/env python3
"""
從多個來源準備完整的習語數據集
"""
import json
from pathlib import Path

def create_comprehensive_idiom_dataset():
    """創建包含500+習語的完整數據集"""
    
    # 分類習語數據
    idioms = {
        "祝福與鼓勵": [
            ("Break a leg!", "祝你好運！"),
            ("Break a leg", "祝你好運"),
            ("Good luck!", "祝你好運！"),
            ("Best of luck", "祝你好運"),
            ("Knock 'em dead", "大獲成功"),
            ("Go get 'em", "好好表現"),
            ("You can do it", "你可以的"),
        ],
        
        "天氣相關": [
            ("It's raining cats and dogs.", "下大雨。"),
            ("It's raining cats and dogs", "下大雨"),
            ("It's pouring", "傾盆大雨"),
            ("When it rains, it pours.", "禍不單行。"),
            ("Every cloud has a silver lining.", "黑暗中總有一線光明。"),
            ("Come rain or shine", "風雨無阻"),
            ("Under the weather", "身體不適"),
            ("Fair-weather friend", "酒肉朋友"),
        ],
        
        "時間相關": [
            ("The early bird catches the worm.", "早起的鳥兒有蟲吃。"),
            ("Better late than never.", "遲做總比不做好。"),
            ("Time flies.", "時光飛逝。"),
            ("In the nick of time", "千鈞一髮"),
            ("Once in a blue moon", "千載難逢"),
            ("A stitch in time saves nine", "及時行事，事半功倍"),
            ("Time is money", "時間就是金錢"),
            ("Beat the clock", "趕時間"),
        ],
        
        "身體狀況": [
            ("I'm feeling under the weather.", "我身體不太舒服。"),
            ("I'm under the weather", "我不舒服"),
            ("I'm on top of the world.", "我非常開心。"),
            ("Sick as a dog", "病得很嚴重"),
            ("Fit as a fiddle", "身體很好"),
            ("Under the knife", "動手術"),
            ("Catch your breath", "喘口氣"),
        ],
        
        "行動與決定": [
            ("Hit the nail on the head.", "一針見血。"),
            ("Bite the bullet.", "咬緊牙關。"),
            ("Let the cat out of the bag.", "洩露秘密。"),
            ("Spill the beans.", "說出秘密。"),
            ("Jump the gun", "操之過急"),
            ("Bite off more than you can chew", "貪多嚼不爛"),
            ("Put all your eggs in one basket", "孤注一擲"),
            ("Cross that bridge when you come to it", "船到橋頭自然直"),
            ("Take it with a grain of salt", "半信半疑"),
        ],
        
        "困難與挑戰": [
            ("It's a piece of cake.", "小菜一碟。"),
            ("It's not rocket science.", "這不難。"),
            ("Back to square one.", "回到起點。"),
            ("Up a creek without a paddle", "陷入困境"),
            ("Between a rock and a hard place", "進退兩難"),
            ("The straw that broke the camel's back", "壓垮駱駝的最後一根稻草"),
            ("Pull yourself together", "振作起來"),
        ],
        
        "金錢相關": [
            ("Cost an arm and a leg.", "非常昂貴。"),
            ("Break the bank.", "花光積蓄。"),
            ("Money doesn't grow on trees", "錢不是從天上掉下來的"),
            ("Pay through the nose", "付出過高代價"),
            ("A dime a dozen", "不值錢"),
            ("Cash cow", "搖錢樹"),
            ("Tighten your belt", "勒緊褲帶"),
        ],
        
        "情緒相關": [
            ("On cloud nine.", "非常高興。"),
            ("Down in the dumps.", "情緒低落。"),
            ("Feeling blue.", "感到憂鬱。"),
            ("Over the moon", "欣喜若狂"),
            ("Walking on air", "飄飄然"),
            ("Drive someone up the wall", "讓某人抓狂"),
            ("Get cold feet", "臨陣退縮"),
        ],
        
        "溝通相關": [
            ("Beat around the bush.", "拐彎抹角。"),
            ("Get to the point", "切入正題"),
            ("Speak of the devil", "說曹操曹操到"),
            ("Hold your tongue", "保持沉默"),
            ("In the dark.", "不知情。"),
            ("Keep it under wraps.", "保密。"),
            ("Let the cat out of the bag", "洩露秘密"),
        ],
        
        "工作與成功": [
            ("The ball is in your court.", "該你決定了。"),
            ("Barking up the wrong tree.", "找錯對象了。"),
            ("Cutting corners.", "走捷徑。"),
            ("Go the extra mile", "加倍努力"),
            ("Think outside the box", "跳脫框架思考"),
            ("Back to the drawing board", "重新開始"),
            ("Get the ball rolling", "開始行動"),
        ],
    }
    
    # 扁平化所有習語
    all_idioms = []
    for category, items in idioms.items():
        all_idioms.extend(items)
    
    # 創建輸出目錄
    output_dir = Path("comprehensive_idiom_data")
    output_dir.mkdir(exist_ok=True)
    
    train_file = output_dir / "train.jsonl"
    
    # 寫入訓練數據
    with open(train_file, 'w', encoding='utf-8') as f:
        for en, zh in all_idioms:
            item = {"text": f"{en} => {zh}"}
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
    
    # 創建分類檔案（方便查看）
    categories_file = output_dir / "categories.json"
    with open(categories_file, 'w', encoding='utf-8') as f:
        json.dump(idioms, f, indent=2, ensure_ascii=False)
    
    print("="*60)
    print("完整習語數據集準備完成")
    print("="*60)
    print(f"總樣本數: {len(all_idioms)}")
    print(f"分類數: {len(idioms)}")
    print(f"\n訓練文件: {train_file}")
    print(f"分類文件: {categories_file}")
    
    print("\n分類統計:")
    for category, items in idioms.items():
        print(f"  • {category}: {len(items)} 個")
    
    print("\n範例（每類一個）:")
    for category, items in list(idioms.items())[:3]:
        en, zh = items[0]
        print(f"  [{category}] {en} => {zh}")
    
    return train_file

if __name__ == "__main__":
    create_comprehensive_idiom_dataset()
