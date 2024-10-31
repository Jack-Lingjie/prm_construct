CUDA_VISIBLE_DEVICES=0 python run_test.py --task_start_index 4010 --task_end_index 4260 --steps 6 | tee /mnt/lingjiejiang/textual_aesthetics/prm/data/logs/machine_3_gpu_0.log &
CUDA_VISIBLE_DEVICES=1 python run_test.py --task_start_index 4260 --task_end_index 4510 --steps 6 | tee /mnt/lingjiejiang/textual_aesthetics/prm/data/logs/machine_3_gpu_1.log &
CUDA_VISIBLE_DEVICES=2 python run_test.py --task_start_index 4510 --task_end_index 4760 --steps 6 | tee /mnt/lingjiejiang/textual_aesthetics/prm/data/logs/machine_3_gpu_2.log &
CUDA_VISIBLE_DEVICES=3 python run_test.py --task_start_index 4760 --task_end_index 5010 --steps 6 | tee /mnt/lingjiejiang/textual_aesthetics/prm/data/logs/machine_3_gpu_3.log &
CUDA_VISIBLE_DEVICES=4 python run_test.py --task_start_index 5010 --task_end_index 5260 --steps 6 | tee /mnt/lingjiejiang/textual_aesthetics/prm/data/logs/machine_3_gpu_4.log &
CUDA_VISIBLE_DEVICES=5 python run_test.py --task_start_index 5260 --task_end_index 5510 --steps 6 | tee /mnt/lingjiejiang/textual_aesthetics/prm/data/logs/machine_3_gpu_5.log &
CUDA_VISIBLE_DEVICES=6 python run_test.py --task_start_index 5510 --task_end_index 5760 --steps 6 | tee /mnt/lingjiejiang/textual_aesthetics/prm/data/logs/machine_3_gpu_6.log &
CUDA_VISIBLE_DEVICES=7 python run_test.py --task_start_index 5760 --task_end_index 6010 --steps 6 | tee /mnt/lingjiejiang/textual_aesthetics/prm/data/logs/machine_3_gpu_7.log
wait