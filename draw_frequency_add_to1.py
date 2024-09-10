import json
from collections import Counter
import matplotlib.pyplot as plt

# 读取 JSON 数据
with open('D:\\PDF\\summer_project\\transformer-debugger\\processed_result.json', 'r', encoding='utf-8') as f:
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
def calculate_frequency(counter, total):
    return {k: v / total for k, v in counter.items()}

mlp_match_freq = calculate_frequency(mlp_match_counts, total_matches)
attn_match_freq = calculate_frequency(attn_match_counts, total_matches)
mlp_non_match_freq = calculate_frequency(mlp_non_match_counts, total_non_matches)
attn_non_match_freq = calculate_frequency(attn_non_match_counts, total_non_matches)

# 归一化处理
def normalize(counter1, counter2):
    total = sum(counter1.values()) + sum(counter2.values())
    normalized_counter1 = {k: v / total for k, v in counter1.items()}
    normalized_counter2 = {k: v / total for k, v in counter2.items()}
    return normalized_counter1, normalized_counter2

mlp_match_freq, attn_match_freq = normalize(mlp_match_freq, attn_match_freq)
mlp_non_match_freq, attn_non_match_freq = normalize(mlp_non_match_freq, attn_non_match_freq)

# 定义绘图函数
def plot_counts(counter, title):
    sorted_counter = dict(sorted(counter.items(), key=lambda item: item[1], reverse=True))
    
    labels, counts = zip(*sorted_counter.items())
    colors = ['lightblue' if 'mlp' in label else 'lightgreen' for label in labels]  
    
    plt.figure(figsize=(16, 10)) 
    plt.bar(labels, counts, color=colors)
    plt.xticks(rotation=90) 
    for i, count in enumerate(counts):
        plt.text(i, count, f'{count:.2f}', ha='center', va='bottom')
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
