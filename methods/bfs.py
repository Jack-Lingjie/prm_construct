import re
import json
DELIMITER = "step"
TARGET = "the answer is"

def extract_answer(text):  
    # Pattern to match different formats of "The answer is: C"  
    pattern = r"answer is[:\s]*\(?(?P<answer>[A-J])\)?"  
    match = re.search(pattern, text, re.IGNORECASE)  
    if match:  
        return match.group("answer")  
    else:  
        # print("1st answer extract failed\n" + text)  
        return extract_again(text)  
  
def extract_again(text):  
    # Pattern to match formats like "Answer: C"  
    pattern = r'.*[aA]nswer[:\s]*([A-J])'  
    match = re.search(pattern, text)  
    if match:  
        return match.group(1)  
    else:  
        return extract_final(text)  

def extract_final(text):
    pattern = r"\b[A-J]\b(?!.*\b[A-J]\b)"
    match = re.search(pattern, text, re.DOTALL)
    if match:
        return match.group(0)
    else:
        return None
    
class Node:
    def __init__(self, qid, idx, x, y, step, parent=None, next_nodes=None, gt_answer=None, category=None):
        self.qid = qid
        self.idx = idx
        self.x = x
        self.y = y
        self.step = step
        self.parent = parent
        self.next_nodes = next_nodes if next_nodes is not None else [] 
        self.gt_answer = gt_answer
        self.pred_acc = self.get_acc()
        self.is_leaf = False
        self.is_right = False
        self.label_he = 0
        self.label_se = 0
        self.he_list = []  
        self.se_list = [] 
        self.category = category
        # self.depth = self.get_depth(y)

    def get_info(self):
        return {
            'qid': self.qid,
            'idx': self.idx,
            'x': self.x,
            'y': self.y,
            'step': self.step,
            'parent': self.parent,
            'next_nodes': self.next_nodes,
            'pred_acc': self.pred_acc,
            "label_he": self.label_he,
            "label_se": self.label_se,
            "gt_answer": self.gt_answer,
            "pred_acc": self.pred_acc,
            "pred": self.pred,
            "he_list": self.he_list,  
            "se_list": self.se_list,
            "category": self.category
        }
    
    def get_acc(self):
        pred = extract_answer(self.y)
        self.pred = pred
        # print(f"pred: {pred}")
        # print(f"self.pred: {self.pred}")
        # print(f"self.gt_answer: {self.gt_answer}")
        if pred == self.gt_answer:
            return True
        else:
            return False
        
    def get_is_leaf(self):
        return False
    
    def get_is_right(self, delimiter=DELIMITER):
        step_pattern = re.compile(re.escape(delimiter), re.IGNORECASE)  
        matches = list(step_pattern.finditer(self.y))  
        if len(matches) == self.step and self.step > 0:  
            return True
        return False

def get_samples(qid, model, input_prompts, previous_step, n_generate_sample):
    # print(f"input_prompts length: {len(input_prompts)}")
    input_prompts = [x for x in input_prompts for _ in range(n_generate_sample)]
    previous_step_copy = [x for x in previous_step for _ in range(n_generate_sample)]
    # print(f"input_prompts_copy length: {len(input_prompts)}")
    # print(f"input_prompts: {input_prompts}")
    
    try:  
        samples, original_output = model.get_next_response(input_prompts)  # get results  
    except Exception as e:  
        print("IndexError encountered in get_next_response.")  
        print(f"Exception message: {str(e)}")  
        print(f"input_prompts: {input_prompts}")
        print(f"Error qustion id: {qid}")
        raise e
    # print(f"sample: {samples}")
    new_ys = []
    for y_pre, y_new in zip(previous_step_copy, samples):
        new_ys.append(y_pre + y_new)
    # print(f"len new_ys: {len(new_ys)}")
    # print(f"new_ys: {new_ys}")
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
    step_pattern = re.compile(re.escape(delimiter), re.IGNORECASE)  
    matches = list(step_pattern.finditer(input_string))  
    if len(matches) > i:  
        # 找到第 i + 1 个 Step 的位置，并返回其之前的内容  
        return input_string[:matches[i].start()] 
    elif len(matches) <= 1:  
        # 如果没有找到第 i 个 Step，返回空
        return ""
    # else:
        # return ""  
    
