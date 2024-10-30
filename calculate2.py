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
    qid_to_category = {}  
  
    for entry in data:  
        qid = entry["qid"]  
        pred = entry["pred"]  
        gt_answer = entry["gt_answer"]  
        category = entry["category"]  
  
        qid_to_preds[qid].append(pred)  
        qid_to_gt_answers[qid] = gt_answer  
        qid_to_category[qid] = category  
  
    for qid, preds in qid_to_preds.items():  
        majority_pred = get_majority_element(preds)  
        gt_answer = qid_to_gt_answers[qid]  
        category = qid_to_category[qid]  
  
        category_stats[category]["total"] += 1  
        overall_total += 1  
  
        if majority_pred == gt_answer:  
            category_stats[category]["correct"] += 1  
            overall_correct += 1  
  
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

def calculate_max_accuracy(data):  
    category_correct_count = defaultdict(int)  
    category_total_count = defaultdict(int)  
    qid_correct_count = defaultdict(int)  
    qid_total_count = defaultdict(int)  
    overall_correct = 0  
    overall_total = 0  
      
    qid_to_entries = defaultdict(list)  
      
    for entry in data:  
        qid = entry["qid"]  
        pred = entry["pred"]  
        gt_answer = entry["gt_answer"]  
        category = entry["category"]  
          
        qid_to_entries[qid].append((pred, gt_answer, category))  
      
    for qid, entries in qid_to_entries.items():  
        category = entries[0][2]  # All entries for the same qid should have the same category  
        qid_total_count[qid] += 1  
        category_total_count[category] += 1  
        overall_total += 1  
          
        correct = any(pred == gt_answer for pred, gt_answer, _ in entries)  
          
        if correct:  
            qid_correct_count[qid] += 1  
            category_correct_count[category] += 1  
            overall_correct += 1  
      
    overall_accuracy = overall_correct / overall_total  
    category_accuracy = {category: category_correct_count[category] / category_total_count[category] for category in category_total_count}  
      
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


    category_accuracy, overall_accuracy = calculate_max_accuracy(data)  
      
    print("\nMax Category Accuracy:")  
    for category, accuracy in category_accuracy.items():  
        print(f"{category}: {accuracy:.2f}")  
      
    print(f"\nMax Overall Accuracy: {overall_accuracy:.2f}")  