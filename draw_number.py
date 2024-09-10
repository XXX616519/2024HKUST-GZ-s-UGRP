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

# 定义绘图函数
def plot_counts(counter, title):
    sorted_counter = dict(sorted(counter.items(), key=lambda item: item[1], reverse=True))
    
    labels, counts = zip(*sorted_counter.items())
    colors = ['lightblue' if 'mlp' in label else 'lightgreen' for label in labels]  
    
    plt.figure(figsize=(16, 10)) 
    plt.bar(labels, counts, color=colors)
    plt.xticks(rotation=90) 
    for i, count in enumerate(counts):
        plt.text(i, count, str(count), ha='center', va='bottom')
    plt.title(title)
    plt.xlabel('Type')
    plt.ylabel('Frequency')
    plt.tight_layout()  
    plt.show()

# 绘制四张图
plot_counts(mlp_match_counts, "MLP Matching Answers")
plot_counts(attn_match_counts, "Attention Matching Answers")
plot_counts(mlp_non_match_counts, "MLP Non-Matching Answers")
plot_counts(attn_non_match_counts, "Attention Non-Matching Answers")