#!/bin/bash

set -e

export AWS_DEFAULT_REGION=us-east-1

export PGHOST=$1
export PGPORT=$2
export PGUSER=$3
export PGPASSWORD=$4
export PGDATABASE=$5


echo "Copying data from S3 into EC2 for upload to RDS/Redshift"
aws s3 cp s3://s3-eventbridge-batch/sample-data.txt sample-data.txt

echo "Connecting to RDS DB ${PGDATABASE} on port ${PGPORT}"

psql -f 'rds-db-update.sql'


export PGHOST=$6
export PGPORT=$7
export PGUSER=$8
export PGPASSWORD=$9
export PGDATABASE=${10}


echo "Connecting to Redshift cluster db ${PGDATABASE} on port ${PGPORT}"

psql -f 'redshift-db-update.sql'




