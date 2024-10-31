CUDA_VISIBLE_DEVICES=0 python run_test.py --task_start_index 10025 --task_end_index 10275 --steps 6 | tee /mnt/lingjiejiang/textual_aesthetics/prm/data/logs/machine_6_gpu_0.log &
CUDA_VISIBLE_DEVICES=1 python run_test.py --task_start_index 10275 --task_end_index 10525 --steps 6 | tee /mnt/lingjiejiang/textual_aesthetics/prm/data/logs/machine_6_gpu_1.log &
CUDA_VISIBLE_DEVICES=2 python run_test.py --task_start_index 10525 --task_end_index 10775 --steps 6 | tee /mnt/lingjiejiang/textual_aesthetics/prm/data/logs/machine_6_gpu_2.log &
CUDA_VISIBLE_DEVICES=3 python run_test.py --task_start_index 10775 --task_end_index 11025 --steps 6 | tee /mnt/lingjiejiang/textual_aesthetics/prm/data/logs/machine_6_gpu_3.log &
CUDA_VISIBLE_DEVICES=4 python run_test.py --task_start_index 11025 --task_end_index 11275 --steps 6 | tee /mnt/lingjiejiang/textual_aesthetics/prm/data/logs/machine_6_gpu_4.log &
CUDA_VISIBLE_DEVICES=5 python run_test.py --task_start_index 11275 --task_end_index 11525 --steps 6 | tee /mnt/lingjiejiang/textual_aesthetics/prm/data/logs/machine_6_gpu_5.log &
CUDA_VISIBLE_DEVICES=6 python run_test.py --task_start_index 11525 --task_end_index 11775 --steps 6 | tee /mnt/lingjiejiang/textual_aesthetics/prm/data/logs/machine_6_gpu_6.log &
CUDA_VISIBLE_DEVICES=7 python run_test.py --task_start_index 11775 --task_end_index 12025 --steps 6 | tee /mnt/lingjiejiang/textual_aesthetics/prm/data/logs/machine_6_gpu_7.log
wait