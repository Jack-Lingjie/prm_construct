# import itertools
# import numpy as np
# from functools import partial
# from tot.models import gpt
# from models.mymodel import Generator
import re

# import logging  
  
# 配置日志  
# logging.basicConfig(  
#     filename='tree_construction.log',  # 日志文件名  
#     filemode='w',  # 写模式
#     level=print,  # 设置日志级别  
#     format='%(asctime)s - %(levelname)s - %(message)s'  # 日志格式  
# )  

DELIMITER = "."
TARGET = "the answer is"

# def get_value(task, x, y, n_evaluate_sample, cache_value=True):
#     value_prompt = task.value_prompt_wrap(x, y)
#     if cache_value and value_prompt in task.value_cache:
#         return task.value_cache[value_prompt]
#     value_outputs = gpt(value_prompt, n=n_evaluate_sample, stop=None)
#     value = task.value_outputs_unwrap(x, y, value_outputs)
#     if cache_value:
#         task.value_cache[value_prompt] = value
#     return value

# def get_values(task, x, ys, n_evaluate_sample, cache_value=True):
#     values = []
#     local_value_cache = {}
#     for y in ys:  # each partial output
#         if y in local_value_cache:  # avoid duplicate candidates
#             value = 0
#         else:    
#             value = get_value(task, x, y, n_evaluate_sample, cache_value=cache_value)
#             local_value_cache[y] = value
#         values.append(value)
#     return values

# def get_votes(task, x, ys, n_evaluate_sample):
#     vote_prompt = task.vote_prompt_wrap(x, ys)
#     vote_outputs = gpt(vote_prompt, n=n_evaluate_sample, stop=None)
#     values = task.vote_outputs_unwrap(vote_outputs, len(ys))
#     return values

# def get_proposals(task, x, y): 
#     propose_prompt = task.propose_prompt_wrap(x, y)
#     proposals = gpt(propose_prompt, n=1, stop=None)[0].split('\n')
#     return [y + _ + '\n' for _ in proposals]

# def get_samples(task, x, y, n_generate_sample, prompt_sample, stop):
#     if prompt_sample == 'standard':
#         prompt = task.standard_prompt_wrap(x, y)
#     elif prompt_sample == 'cot':
#         prompt = task.cot_prompt_wrap(x, y)
#     else:
#         raise ValueError(f'prompt_sample {prompt_sample} not recognized')
#     samples = gpt(prompt, n=n_generate_sample, stop=stop)
#     return [y + _ for _ in samples]

class Node:
    def __init__(self, qid, idx, x, y, step, parent=None, next_nodes=None):
        self.qid = qid
        self.idx = idx
        self.x = x
        self.y = y
        self.step = step
        self.parent = parent
        self.next_nodes = next_nodes if next_nodes is not None else [] 
        # self.depth = self.get_depth(y)

    def get_info(self):
        return {
            'qid': self.qid,
            'idx': self.idx,
            'x': self.x,
            'y': self.y,
            'step': self.step,
            'parent': self.parent,
            'next_nodes': self.next_nodes
        }

    # def get_depth(self, y: str, target=TARGET) -> int:
    #     y_lower = y.lower()
    #     target_pos = y_lower.find(target)
    #     if target_pos == -1:  
    #     # If the target string is not found, return 0  
    #         return 0
    #     substring = y_lower[:target_pos]
    #     count = substring.count(DELIMITER)
    #     return count

def get_samples(task, model, input_prompts, previous_step, n_generate_sample):
    print(f"input_prompts length: {len(input_prompts)}")
    input_prompts = [x for x in input_prompts for _ in range(n_generate_sample)]
    previous_step_copy = [x for x in previous_step for _ in range(n_generate_sample)]
    print(f"input_prompts_copy length: {len(input_prompts)}")
    print(f"input_prompts: {input_prompts}")

    samples, original_output = model.get_response(input_prompts) # get result
    # print(f"sample: {samples}")
    new_ys = []
    for y_pre, y_new in zip(previous_step_copy, samples):
        new_ys.append(y_pre + y_new)
    print(f"len new_ys: {len(new_ys)}")
    print(f"new_ys: {new_ys}")
    # print(f"new_ys: {new_ys}")
    # print(f"original_output: {original_output}")
    return new_ys


def extract_content_before_ith_delimiter(delimiter, input_string, i): 
    input_string_lower = input_string.lower()
    target_pos = input_string_lower.find(TARGET)
    if target_pos == -1:
        return ""
    input_string = input_string[:target_pos]

    # 使用正则表达式查找所有匹配的位置  
    matches = list(re.finditer(re.escape(delimiter), input_string))  
      
    if len(matches) >= i:  
        # 找到第 i + 1 个 Step 的位置，并返回其之前的内容  
        return input_string[:matches[i - 1].end()] 
    elif len(matches) <= 1:  
        # 如果没有找到第 i 个 Step，返回空
        return ""
    # else:
        # return ""  
    
def get_split_prompt(task, nodes, x, step):
    """get split prompt
    """
    # ys = [node.y for node in nodes]
    delimiter = task.DELIMITER
    input_prompts = []
    node_has_sons = []
    node_completed = []
    previous_step = []
    for node in nodes:
        y = node.y
        prompt_extrcted = extract_content_before_ith_delimiter(delimiter, y, step)
        if prompt_extrcted or y == "":
            # TODO: add prompt warp
            print(f"prompt_extrcted: {prompt_extrcted}")
            previous_step.append(prompt_extrcted)
            prompt_extrcted = task.standard_prompt_wrap(x, prompt_extrcted)
            input_prompts.append(prompt_extrcted)
            node_has_sons.append(node)
        else:  
            node_completed.append(node)
    return input_prompts, previous_step, node_has_sons, node_completed

