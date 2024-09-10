import requests
import json
import pandas as pd

# Load the JSON data from processed_result.json
json_file_path = 'D:\\PDF\\summer_project\\transformer-debugger\\code\\processed_result.json'
with open(json_file_path, 'r', encoding='utf-8') as f:
    processed_data = json.load(f)

def generate_payload(question, answer):
    prompt = f"<|endoftext|>Answer this question with yes or no\nQuestion:{question}?\nAnswer:"
    if answer == "yes":
        targetTokens = [" yes"]
        distractorTokens = [" no"]
    else:
        targetTokens = [" yes"]
        distractorTokens = [" no"]
    
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

# Iterate over the questions in processed_result.json
for index, (key, item) in enumerate(processed_data.items(), start=1):
    question = item['question']
    answer = item['answer']

    # Generate the payload
    payload = generate_payload(question, answer)

    # Send the POST request
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

    results[index] = {
        'question': question,
        'answer': answer,
        'response': response.json(),
        'data': payload
    }

# Save the results to a JSON file
output_file = 'D:\\PDF\\summer_project\\transformer-debugger\\code\\result1.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=4)
