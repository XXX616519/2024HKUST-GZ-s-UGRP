#计算yes和no的数量
import json

with open('D:\\PDF\\summer_project\\transformer-debugger\\code\\processed_result1.json', 'r') as file:
    data = json.load(file)

no_count = 0

for key, value in data.items():
    if value["GPT-2's answer"].strip().lower() == "no":
        no_count += 1

# 输出结果
print(f"Total 'no' Answers in GPT-2's answer: {no_count}")