def get_split_prompt(task, nodes, x, step):
    """get split prompt
    """
    # ys = [node.y for node in nodes]
    delimiter = DELIMITER
    input_prompts = []
    node_has_sons = []
    node_completed = []
    previous_step = []
    for node in nodes:
        y = node.y
        prompt_extrcted = extract_content_before_ith_delimiter(delimiter, y, step)
        if prompt_extrcted or y == "":
            # TODO: add prompt warp
            # print(f"prompt_extrcted: {prompt_extrcted}")
            previous_step.append(prompt_extrcted)
            prompt_extrcted = task.prompt_concat(x, prompt_extrcted)
            input_prompts.append(prompt_extrcted)
            node_has_sons.append(node)
        else:  
            node_completed.append(node)
    return input_prompts, previous_step, node_has_sons, node_completed

def get_filter_results(nodes, node_has_son, node_completed, new_ys, max_samples, n_generate_sample, step, idx, gt_answer):
    new_nodes = []
    for i, node in enumerate(node_has_son):
        if len(new_nodes) >= max_samples:
            break
        # new_nodes.append(node)
        for j in range(n_generate_sample):
            idx += 1
            temp_node = Node(qid=node.qid, idx=idx, x=node.x, y=new_ys[i * n_generate_sample + j], step=step, parent=node.idx, gt_answer=gt_answer, category=node.category)
            node.next_nodes.append(idx)
            new_nodes.append(temp_node)
    # new_nodes += node_completed
    # if len(nodes) == 1:
    #     # 排除根节点
    #     new_nodes = [node for node in new_nodes if node.idx != 0]
    select_new_ys = [node.y for node in new_nodes]

    return new_nodes, select_new_ys, idx    
    # select_new_ys = ys + new_ys
    # if len(select_new_ys) > max_samples:
    #     select_new_ys = select_new_ys[:max_samples]
    # return select_new_ys
def count_leaves_and_true_leaves(node, all_nodes):  
    if not node.next_nodes:  
        # 当前节点是叶节点  
        node.is_leaf = True  
        node.label_he = 1 if node.pred_acc else 0  
        node.label_se = 1 if node.pred_acc else 0  
        return 1, 1 if node.pred_acc else 0    
  
    total_leaves = 0  
    true_leaves = 0  
    for next_node_idx in node.next_nodes:  
        next_node = all_nodes[next_node_idx]  
        leaves, true_leaves_count = count_leaves_and_true_leaves(next_node, all_nodes)  
        total_leaves += leaves  
        true_leaves += true_leaves_count  
  
    # 设置当前节点的 label_he 和 label_se  
    node.label_he = 1 if true_leaves > 0 else 0  
    node.label_se = true_leaves / total_leaves if total_leaves > 0 else 0  
  
    return total_leaves, true_leaves  
  
  
def process_tree(all_nodes):  
    root = all_nodes[0]  
    count_leaves_and_true_leaves(root, all_nodes)

