from vllm import LLM, SamplingParams

class Generator:
    """open model for answer generate
    """
    def __init__(self, model_name, model_path="/mnt/lingjiejiang/textual_aesthetics/model_checkpoint/sft_merge_checkpoints", max_tokens=2048, temperature=0.8) -> None:
        """_summary_

        Args:
            model_name (str): model name
            model_path (str, optional): model save path. Defaults to "/mnt/lingjiejiang/textual_aesthetics/model_checkpoint/sft_merge_checkpoints".
            max_tokens (int, optional): max generated tokens. Defaults to 2048.
            temperature (float, optional): temperature. Defaults to 0.8.
        """
        self.llm = LLM(model=f"{model_path}/{model_name}")
        gen_kwargs_vllm = {
            "max_tokens": max_tokens,
            "top_p":0.9,
            "temperature": temperature,
            "top_k":50,
            "repetition_penalty": 1.0
        }
        template = "{% if messages[0]['role'] == 'system' %}{% set system_message = messages[0]['content'] %}{% endif %}{% if system_message is defined %}{{ system_message + '\n' }}{% endif %}{% for message in messages %}{% set content = message['content'] %}{% if message['role'] == 'user' %}{{ 'Human: ' + content + '\nAssistant:' }}{% elif message['role'] == 'assistant' %}{{ content + '<|end_of_text|>' + '\n' }}{% endif %}{% endfor %}"
        self.tokenizer = self.llm.get_tokenizer()
        if self.tokenizer.chat_template is None:
            self.tokenizer.chat_template = template
            gen_kwargs_vllm['stop_token_ids'] = [self.tokenizer.eos_token_id, self.tokenizer.convert_tokens_to_ids("<|eot_id|>")]
            print(f"tokenizer.chat_template: {self.tokenizer.chat_template}")
            print("tokenizer is None, use setted template")
        else:
            gen_kwargs_vllm['stop_token_ids'] = [self.tokenizer.eos_token_id, self.tokenizer.convert_tokens_to_ids("<|end_of_text|>")]
            print("use original template")

        self.sampling_params = SamplingParams(**gen_kwargs_vllm)
        pass
    
    def get_input_wrap(self, question_prompt) -> str:
        messages = [{"role": "user", "content": question_prompt}] 
        inputs = self.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        return inputs
    
    def get_next_response(self, inputs: list):
        encoded_inputs = self.tokenizer.batch_encode_plus(  
            inputs,  
            add_special_tokens=False,
        )  
        input_ids = encoded_inputs['input_ids']  
        print(f"sampling_params：{self.sampling_params}")
        outputs = self.llm.generate(prompt_token_ids=input_ids, sampling_params=self.sampling_params)
        outputs_text = [x.outputs[0].text for x in outputs]
        return outputs_text, outputs
           
    def get_response(self, messages: list):
        """_summary_

        Args:
            messages (list): input messages

        Returns:
            complete texts, original complete texts: [list, list]
        """
        messages = [[{"role": "user", "content": input}] for input in messages]  
        inputs = self.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        encoded_inputs = self.tokenizer.batch_encode_plus(  
            inputs,  
            add_special_tokens=False,
        ) 
        input_ids = encoded_inputs['input_ids']  
        print(f"sampling_params：{self.sampling_params}")
        outputs = self.llm.generate(prompt_token_ids=input_ids, sampling_params=self.sampling_params)
        outputs_text = [x.outputs[0].text for x in outputs]
        return outputs_text, outputs

if __name__ == '__main__':
    model = Generator("Meta-Llama-3.1-8B-Instruct")
    input_x = ["hello", "Who are you?"]
    text, complete = model.get_response(input_x)
    print(text)