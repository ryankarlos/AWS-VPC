#!/bin/bash

set -e

account_id=$1

docker build -t awsbatch-rds .
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin $1.dkr.ecr.us-east-1.amazonaws.com
docker tag awsbatch-rds:latest $1.dkr.ecr.us-east-1.amazonaws.com/awsbatch-rds:latest
docker push $1.dkr.ecr.us-east-1.amazonaws.com/awsbatch-rds:latest
