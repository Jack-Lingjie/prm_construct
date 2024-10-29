CUDA_VISIBLE_DEVICES=0 python run_test.py --task_start_index 8020 --task_end_index 8270 | tee /mnt/lingjiejiang/textual_aesthetics/prm/data/logs/machine_5_gpu_0.log &
CUDA_VISIBLE_DEVICES=1 python run_test.py --task_start_index 8270 --task_end_index 8520 | tee /mnt/lingjiejiang/textual_aesthetics/prm/data/logs/machine_5_gpu_1.log &
CUDA_VISIBLE_DEVICES=2 python run_test.py --task_start_index 8520 --task_end_index 8770 | tee /mnt/lingjiejiang/textual_aesthetics/prm/data/logs/machine_5_gpu_2.log &
CUDA_VISIBLE_DEVICES=3 python run_test.py --task_start_index 8770 --task_end_index 9020 | tee /mnt/lingjiejiang/textual_aesthetics/prm/data/logs/machine_5_gpu_3.log &
CUDA_VISIBLE_DEVICES=4 python run_test.py --task_start_index 9020 --task_end_index 9270 | tee /mnt/lingjiejiang/textual_aesthetics/prm/data/logs/machine_5_gpu_4.log &
CUDA_VISIBLE_DEVICES=5 python run_test.py --task_start_index 9270 --task_end_index 9520 | tee /mnt/lingjiejiang/textual_aesthetics/prm/data/logs/machine_5_gpu_5.log &
CUDA_VISIBLE_DEVICES=6 python run_test.py --task_start_index 9520 --task_end_index 9770 | tee /mnt/lingjiejiang/textual_aesthetics/prm/data/logs/machine_5_gpu_6.log &
CUDA_VISIBLE_DEVICES=7 python run_test.py --task_start_index 9770 --task_end_index 10020 | tee /mnt/lingjiejiang/textual_aesthetics/prm/data/logs/machine_5_gpu_7.log
wait