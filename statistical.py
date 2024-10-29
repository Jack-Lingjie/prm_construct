import json  
import random  
from collections import Counter, defaultdict  
  
def load_jsonl(file_path):  
    with open(file_path, 'r', encoding='utf-8') as file:  
        lines = file.readlines()  
        data = [json.loads(line.strip()) for line in lines]  
    return data  
  
def get_majority_element(elements):  
    counter = Counter(elements)  
    majority_element, count = counter.most_common(1)[0]  
    return majority_element  
  
def calculate_majority_accuracy(data):  
    category_stats = defaultdict(lambda: {"correct": 0, "total": 0})  
    overall_correct = 0  
    overall_total = 0  
  
    qid_to_preds = defaultdict(list)  
    qid_to_gt_answers = {}  
  
    for entry in data:  
        qid = entry["qid"]  
        pred = entry["pred"]  
        gt_answer = entry["gt_answer"]  
        category = entry["category"]  
  
        qid_to_preds[qid].append(pred)  
        qid_to_gt_answers[qid] = gt_answer  
        category_stats[category]["total"] += 1  
  
    for qid, preds in qid_to_preds.items():  
        majority_pred = get_majority_element(preds)  
        gt_answer = qid_to_gt_answers[qid]  
  
        category = next(entry["category"] for entry in data if entry["qid"] == qid)  
  
        if majority_pred == gt_answer:  
            category_stats[category]["correct"] += 1  
            overall_correct += 1  
        overall_total += 1  
  
    # Calculate accuracy for each category  
    category_accuracy = {category: stats["correct"] / stats["total"] for category, stats in category_stats.items()}  
    overall_accuracy = overall_correct / overall_total  
  
    return category_accuracy, overall_accuracy  
  
def calculate_random_accuracy(data):  
    category_stats = defaultdict(lambda: {"correct": 0, "total": 0})  
    overall_correct = 0  
    overall_total = 0  
  
    qid_to_entries = defaultdict(list)  
  
    for entry in data:  
        qid = entry["qid"]  
        qid_to_entries[qid].append(entry)  
  
    for qid, entries in qid_to_entries.items():  
        random_entry = random.choice(entries)  
        pred = random_entry["pred"]  
        gt_answer = random_entry["gt_answer"]  
        category = random_entry["category"]  
  
        category_stats[category]["total"] += 1  
        overall_total += 1  
  
        if pred == gt_answer:  
            category_stats[category]["correct"] += 1  
            overall_correct += 1  
  
    # Calculate accuracy for each category  
    category_accuracy = {category: stats["correct"] / stats["total"] for category, stats in category_stats.items()}  
    overall_accuracy = overall_correct / overall_total  
  
    return category_accuracy, overall_accuracy  
  
if __name__ == "__main__":  
    file_path = 'data/prm_results/Meta-Llama-3.1-8B-Instruct_0.8_Meta-Llama-3.1-8B-Instruct3_match1_greedy1_start0_end2.json'  # 请替换为您的文件路径  
    data = load_jsonl(file_path)  
  
    majority_category_accuracy, majority_overall_accuracy = calculate_majority_accuracy(data)  
    random_category_accuracy, random_overall_accuracy = calculate_random_accuracy(data)  
  
    print("Majority Category Accuracy:")  
    for category, accuracy in majority_category_accuracy.items():  
        print(f"{category}: {accuracy:.2f}")  
  
    print(f"\nMajority Overall Accuracy: {majority_overall_accuracy:.2f}")  
  
    print("\nRandom Category Accuracy:")  
    for category, accuracy in random_category_accuracy.items():  
        print(f"{category}: {accuracy:.2f}")  
  
    print(f"\nRandom Overall Accuracy: {random_overall_accuracy:.2f}")  