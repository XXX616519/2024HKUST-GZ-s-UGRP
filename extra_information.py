#extra information + basic information
import json
from jsonpath_ng.ext import parse


with open('D:\\PDF\\summer_project\\transformer-debugger\\code\\result1.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

results = {}

for key, value in data.items():
    question = value['question']
    answer = value['answer']
    
    jsonpath_expr = parse("$..vocabTokenStringsForIndices")
    vocab_token_lists = [match.value for match in jsonpath_expr.find(value) if match.value]

    first_token = None
    if vocab_token_lists:
        for token in vocab_token_lists[-1]:
            if token.lower() in ['yes', 'no']:
                first_token = token.lower()
                break

    if not first_token:
        first_token = 'none'

    inference_sub_responses = value['response'].get('inferenceSubResponses', [])
    if inference_sub_responses and 'processingResponseDataByName' in inference_sub_responses[0]:
        top_k_components = inference_sub_responses[0]['processingResponseDataByName']['topKComponents']
        direction_write_values = top_k_components['activationsByGroupId'].get('direction_write', [])
        
        if direction_write_values:
            sorted_indices = sorted(range(len(direction_write_values)), key=lambda i: direction_write_values[i], reverse=True)
            top_indices = sorted_indices[:10]

            node_indices = top_k_components['nodeIndices']
            extra_info = {}
            for idx, top_index in enumerate(top_indices, start=1):
                node = node_indices[top_index]
                node_type = node['nodeType']
                layer_index = node['layerIndex'] if node['layerIndex'] is not None else "unknown"
                head = node['tensorIndices'][-1]

                if 'att' in node_type:
                    node_key = f"attn_L{layer_index}_{head}"
                else:
                    node_key = f"{node_type[0:3]}_L{layer_index}_{head}"

                extra_info[str(idx)] = node_key

            results[key] = {
                'question': question,
                'answer': answer,
                "GPT-2's answer": first_token,
                **extra_info 
            }
        else:
            results[key] = {
                'question': question,
                'answer': answer,
                "GPT-2's answer": first_token
            }

output_file = 'D:\\PDF\\summer_project\\transformer-debugger\\code\\processed_result1.json'
with open(output_file, 'w', encoding='utf-8') as outfile:
    json.dump(results, outfile, ensure_ascii=False, indent=4)

print(f"处理完成，结果已保存到 {output_file}")
