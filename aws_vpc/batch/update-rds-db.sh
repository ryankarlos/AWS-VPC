#!/bin/bash
export AWS_DEFAULT_REGION=us-east-1

export PGHOST=$1
export PGPORT=$2
export PGUSER=$3
export PGPASSWORD=$4
export PGDATABSE=$5

aws s3 cp s3://s3-eventbridge-batch/sample-data.txt sample-data.txt
psql -f 'db-update.sql'

