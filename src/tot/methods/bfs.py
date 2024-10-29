import itertools
import numpy as np
from functools import partial
from tot.models import gpt
from tot.mymodel import Generator
import re

def get_value(task, x, y, n_evaluate_sample, cache_value=True):
    value_prompt = task.value_prompt_wrap(x, y)
    if cache_value and value_prompt in task.value_cache:
        return task.value_cache[value_prompt]
    value_outputs = gpt(value_prompt, n=n_evaluate_sample, stop=None)
    value = task.value_outputs_unwrap(x, y, value_outputs)
    if cache_value:
        task.value_cache[value_prompt] = value
    return value

def get_values(task, x, ys, n_evaluate_sample, cache_value=True):
    values = []
    local_value_cache = {}
    for y in ys:  # each partial output
        if y in local_value_cache:  # avoid duplicate candidates
            value = 0
        else:    
            value = get_value(task, x, y, n_evaluate_sample, cache_value=cache_value)
            local_value_cache[y] = value
        values.append(value)
    return values

def get_votes(task, x, ys, n_evaluate_sample):
    vote_prompt = task.vote_prompt_wrap(x, ys)
    vote_outputs = gpt(vote_prompt, n=n_evaluate_sample, stop=None)
    values = task.vote_outputs_unwrap(vote_outputs, len(ys))
    return values

def get_proposals(task, x, y): 
    propose_prompt = task.propose_prompt_wrap(x, y)
    proposals = gpt(propose_prompt, n=1, stop=None)[0].split('\n')
    return [y + _ + '\n' for _ in proposals]

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

def get_samples(task, model, input_prompts, n_generate_sample):
    input_prompts = [x for x in input_prompts for _ in range(n_generate_sample)]
    samples = model.get_response(input_prompts) # get result
    new_ys = []
    for x, y in zip(input_prompts, samples):
        new_ys.append(x + y)
    return new_ys


def extract_content_before_ith_delimiter(delimiter, input_string, i):        
    # 使用正则表达式查找所有匹配的位置  
    matches = list(re.finditer(delimiter, input_string))  
      
    if len(matches) > i:  
        # 找到第 i + 1 个 Step 的位置，并返回其之前的内容  
        return input_string[:matches[i].start()]  
    elif len(matches) <= 1:  
        # 如果没有找到第 i 个 Step，返回空字符串  
        return input_string
    else:
        return ""  
    
def get_split_prompt(task, ys, step):
    """get split prompt
    """
    delimiter = task.DELIMITER
    input_prompts = []
    for y in ys:
        # y = node.y
        prompt_extrcted = extract_content_before_ith_delimiter(delimiter, y, step)
        if prompt_extrcted:
            # TODO: add prompt warp
            prompt_extrcted = task.standard_prompt_wrap(prompt_extrcted)
            input_prompts.append(prompt_extrcted)
    return input_prompts

def get_filter_results(task, nodes, input_prompts, ys, new_ys, max_samples, n_generate_sample, step, idx):
    new_nodes = []
    for i, node in enumerate(nodes):
        if len(new_nodes) >= max_samples:
            break
        new_nodes.append(node)
        for j in range(1, n_generate_sample):
            idx += 1
            temp_node = Node(qid=node.qid, idx=idx, x=input_prompts[i], y=new_ys[i + j], step=step, parent=node.idx)
            node.next_nodes.append(idx)
            new_nodes.append(temp_node)
    select_new_ys = [node.x + node.y for node in new_nodes]
    return new_nodes, select_new_ys, idx    
    # select_new_ys = ys + new_ys
    # if len(select_new_ys) > max_samples:
    #     select_new_ys = select_new_ys[:max_samples]
    # return select_new_ys

def bsf_solve(args, task, qid, to_print=True):
    model = task.model
    idx = 0 

    x = task.get_input(qid)  # input
    ys = [task.cot_prompt_wrap(x)]  # current output candidates
    infos = []
    node_x = Node(qid=qid, idx=idx, x=x, y="", step=0, parent=-1)
    nodes = [node_x]
    for step in range(task.steps):
        # TODO: add nodes meta information
        input_prompts = get_split_prompt(task, ys, step)
        # get sample y
        # NOTE y need to append to the input x
        new_ys = get_samples(task, model, input_prompts, args.n_generate_sample)
        # get new results
        new_nodes, select_new_ys, idx = get_filter_results(task, nodes, input_prompts, ys, new_ys, args.max_samples, args.n_generate_sample, step, idx)

        ys = select_new_ys
        nodes = new_nodes
    
    if to_print: 
        print(ys)
    infos = [node.get_info() for node in nodes]
    return ys, {'tree_path': infos}

def solve(args, task, idx, to_print=True):
    global gpt
    gpt = partial(gpt, model=args.backend, temperature=args.temperature)
    print(gpt)
    x = task.get_input(idx)  # input
    ys = ['']  # current output candidates
    infos = []
    for step in range(task.steps):
        # generation
        if args.method_generate == 'sample':
            new_ys = [get_samples(task, x, y, args.n_generate_sample, prompt_sample=args.prompt_sample, stop=task.stops[step]) for y in ys]
        elif args.method_generate == 'propose':
            new_ys = [get_proposals(task, x, y) for y in ys]
        new_ys = list(itertools.chain(*new_ys))
        ids = list(range(len(new_ys)))
        # evaluation
        if args.method_evaluate == 'vote':
            values = get_votes(task, x, new_ys, args.n_evaluate_sample)
        elif args.method_evaluate == 'value':
            values = get_values(task, x, new_ys, args.n_evaluate_sample)

        # selection
        if args.method_select == 'sample':
            ps = np.array(values) / sum(values)
            select_ids = np.random.choice(ids, size=args.n_select_sample, p=ps).tolist()
        elif args.method_select == 'greedy':
            select_ids = sorted(ids, key=lambda x: values[x], reverse=True)[:args.n_select_sample]
        select_new_ys = [new_ys[select_id] for select_id in select_ids]

        # log
        if to_print: 
            sorted_new_ys, sorted_values = zip(*sorted(zip(new_ys, values), key=lambda x: x[1], reverse=True))
            print(f'-- new_ys --: {sorted_new_ys}\n-- sol values --: {sorted_values}\n-- choices --: {select_new_ys}\n')
        
        infos.append({'step': step, 'x': x, 'ys': ys, 'new_ys': new_ys, 'values': values, 'select_new_ys': select_new_ys})
        ys = select_new_ys
    
    if to_print: 
        print(ys)
    return ys, {'steps': infos}

def naive_solve(args, task, idx, to_print=True):
    global gpt
    gpt = partial(gpt, model=args.backend, temperature=args.temperature)
    print(gpt)
    x = task.get_input(idx)  # input
    ys = get_samples(task, x, '', args.n_generate_sample, args.prompt_sample, stop=None)
    return ys, {}