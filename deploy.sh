#!/bin/bash

sudo docker stop jolly_lichterman&& \
sudo docker image prune -a&& \
sudo aws s3 sync s3://alpha-model-repo/completion_model/ ./&& \
sudo aws s3 sync s3://alpha-model-repo/model_weight/ /home/ubuntu/model/Model/&& \
sudo aws s3 sync s3://alpha-model-repo/env_repo/S3/ /home/ubuntu/model/app/v1/&& \
sudo aws s3 sync s3://alpha-model-repo/env_repo/S3/ /home/ubuntu/model/app/v1/&& \
sudo aws s3 cp s3://alpha-private/db/.env /home/ubuntu/model/app/core/models/.env&& \
sudo aws s3 cp s3://alpha-private/s3/.env /home/ubuntu/model/app/v1/.env&& \
sudo docker build -t server&& \
sudodocker run --name jolly_lichterman -p 8000:80 server

