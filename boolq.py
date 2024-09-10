# 下载boolq数据集
from datasets import load_dataset

dataset = load_dataset("google/boolq")

dataset['train'].to_csv("boolq_train.csv", index=False)

dataset['validation'].to_csv("boolq_validation.csv", index=False)
