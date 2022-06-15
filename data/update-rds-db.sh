#!/bin/bash

export PGHOST=$1
export PGPORT=$2
export PGUSER=$3
export PGPASSWORD=$4
export PGDATABSE=$5

sudo amazon-linux-extras install postgresql10

psql -f 's3://s3-eventbridge-batch/sample-data.txt'