def get_filter_results(nodes, node_has_son, node_completed, new_ys, max_samples, n_generate_sample, step, idx):
    new_nodes = []
    for i, node in enumerate(node_has_son):
        if len(new_nodes) >= max_samples:
            break
        new_nodes.append(node)
        for j in range(n_generate_sample):
            idx += 1
            temp_node = Node(qid=node.qid, idx=idx, x=node.x, y=new_ys[i * n_generate_sample + j], step=step, parent=node.idx)
            node.next_nodes.append(idx)
            new_nodes.append(temp_node)
    new_nodes += node_completed
    if len(nodes) == 1:
        # 排除根节点
        new_nodes = [node for node in new_nodes if node.idx != 0]
    select_new_ys = [node.y for node in new_nodes]

    return new_nodes, select_new_ys, idx    
    # select_new_ys = ys + new_ys
    # if len(select_new_ys) > max_samples:
    #     select_new_ys = select_new_ys[:max_samples]
    # return select_new_ys

def bsf_solve(args, task, qid, model, to_print=True):
    # model = task.model
    idx = 0 

    input_data = task.get_input(qid)  # input
    x = task.cot_prompt_wrap(input_data)
    ys = [""]  # current output candidates
    infos = []
    node_x = Node(qid=qid, idx=idx, x=x, y="", step=0, parent=-1)
    nodes = [node_x]
    for step in range(task.steps):
        # TODO: add nodes meta information
        print(f"node numbers: {len(nodes)}")
        node_idxs = [node.idx for node in nodes]
        print(f"node idxs: {str(node_idxs)}")
        input_prompts, previous_step, node_has_son, node_completed = get_split_prompt(task, nodes, x, step)
        node_has_son_y = [node.y for node in node_has_son]
        node_has_son_idx = [node.idx for node in node_has_son]
        node_completed_y = [node.y for node in node_completed]
        node_completed_idx = [node.idx for node in node_completed]
        print(f"node_has_son_idx: {str(node_has_son_idx)}")
        print(f"node_has_son_y: {node_has_son_y}")
        print(f"node_completed_idx: {str(node_completed_idx)}")
        print(f"node_completed_y: {node_completed_y}")
        print(f"node_has_son: {len(node_has_son)}")
        print(f"node_completed: {len(node_completed)}")
        # get sample y
        # NOTE y need to append to the input x
        new_ys = get_samples(task, model, input_prompts, previous_step, args.n_generate_sample)
        # get new results
        new_nodes, select_new_ys, idx = get_filter_results(nodes, node_has_son, node_completed, new_ys, args.max_samples, args.n_generate_sample, step, idx)

        ys = select_new_ys
        nodes = new_nodes
        
        if (len(ys) >= args.max_samples):
            break
    
    # if to_print: 
    #     print(ys)
    infos = [node.get_info() for node in nodes]
    return ys, {'tree_path': infos}

# def solve(args, task, idx, to_print=True):
#     global gpt
#     gpt = partial(gpt, model=args.backend, temperature=args.temperature)
#     print(gpt)
#     x = task.get_input(idx)  # input
#     ys = ['']  # current output candidates
#     infos = []
#     for step in range(task.steps):
#         # generation
#         if args.method_generate == 'sample':
#             new_ys = [get_samples(task, x, y, args.n_generate_sample, prompt_sample=args.prompt_sample, stop=task.stops[step]) for y in ys]
#         elif args.method_generate == 'propose':
#             new_ys = [get_proposals(task, x, y) for y in ys]
#         new_ys = list(itertools.chain(*new_ys))
#         ids = list(range(len(new_ys)))
#         # evaluation
#         if args.method_evaluate == 'vote':
#             values = get_votes(task, x, new_ys, args.n_evaluate_sample)
#         elif args.method_evaluate == 'value':
#             values = get_values(task, x, new_ys, args.n_evaluate_sample)

#         # selection
#         if args.method_select == 'sample':
#             ps = np.array(values) / sum(values)
#             select_ids = np.random.choice(ids, size=args.n_select_sample, p=ps).tolist()
#         elif args.method_select == 'greedy':
#             select_ids = sorted(ids, key=lambda x: values[x], reverse=True)[:args.n_select_sample]
#         select_new_ys = [new_ys[select_id] for select_id in select_ids]

#         # log
#         if to_print: 
#             sorted_new_ys, sorted_values = zip(*sorted(zip(new_ys, values), key=lambda x: x[1], reverse=True))
#             print(f'-- new_ys --: {sorted_new_ys}\n-- sol values --: {sorted_values}\n-- choices --: {select_new_ys}\n')
        
#         infos.append({'step': step, 'x': x, 'ys': ys, 'new_ys': new_ys, 'values': values, 'select_new_ys': select_new_ys})
#         ys = select_new_ys
    
#     if to_print: 
#         print(ys)
#     return ys, {'steps': infos}

# def naive_solve(args, task, idx, to_print=True):
#     global gpt
#     gpt = partial(gpt, model=args.backend, temperature=args.temperature)
#     print(gpt)
#     x = task.get_input(idx)  # input
#     ys = get_samples(task, x, '', args.n_generate_sample, args.prompt_sample, stop=None)
#     return ys, {}