import json
from collections import Counter
import matplotlib.pyplot as plt

# 读取 JSON 数据
with open('D:\\PDF\\summer_project\\transformer-debugger\\code\\processed_result1.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 初始化计数器和总数
mlp_match_counts = Counter()
attn_match_counts = Counter()
mlp_non_match_counts = Counter()
attn_non_match_counts = Counter()
total_matches = 0
total_non_matches = 0

# 遍历数据
for key, value in data.items():
    is_match = value['answer'] == value["GPT-2's answer"]
    
    if is_match:
        total_matches += 1
    else:
        total_non_matches += 1
    
    # 分别处理 match 和 non-match 的情况
    for i in range(1, 11):
        node_type = value[str(i)]
        
        if 'mlp' in node_type:
            if is_match:
                mlp_match_counts[node_type] += 1
            else:
                mlp_non_match_counts[node_type] += 1
        if 'attn' in node_type:
            if is_match:
                attn_match_counts[node_type] += 1
            else:
                attn_non_match_counts[node_type] += 1

# 计算频率
mlp_match_freq = {k: v / total_matches for k, v in mlp_match_counts.items()}
attn_match_freq = {k: v / total_matches for k, v in attn_match_counts.items()}
mlp_non_match_freq = {k: v / total_non_matches for k, v in mlp_non_match_counts.items()}
attn_non_match_freq = {k: v / total_non_matches for k, v in attn_non_match_counts.items()}

def plot_counts(counter, title):
    # 过滤出频率大于等于 0.01 的条目
    filtered_counter = {k: v for k, v in counter.items() if v >= 0.01}
    
    sorted_counter = dict(sorted(filtered_counter.items(), key=lambda item: item[1], reverse=True))
    
    labels, counts = zip(*sorted_counter.items())
    colors = ['lightblue' if 'mlp' in label else 'lightgreen' for label in labels]  
    
    plt.figure(figsize=(16, 10)) 
    plt.bar(labels, counts, color=colors)
    plt.xticks(rotation=90) 
    for i, count in enumerate(counts):
        plt.text(i, count, f'{count:.4f}', ha='center', va='bottom')
    plt.title(title)
    plt.xlabel('Type')
    plt.ylabel('Frequency')
    plt.tight_layout()  
    plt.show()

# 绘制四张图
plot_counts(mlp_match_freq, "MLP Matching Answers Frequency")
plot_counts(attn_match_freq, "Attention Matching Answers Frequency")
plot_counts(mlp_non_match_freq, "MLP Non-Matching Answers Frequency")
plot_counts(attn_non_match_freq, "Attention Non-Matching Answers Frequency")

