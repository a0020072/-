python model_main.py \
    --pipeline_config_path=training/ssd_mobilenet_v1_pets.config \
    --model_dir=training \
    --num_train_steps=50000 \
    --num_eval_steps=2000 \
    --alsologtostderr
pause