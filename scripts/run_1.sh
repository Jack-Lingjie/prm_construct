CUDA_VISIBLE_DEVICES=0 python run_test.py --task_start_index 0 --task_end_index 250 | tee /mnt/lingjiejiang/textual_aesthetics/prm/data/logs/machine_1_gpu_0.log &
CUDA_VISIBLE_DEVICES=1 python run_test.py --task_start_index 250 --task_end_index 500 | tee /mnt/lingjiejiang/textual_aesthetics/prm/data/logs/machine_1_gpu_1.log &
CUDA_VISIBLE_DEVICES=2 python run_test.py --task_start_index 500 --task_end_index 750 | tee /mnt/lingjiejiang/textual_aesthetics/prm/data/logs/machine_1_gpu_2.log &
CUDA_VISIBLE_DEVICES=3 python run_test.py --task_start_index 750 --task_end_index 1000 | tee /mnt/lingjiejiang/textual_aesthetics/prm/data/logs/machine_1_gpu_3.log &
CUDA_VISIBLE_DEVICES=4 python run_test.py --task_start_index 1000 --task_end_index 1250 | tee /mnt/lingjiejiang/textual_aesthetics/prm/data/logs/machine_1_gpu_4.log &
CUDA_VISIBLE_DEVICES=5 python run_test.py --task_start_index 1250 --task_end_index 1500 | tee /mnt/lingjiejiang/textual_aesthetics/prm/data/logs/machine_1_gpu_5.log &
CUDA_VISIBLE_DEVICES=6 python run_test.py --task_start_index 1500 --task_end_index 1750 | tee /mnt/lingjiejiang/textual_aesthetics/prm/data/logs/machine_1_gpu_6.log &
CUDA_VISIBLE_DEVICES=7 python run_test.py --task_start_index 1750 --task_end_index 2000 | tee /mnt/lingjiejiang/textual_aesthetics/prm/data/logs/machine_1_gpu_7.log
wait