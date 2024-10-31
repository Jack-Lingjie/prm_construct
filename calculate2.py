import json  
import random  
from collections import Counter, defaultdict  
from tqdm import tqdm  
import pandas as pd

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
  
    for entry in tqdm(data, desc="Processing majority accuracy"): 
        qid = entry["qid"]  
        pred = entry["pred"]  
        gt_answer = entry["gt_answer"]  
        category = entry["category"]  
  
        qid_to_preds[qid].append(pred)  
        qid_to_gt_answers[qid] = gt_answer  
        qid_to_category[qid] = category  
  
    for qid, preds in tqdm(qid_to_preds.items(), desc="Calculating majority accuracy"): 
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
  
    for entry in tqdm(data, desc="Processing random accuracy"):   
        qid = entry["qid"]  
        qid_to_entries[qid].append(entry)  
  
    for qid, entries in tqdm(qid_to_entries.items(), desc="Calculating random accuracy"):  
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
      
    for entry in tqdm(data, desc="Processing max accuracy"):  
        qid = entry["qid"]  
        pred = entry["pred"]  
        gt_answer = entry["gt_answer"]  
        category = entry["category"]  
          
        qid_to_entries[qid].append((pred, gt_answer, category))  
      
    for qid, entries in tqdm(qid_to_entries.items(), desc="Calculating max accuracy"): 
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

def save_results_to_csv(majority_category_accuracy, majority_overall_accuracy, random_category_accuracy, random_overall_accuracy, max_category_accuracy, max_overall_accuracy, output_file):  
    # 存储结果的字典  
    results = {  
        "Random": random_category_accuracy,  
        "Majority": majority_category_accuracy,  
        "Max": max_category_accuracy  
    }  
  
    # 添加overall accuracy到字典中  
    results["Random"]["average"] = random_overall_accuracy  
    results["Majority"]["average"] = majority_overall_accuracy  
    results["Max"]["average"] = max_overall_accuracy  
  
    # 获取所有的学科名  
    categories = list(set(list(random_category_accuracy.keys()) + list(majority_category_accuracy.keys()) + list(max_category_accuracy.keys())))  
    categories.append("average")  
  
    # 创建DataFrame  
    df = pd.DataFrame(index=categories, columns=["Random", "Majority", "Max"])  
  
    for category in categories:  
        df.loc[category, "Random"] = results["Random"].get(category, "")  
        df.loc[category, "Majority"] = results["Majority"].get(category, "")  
        df.loc[category, "Max"] = results["Max"].get(category, "")  
  
    # 存储为CSV文件  
    df.to_csv(output_file, float_format="%.2f")  
  
    print(f"Results saved to {output_file}")  

if __name__ == "__main__":  
    file_path = '/mnt/lingjiejiang/textual_aesthetics/prm/data/data/merge_results/merged_results.jsonl'  # 请替换为您的文件路径  
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


    max_category_accuracy, max_overall_accuracy = calculate_max_accuracy(data)  
      
    print("\nMax Category Accuracy:")  
    for category, accuracy in max_category_accuracy.items():  
        print(f"{category}: {accuracy:.2f}")  
      
    print(f"\nMax Overall Accuracy: {max_overall_accuracy:.2f}")  

    # 保存结果到CSV文件  
    output_file = "data/accuracy_results.csv"  
    save_results_to_csv(majority_category_accuracy, majority_overall_accuracy, random_category_accuracy, random_overall_accuracy, max_category_accuracy, max_overall_accuracy, output_file) 