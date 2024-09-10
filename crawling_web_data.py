import requests
import json
import pandas as pd

file_path = 'D:\\PDF\\summer_project\\transformer-debugger\\code\\boolq_train.csv'
data = pd.read_csv(file_path, encoding='ISO-8859-1')

# 分别筛选出 ans 为 True 和 False 的数据
true_data = data[data['answer'] == True]
false_data = data[data['answer'] == False]

# 从 true_data 和 false_data 中各随机抽取 1000 条
true_sample = true_data.sample(n=1000, random_state=42)
false_sample = false_data.sample(n=1000, random_state=42)

# 合并两个数据集
data_sample = pd.concat([true_sample, false_sample])

def generate_payload(question, answer):
    prompt = f"<|endoftext|>Answer this question with yes or no\nQuestion:{question}?\nAnswer:"
    if answer == "yes":
        targetTokens = [" yes"]
        distractorTokens = [" no"]
    else:
        targetTokens = [" no"]
        distractorTokens = [" yes"]
    
    data = {
        "subRequests": [
            {
                "prompt": prompt,
                "targetTokens": targetTokens,
                "distractorTokens": distractorTokens,
                "componentTypeForMlp": "neuron",
                "componentTypeForAttention": "attention_head",
                "topAndBottomKForNodeTable": 10,
                "hideEarlyLayersWhenAblating": True,
                "nodeAblations": []
            }
        ]
    }
    return data


results = {}

# 遍历抽取的数据集
for index, row in data_sample.iterrows():
    question = row['question']
    answer = row['answer']

    # 将 True 和 False 转换为 "yes" 和 "no"
    if answer == True:
        answer = "yes"
    elif answer == False:
        answer = "no"
    
    # 生成请求负载
    payload = generate_payload(question, answer)

    # 发送POST请求
    url = 'http://127.0.0.1:8000/batched_tdb'
    headers = {
        'Accept': 'application/json',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Host': '127.0.0.1:8000',
        'Origin': 'http://localhost:1234',
        'Referer': 'http://localhost:1234/',
        'Sec-CH-UA': '"Chromium";v="128", "Not;A=Brand";v="24", "Microsoft Edge";v="128"',
        'Sec-CH-UA-Mobile': '?0',
        'Sec-CH-UA-Platform': '"Windows"',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0'
    }
    response = requests.post(url, headers=headers, json=payload)

    results[index + 1] = {
        'question': question,
        'answer': answer,
        'response': response.json(),
        #'data': payload
    }

output_file = 'D:\\PDF\\summer_project\\transformer-debugger\\code\\result.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=4)
