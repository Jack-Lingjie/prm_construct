import os
import json
import argparse

from my_task import get_task
# from tot.methods.bfs import solve, naive_solve
from methods.bfs import bsf_solve
# from tot.models import gpt_usage
from models.mymodel import Generator

def run(args):
    task = get_task(args.task)
    model = Generator(args.model_name, temperature=args.temperature, max_tokens=args.max_tokens)
    logs, cnt_avg, cnt_any = [], 0, 0
    if args.naive_run:
        file = f'./tree_path/{args.task}/{args.model_name}_{args.temperature}_naive_{args.prompt_sample}_sample_{args.n_generate_sample}_start{args.task_start_index}_end{args.task_end_index}.json'
    else:
        file = f'./tree_path/{args.task}/{args.model_name}_{args.temperature}_{args.model_name}{args.n_generate_sample}_{args.method_evaluate}{args.n_evaluate_sample}_{args.method_select}{args.n_select_sample}_start{args.task_start_index}_end{args.task_end_index}.json'
    

    path_file = f'./data/{args.task}/{args.model_name}_{args.temperature}_{args.model_name}{args.n_generate_sample}_{args.method_evaluate}{args.n_evaluate_sample}_{args.method_select}{args.n_select_sample}_start{args.task_start_index}_end{args.task_end_index}.json'
    
    os.makedirs(os.path.dirname(file), exist_ok=True)
    os.makedirs(os.path.dirname(path_file), exist_ok=True)

    with open(file, 'w') as f:  
        f.write('')

    with open(path_file, 'w') as f:  
        f.write('')

    total_tasks = args.task_end_index - args.task_start_index
    for i in range(args.task_start_index, args.task_end_index):

        leaf_nodes, info = bsf_solve(args, task, i, model)

        # 打印当前进度信息  
        current_task = i - args.task_start_index + 1  
        print(f"Processing task {current_task}/{total_tasks} (index {i})")  

        with open(file, 'a') as f:
            json.dump(info, f, indent=4)
        
        with open(path_file, 'a') as f:  
            for leaf in leaf_nodes:  
                f.write(json.dumps(leaf) + '\n')
    
    n = args.task_end_index - args.task_start_index
    # print(cnt_avg / n, cnt_any / n)
    # print('usage_so_far', gpt_usage(args.backend))


def parse_args():
    args = argparse.ArgumentParser()
    args.add_argument('--backend', type=str, choices=['gpt-4', 'gpt-3.5-turbo'], default='gpt-4')
    args.add_argument('--model_name', type=str, default="Meta-Llama-3.1-8B-Instruct")
    args.add_argument('--temperature', type=float, default=0.8)
    args.add_argument('--max_tokens', type=int, default=2048)
    args.add_argument('--max_samples', type=int, default=1000)

    args.add_argument('--task', type=str, choices=["prm"], default="prm")
    args.add_argument('--task_start_index', type=int, default=900)
    args.add_argument('--task_end_index', type=int, default=901)

    args.add_argument('--naive_run', action='store_true')
    args.add_argument('--prompt_sample', type=str, choices=['standard', 'cot'])  # only used when method_generate = sample, or naive_run

    args.add_argument('--method_generate', type=str, choices=['sample', 'propose'])
    args.add_argument('--method_evaluate', type=str, choices=['match', 'model'], default="match")
    args.add_argument('--method_select', type=str, choices=['sample', 'greedy'], default='greedy')
    args.add_argument('--n_generate_sample', type=int, default=3)  # only thing needed if naive_run
    args.add_argument('--n_evaluate_sample', type=int, default=1)
    args.add_argument('--n_select_sample', type=int, default=1)

    args = args.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()
    print(args)
    run(args)