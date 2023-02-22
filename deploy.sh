#!/bin/bash

sudo docker stop jolly_lichterman&& \
docker image prune -a&& \
aws s3 sync s3://alpha-model-repo/completion_model/ ./&& \
aws s3 sync s3://alpha-model-repo/model_weight/ /home/ubuntu/model/Model/&& \
aws s3 sync s3://alpha-model-repo/env_repo/S3/ /home/ubuntu/model/app/v1/&& \
aws s3 sync s3://alpha-model-repo/env_repo/S3/ /home/ubuntu/model/app/v1/&& \
aws s3 cp s3://alpha-private/db/.env /home/ubuntu/model/app/core/models/.env&& \
aws s3 cp s3://alpha-private/s3/.env /home/ubuntu/model/app/v1/.env&& \
docker build -t server&& \
docker run --name jolly_lichterman -p 8000:80 server

