export MODEL_PATH='/dataset/pretrained-models/Qwen2-7B-Instruct'
export PRED_PATH='./data_pipeline/predictions/qwen2-7b-instruct-temp0.8-top_p0.95_rep2_seed0-alpaca-group'
export EVAL_PROMPT='qwen2-boxed-step'
CUDA_VISIBLE_DEVICES=0 python run_test.py --task_start_index 8020 --task_end_index 8521 &
CUDA_VISIBLE_DEVICES=1 python run_test.py --task_start_index 8521 --task_end_index 9022 &
CUDA_VISIBLE_DEVICES=2 python run_test.py --task_start_index 9022 --task_end_index 9523 &
CUDA_VISIBLE_DEVICES=3 python run_test.py --task_start_index 9523 --task_end_index 10024 &
CUDA_VISIBLE_DEVICES=4 python run_test.py --task_start_index 10024 --task_end_index 10525 &
CUDA_VISIBLE_DEVICES=5 python run_test.py --task_start_index 10525 --task_end_index 11026 &
CUDA_VISIBLE_DEVICES=6 python run_test.py --task_start_index 11026 --task_end_index 11527 &
CUDA_VISIBLE_DEVICES=7 python run_test.py --task_start_index 11527 --task_end_index 12028
wait