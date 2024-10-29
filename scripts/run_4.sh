CUDA_VISIBLE_DEVICES=0 python run_test.py --task_start_index 6015 --task_end_index 6265 | tee /mnt/lingjiejiang/textual_aesthetics/prm/data/logs/machine_4_gpu_0.log &
CUDA_VISIBLE_DEVICES=1 python run_test.py --task_start_index 6265 --task_end_index 6515 | tee /mnt/lingjiejiang/textual_aesthetics/prm/data/logs/machine_4_gpu_1.log &
CUDA_VISIBLE_DEVICES=2 python run_test.py --task_start_index 6515 --task_end_index 6765 | tee /mnt/lingjiejiang/textual_aesthetics/prm/data/logs/machine_4_gpu_2.log &
CUDA_VISIBLE_DEVICES=3 python run_test.py --task_start_index 6765 --task_end_index 7015 | tee /mnt/lingjiejiang/textual_aesthetics/prm/data/logs/machine_4_gpu_3.log &
CUDA_VISIBLE_DEVICES=4 python run_test.py --task_start_index 7015 --task_end_index 7265 | tee /mnt/lingjiejiang/textual_aesthetics/prm/data/logs/machine_4_gpu_4.log &
CUDA_VISIBLE_DEVICES=5 python run_test.py --task_start_index 7265 --task_end_index 7515 | tee /mnt/lingjiejiang/textual_aesthetics/prm/data/logs/machine_4_gpu_5.log &
CUDA_VISIBLE_DEVICES=6 python run_test.py --task_start_index 7515 --task_end_index 7765 | tee /mnt/lingjiejiang/textual_aesthetics/prm/data/logs/machine_4_gpu_6.log &
CUDA_VISIBLE_DEVICES=7 python run_test.py --task_start_index 7765 --task_end_index 8015 | tee /mnt/lingjiejiang/textual_aesthetics/prm/data/logs/machine_4_gpu_7.log
wait