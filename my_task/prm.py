import os
import re
# from tot.tasks.base import Task, DATA_PATH
# from tot.prompts.text import *
# from tot.models import gpt
from datasets import load_dataset



choices = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P"]

def preprocess(test_df):
    res_df = []
    for each in test_df:
        options = []
        for opt in each["options"]:
            if opt == "N/A":
                continue
            options.append(opt)
        each["options"] = options
        res_df.append(each)
    return res_df

def load_mmlu_pro():
    dataset = load_dataset("TIGER-Lab/MMLU-Pro")
    test_df, val_df = dataset["test"], dataset["validation"]
    test_df = preprocess(test_df)
    val_df = preprocess(val_df)
    return test_df, val_df

def format_cot_example(example, including_answer=True):
    prompt = "Question:\n"
    question = example["question"]
    options = example["options"]
    prompt += question + "\n"
    prompt += "Options:\n"
    for i, opt in enumerate(options):
        prompt += "{}. {}\n".format(choices[i], opt)
    if including_answer:
        cot_content = example["cot_content"].replace("A: Let's think step by step.",
                                                     "Answer: Let's think step by step.")
        prompt += cot_content + "\n\n"
    # else:
    #     promp
    #     prompt += "Answer: Let's think step by step."
    return prompt

def select_by_category(df, subject):
    res = []
    for each in df:
        if each["category"] == subject:
            res.append(each)
    return res

def generate_cot_prompt(val_df, curr, k):
    prompt = ""
    with open(f"cot_prompt_lib/prompt_template_fewshot.txt", "r") as fi:
        for line in fi.readlines():
            prompt += line
    subject = curr["category"]
    val_df = select_by_category(val_df, subject)
    val_df = val_df[: k]
    prompt = prompt.replace("{$}", subject) + "\n"
    for example in val_df:
        prompt += format_cot_example(example, including_answer=True)
    prompt += format_cot_example(curr, including_answer=False)
    return prompt



class PRM:
    """
    Input (x)   : a text instruction
    Output (y)  : a text generation
    Reward (r)  : # TODO
    Input Example: 
    Output Example: 
    """
    def __init__(self, file='data_100_random_text.txt'):
        """
        file: a text file, each line is some sentences
        """
        # super().__init__()
        # path = os.path.join(DATA_PATH, 'text', file)

        # self.data = open(path).readlines()
        # self.data 
        self.full_test_df, self.full_val_df = load_mmlu_pro()
        self.data = self.full_test_df
        # self.steps = 6
        self.stops = ['\nPassage:\n', None]
        self.DELIMITER = "step"
        # self.depth = self.get_depth()

    def __len__(self) -> int:
        return len(self.data)
    
    def get_input(self, idx: int) -> str:
        return self.data[idx]
    
    def get_answer(self, idx: int) -> str:
        return self.data[idx]["answer"]
    
    # def test_output(self, idx: int, output: str):
    #     output = output.split('Passage:\n')[-1]
    #     prompt = score_prompt + output
    #     score_outputs = gpt(prompt, n=5, model='gpt-4')
    #     scores = []
    #     for score_output in score_outputs:
    #         # print(score_output)
    #         pattern = r".*coherency score is (\d+).*"
    #         match = re.match(pattern, score_output, re.DOTALL)
    #         if match:
    #             score = int(match.groups()[0])
    #             scores.append(score)
    #         else:
    #             print(f'------------------score no match: {[score_output]}')
    #     print(scores)
    #     # print('------------')
    #     info = {'rs': scores, 'r': sum(scores) / len(scores) if scores else 0}
    #     return info
    
    @staticmethod
    def standard_prompt_wrap(x: str, y:str='') -> str:
        return x + y
    
    @staticmethod
    def prompt_concat(x: str, y:str='') -> str:
        return x + y

    # @staticmethod
    def cot_prompt_wrap(self, x, model, k=1) -> str:
        # return cot_prompt.format(input=x) + y
        val_df = select_by_category(self.full_val_df, x["category"])
        raw_prompt = generate_cot_prompt(val_df, x, k)
        prompt = model.get_input_wrap(raw_prompt) + "Answer: Let's think step by step."
        question = format_cot_example(x, including_answer=False)
        return prompt, question

    # # @staticmethod
    # def get_depth(self, y: str, target="the answer is") -> int:
    #     y_lower = y.lower()
    #     target_pos = y_lower.find(target)
    #     if target_pos == -1:  
    #     # If the target string is not found, return 0  
    #         return 0
    #     substring = y_lower[:target_pos]
    #     count = substring.count(self.DELIMITER)
    #     return count
        # return x.count(".")
    # @staticmethod
    # def vote_prompt_wrap(x: str, ys: list) -> str:
    #     prompt = vote_prompt
    #     for i, y in enumerate(ys, 1):
    #         # y = y.replace('Plan:\n', '')
    #         # TODO: truncate the plan part?
    #         prompt += f'Choice {i}:\n{y}\n'
    #     return prompt
    
    # @staticmethod
    # def vote_outputs_unwrap(vote_outputs: list, n_candidates: int) -> list:
    #     vote_results = [0] * n_candidates
    #     for vote_output in vote_outputs:
    #         pattern = r".*best choice is .*(\d+).*"
    #         match = re.match(pattern, vote_output, re.DOTALL)
    #         if match:
    #             vote = int(match.groups()[0]) - 1
    #             if vote in range(n_candidates):
    #                 vote_results[vote] += 1
    #         else:
    #             print(f'vote no match: {[vote_output]}')
    #     return vote_results

    # @staticmethod
    # def compare_prompt_wrap(x: str, ys: list) -> str:
    #     assert len(ys) == 2, 'compare prompt only supports 2 candidates'
    #     ys = [y.split('Passage:\n')[-1] for y in ys]
    #     prompt = compare_prompt + f'Passage 1:\n{ys[0]}\n\nPassage 2:\n{ys[1]}\n'
    #     return prompt
    
    # @staticmethod
    # def compare_output_unwrap(compare_output: str):
    #     if 'more coherent passage is 1' in compare_output:
    #         return 0
    #     elif 'more coherent passage is 2' in compare_output:
    #         return 1
    #     elif 'two passages are similarly coherent' in compare_output:
    #         return 0.5
    #     else:
    #         print(f'-----------------compare no match: {[compare_output]}')
    #         return -1