def dfs_collect_stats(node, all_nodes, he_path, se_path, leaf_nodes):  
    if node.step > 0:  
        he_path.append(node.label_he)  
        se_path.append(node.label_se)  
  
    if not node.next_nodes:  # 如果是叶节点  
        node.he_list = he_path.copy()  
        node.se_list = se_path.copy()  
          
        # 使用正则表达式查找所有匹配的位置  
        step_pattern = re.compile(re.escape(DELIMITER), re.IGNORECASE)  
        matches = list(step_pattern.finditer(node.y))  
        num_steps = len(matches)  
          
        # 补齐 he_list 和 se_list  
        if len(node.he_list) < num_steps:  
            last_he = node.he_list[-1] if node.he_list else 0  
            node.he_list.extend([last_he] * (num_steps - len(node.he_list)))  
              
        if len(node.se_list) < num_steps:  
            last_se = node.se_list[-1] if node.se_list else 0  
            node.se_list.extend([last_se] * (num_steps - len(node.se_list)))  
  
        # 将叶节点信息添加到 leaf_nodes 列表中  
        leaf_info = {  
            'qid': node.qid,  
            'idx': node.idx, 
            "category": node.category,
            'step': node.step,  
            'question': node.x,  
            'answer': node.y,  
            'hard_estimation': node.he_list,  
            'soft_estimation': node.se_list,
            "gt_answer": node.gt_answer,
            "pred": node.pred 
        }  
        leaf_nodes.append(leaf_info)  
  
        return  
  
    for next_node_idx in node.next_nodes:  
        next_node = all_nodes[next_node_idx]  
        dfs_collect_stats(next_node, all_nodes, he_path.copy(), se_path.copy(), leaf_nodes)  
  
def collect_stats_from_root(all_nodes):  
    leaf_nodes = []  
    root = all_nodes[0]  
    dfs_collect_stats(root, all_nodes, [], [], leaf_nodes)  
    return leaf_nodes 

def bsf_solve(args, task, qid, model, to_print=True):
    # model = task.model
    idx = 0 
    cnt = 0
    input_data = task.get_input(qid)  # input
    gt_answer = input_data["answer"]
    # x = task.cot_prompt_wrap(input_data)
    # x = model.get_input_wrap(x)
    x, raw_prompt= task.cot_prompt_wrap(input_data, model, k=0)
    ys = [""]  # current output candidates
    infos = []
    question_id = input_data["question_id"]
    category = input_data["category"]
    node_x = Node(qid=question_id, idx=idx, x=raw_prompt, y="", step=0, parent=-1, category=category)
    nodes = [node_x]
    all_nodes = [node_x]
    for step in range(args.steps):
        # TODO: add nodes meta information
        # print(f"node numbers: {len(nodes)}")
        node_idxs = [node.idx for node in nodes]
        # print(f"node idxs: {str(node_idxs)}")
        try:
            input_prompts, previous_step, node_has_son, node_completed = get_split_prompt(task, nodes, x, step)
        except Exception as e:
            print(f"Error question id: {question_id}")
            break
        cnt += len(node_completed)
        node_has_son_y = [node.y for node in node_has_son]
        node_has_son_idx = [node.idx for node in node_has_son]
        node_completed_y = [node.y for node in node_completed]
        node_completed_idx = [node.idx for node in node_completed]
        # print(f"node_has_son_idx: {str(node_has_son_idx)}")
        # print(f"node_has_son_y: {node_has_son_y}")
        # print(f"node_completed_idx: {str(node_completed_idx)}")
        # print(f"node_completed_y: {node_completed_y}")
        # print(f"node_has_son: {len(node_has_son)}")
        # print(f"node_completed: {len(node_completed)}")
        # get sample y
        # NOTE y need to append to the input x
        if len(input_prompts) == 0:
            break
        new_ys = get_samples(question_id, model, input_prompts, previous_step, args.n_generate_sample)
        # get new results
        new_nodes, select_new_ys, idx = get_filter_results(nodes, node_has_son, node_completed, new_ys, args.max_samples, args.n_generate_sample, step + 1, idx, gt_answer)
        
        ys = select_new_ys
        nodes = new_nodes
        all_nodes += nodes # parent nodes
        if cnt >= args.max_samples:
            break
        if (len(ys) >= args.max_samples):
            break

    all_nodes_dict = {node.idx: node for node in all_nodes}
    import time
    start_time = time.time()  
    process_tree(all_nodes)

  
    # 计算运行时间  


    leaf_nodes = collect_stats_from_root(all_nodes_dict)  
  
    end_time = time.time()  
    execution_time = end_time - start_time  
    print(f"process_tree 函数的运行时间: {execution_time} 秒") 

    infos = [node.get_info() for node in all_nodes]
    return leaf_nodes, {qid: infos}
