CUDA_VISIBLE_DEVICES=0 python run_test.py --task_start_index 2005 --task_end_index 2255 --steps 6 | tee /mnt/lingjiejiang/textual_aesthetics/prm/data/logs/machine_2_gpu_0.log &
CUDA_VISIBLE_DEVICES=1 python run_test.py --task_start_index 2255 --task_end_index 2505 --steps 6 | tee /mnt/lingjiejiang/textual_aesthetics/prm/data/logs/machine_2_gpu_1.log &
CUDA_VISIBLE_DEVICES=2 python run_test.py --task_start_index 2505 --task_end_index 2755 --steps 6 | tee /mnt/lingjiejiang/textual_aesthetics/prm/data/logs/machine_2_gpu_2.log &
CUDA_VISIBLE_DEVICES=3 python run_test.py --task_start_index 2755 --task_end_index 3005 --steps 6 | tee /mnt/lingjiejiang/textual_aesthetics/prm/data/logs/machine_2_gpu_3.log &
CUDA_VISIBLE_DEVICES=4 python run_test.py --task_start_index 3005 --task_end_index 3255 --steps 6 | tee /mnt/lingjiejiang/textual_aesthetics/prm/data/logs/machine_2_gpu_4.log &
CUDA_VISIBLE_DEVICES=5 python run_test.py --task_start_index 3255 --task_end_index 3505 --steps 6 | tee /mnt/lingjiejiang/textual_aesthetics/prm/data/logs/machine_2_gpu_5.log &
CUDA_VISIBLE_DEVICES=6 python run_test.py --task_start_index 3505 --task_end_index 3755 --steps 6 | tee /mnt/lingjiejiang/textual_aesthetics/prm/data/logs/machine_2_gpu_6.log &
CUDA_VISIBLE_DEVICES=7 python run_test.py --task_start_index 3755 --task_end_index 4005 --steps 6 | tee /mnt/lingjiejiang/textual_aesthetics/prm/data/logs/machine_2_gpu_7.log
wait