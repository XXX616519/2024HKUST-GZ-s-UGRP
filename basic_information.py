# 找到yes和no答案
import json
from jsonpath_ng.ext import parse

with open('D:\\PDF\\summer_project\\transformer-debugger\\result1.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

results = {}

for key, value in data.items():
    question = value['question']
    answer = value['answer']
    
    jsonpath_expr = parse("$..vocabTokenStringsForIndices")
    vocab_token_lists = [match.value for match in jsonpath_expr.find(value) if match.value]

    # 查找最后一个 vocabTokenStringsForIndices 列表中的第一个符合条件的词汇
    first_token = None
    if vocab_token_lists:
        for token in vocab_token_lists[-1]:
            if token.lower() in ['yes', 'no']:
                first_token = token.lower()
                break

    if not first_token:
        first_token = 'none'

    results[key] = {
        'question': question,
        'answer': answer,
        "GPT-2's answer": first_token
    }

output_file = 'D:\\PDF\\summer_project\\transformer-debugger\\processed_result1.json'
with open(output_file, 'w', encoding='utf-8') as outfile:
    json.dump(results, outfile, ensure_ascii=False, indent=4)

print(f"处理完成，结果已保存到 {output_file}")
