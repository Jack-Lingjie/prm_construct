export MODEL_PATH='/dataset/pretrained-models/Qwen2-7B-Instruct'
export PRED_PATH='./data_pipeline/predictions/qwen2-7b-instruct-temp0.8-top_p0.95_rep2_seed0-alpaca-group'
export EVAL_PROMPT='qwen2-boxed-step'
CUDA_VISIBLE_DEVICES=0 python run_test.py --task_start_index 0 --task_end_index 501 &
CUDA_VISIBLE_DEVICES=1 python run_test.py --task_start_index 501 --task_end_index 1002 &
CUDA_VISIBLE_DEVICES=2 python run_test.py --task_start_index 1002 --task_end_index 1503 &
CUDA_VISIBLE_DEVICES=3 python run_test.py --task_start_index 1503 --task_end_index 2004 &
CUDA_VISIBLE_DEVICES=4 python run_test.py --task_start_index 2004 --task_end_index 2505 &
CUDA_VISIBLE_DEVICES=5 python run_test.py --task_start_index 2505 --task_end_index 3006 &
CUDA_VISIBLE_DEVICES=6 python run_test.py --task_start_index 3006 --task_end_index 3507 &
CUDA_VISIBLE_DEVICES=7 python run_test.py --task_start_index 3507 --task_end_index 4008
wait