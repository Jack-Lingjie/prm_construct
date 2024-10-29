export MODEL_PATH='/dataset/pretrained-models/Qwen2-7B-Instruct'
export PRED_PATH='./data_pipeline/predictions/qwen2-7b-instruct-temp0.8-top_p0.95_rep2_seed0-alpaca-group'
export EVAL_PROMPT='qwen2-boxed-step'
CUDA_VISIBLE_DEVICES=0 python run_test.py --task_start_index 4010 --task_end_index 4511 &
CUDA_VISIBLE_DEVICES=1 python run_test.py --task_start_index 4511 --task_end_index 5012 &
CUDA_VISIBLE_DEVICES=2 python run_test.py --task_start_index 5012 --task_end_index 5513 &
CUDA_VISIBLE_DEVICES=3 python run_test.py --task_start_index 5513 --task_end_index 6014 &
CUDA_VISIBLE_DEVICES=4 python run_test.py --task_start_index 6014 --task_end_index 6515 &
CUDA_VISIBLE_DEVICES=5 python run_test.py --task_start_index 6515 --task_end_index 7016 &
CUDA_VISIBLE_DEVICES=6 python run_test.py --task_start_index 7016 --task_end_index 7517 &
CUDA_VISIBLE_DEVICES=7 python run_test.py --task_start_index 7517 --task_end_index 8018
wait