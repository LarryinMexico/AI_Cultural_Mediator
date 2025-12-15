#!/usr/bin/env python3
"""
視覺化訓練日誌
"""
import json
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # 使用非互動式後端
from pathlib import Path
import argparse

def load_training_log(log_file):
    """載入訓練日誌"""
    logs = []
    with open(log_file, 'r', encoding='utf-8') as f:
        for line in f:
            logs.append(json.loads(line))
    return logs

def plot_training_curves(logs, output_dir="training_plots"):
    """繪製訓練曲線"""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    steps = [log['step'] for log in logs]
    losses = [log['loss'] for log in logs]
    elapsed_times = [log['elapsed_time'] / 60 for log in logs]  # 轉換為分鐘
    
    # 1. Loss 曲線
    plt.figure(figsize=(10, 6))
    plt.plot(steps, losses, 'b-', linewidth=2)
    plt.xlabel('Training Step', fontsize=12)
    plt.ylabel('Loss', fontsize=12)
    plt.title('Training Loss Over Time', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    loss_plot = output_dir / 'loss_curve.png'
    plt.savefig(loss_plot, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✅ Loss 曲線已保存: {loss_plot}")
    
    # 2. Loss vs 時間
    plt.figure(figsize=(10, 6))
    plt.plot(elapsed_times, losses, 'r-', linewidth=2)
    plt.xlabel('Training Time (minutes)', fontsize=12)
    plt.ylabel('Loss', fontsize=12)
    plt.title('Training Loss vs Time', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    time_plot = output_dir / 'loss_vs_time.png'
    plt.savefig(time_plot, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✅ 時間曲線已保存: {time_plot}")
    
    # 3. 學習率曲線（如果有記錄）
    if 'learning_rate' in logs[0]:
        learning_rates = [log['learning_rate'] for log in logs]
        plt.figure(figsize=(10, 6))
        plt.plot(steps, learning_rates, 'g-', linewidth=2)
        plt.xlabel('Training Step', fontsize=12)
        plt.ylabel('Learning Rate', fontsize=12)
        plt.title('Learning Rate Schedule', fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        lr_plot = output_dir / 'learning_rate.png'
        plt.savefig(lr_plot, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✅ 學習率曲線已保存: {lr_plot}")
    
    # 4. 綜合視圖
    fig, axes = plt.subplots(2, 1, figsize=(12, 10))
    
    # Loss
    axes[0].plot(steps, losses, 'b-', linewidth=2)
    axes[0].set_xlabel('Step', fontsize=11)
    axes[0].set_ylabel('Loss', fontsize=11)
    axes[0].set_title('Training Loss', fontsize=12, fontweight='bold')
    axes[0].grid(True, alpha=0.3)
    
    # 時間
    axes[1].plot(elapsed_times, losses, 'r-', linewidth=2)
    axes[1].set_xlabel('Time (minutes)', fontsize=11)
    axes[1].set_ylabel('Loss', fontsize=11)
    axes[1].set_title('Loss vs Time', fontsize=12, fontweight='bold')
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    combined_plot = output_dir / 'training_overview.png'
    plt.savefig(combined_plot, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✅ 綜合視圖已保存: {combined_plot}")
    
    return {
        'loss_curve': loss_plot,
        'time_curve': time_plot,
        'overview': combined_plot
    }

def print_statistics(logs):
    """輸出訓練統計"""
    losses = [log['loss'] for log in logs]
    
    print("\n" + "=" * 60)
    print("訓練統計")
    print("=" * 60)
    print(f"總步數: {len(logs)}")
    print(f"初始 Loss: {losses[0]:.4f}")
    print(f"最終 Loss: {losses[-1]:.4f}")
    print(f"最低 Loss: {min(losses):.4f}")
    print(f"Loss 改善: {losses[0] - losses[-1]:.4f} ({((losses[0] - losses[-1]) / losses[0] * 100):.1f}%)")
    
    if logs[-1].get('elapsed_time'):
        total_time = logs[-1]['elapsed_time']
        print(f"訓練時間: {total_time / 60:.1f} 分鐘")
        print(f"平均每步: {total_time / len(logs):.2f} 秒")
    
    print("=" * 60)

def main():
    parser = argparse.ArgumentParser(description='視覺化訓練日誌')
    parser.add_argument('--log-file', type=str, help='訓練日誌文件路徑')
    parser.add_argument('--log-dir', type=str, default='training_logs', help='日誌目錄')
    parser.add_argument('--output-dir', type=str, default='training_plots', help='輸出圖表目錄')
    
    args = parser.parse_args()
    
    # 找到最新的日誌文件
    if args.log_file:
        log_file = Path(args.log_file)
    else:
        log_dir = Path(args.log_dir)
        if not log_dir.exists():
            print(f"❌ 找不到日誌目錄: {log_dir}")
            return
        
        log_files = list(log_dir.glob('training_*.jsonl'))
        if not log_files:
            print(f"❌ 找不到訓練日誌文件")
            return
        
        log_file = max(log_files, key=lambda p: p.stat().st_mtime)
        print(f"📊 使用最新日誌: {log_file}")
    
    # 載入並視覺化
    logs = load_training_log(log_file)
    print(f"✅ 載入了 {len(logs)} 條記錄")
    
    # 輸出統計
    print_statistics(logs)
    
    # 繪製圖表
    plots = plot_training_curves(logs, args.output_dir)
    
    print(f"\n✅ 所有圖表已保存到: {args.output_dir}")
    print("\n視覺化完成！")

if __name__ == "__main__":
    main()
