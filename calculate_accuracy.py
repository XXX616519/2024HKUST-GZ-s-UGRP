#计算吻合率
import json

with open('D:\\PDF\\summer_project\\transformer-debugger\\code\\processed_result.json', 'r') as file:
    data = json.load(file)

total_questions = len(data)
matching_answers = 0

for key, value in data.items():
    if value["answer"].strip().lower() == value["GPT-2's answer"].strip().lower():
        matching_answers += 1

accuracy = matching_answers / total_questions * 100

print(f"Total Questions: {total_questions}")
print(f"Matching Answers: {matching_answers}")
print(f"Accuracy: {accuracy:.2f}%")
