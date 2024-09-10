import json
from collections import Counter
import matplotlib.pyplot as plt

# 读取 JSON 数据
with open('D:\\PDF\\summer_project\\transformer-debugger\\processed_result.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 初始化计数器
mlp_match_counts = Counter()
attn_match_counts = Counter()
mlp_non_match_counts = Counter()
attn_non_match_counts = Counter()

# 遍历数据
for key, value in data.items():
    is_match = value['answer'] == value["GPT-2's answer"]
    
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

# 计算答对答错的分布差分
def calculate_difference(match_counts, non_match_counts):
    difference = Counter()
    all_keys = set(match_counts.keys()).union(non_match_counts.keys())
    for key in all_keys:
        difference[key] = match_counts[key] - non_match_counts.get(key, 0)
    return difference

# 计算 MLP 和 Attention 节点的差分
mlp_difference = calculate_difference(mlp_match_counts, mlp_non_match_counts)
attn_difference = calculate_difference(attn_match_counts, attn_non_match_counts)

# 定义绘图函数
def plot_difference(counter, title):
    sorted_counter = dict(sorted(counter.items(), key=lambda item: item[1], reverse=True))
    
    labels, counts = zip(*sorted_counter.items())
    colors = ['lightblue' if 'mlp' in label else 'lightgreen' for label in labels]  
    
    plt.figure(figsize=(16, 10)) 
    plt.bar(labels, counts, color=colors)
    plt.xticks(rotation=90) 
    for i, count in enumerate(counts):
        plt.text(i, count, f'{int(count)}', ha='center', va='bottom')  # 以整数形式显示
    plt.title(title)
    plt.xlabel('Node Type')
    plt.ylabel('Difference (Match - Non-Match)')
    plt.tight_layout()  
    plt.show()

# 绘制 MLP 和 Attention 节点的差分图
plot_difference(mlp_difference, "MLP Difference (Matching - Non-Matching)")
plot_difference(attn_difference, "Attention Difference (Matching - Non-Matching)")
