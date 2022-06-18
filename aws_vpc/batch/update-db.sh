#!/bin/bash

set -e

export AWS_DEFAULT_REGION=us-east-1


RDS_SECRETS=$(aws secretsmanager get-secret-value --secret-id RDS-credentials --query SecretString --output text)


export PGHOST=$(echo $RDS_SECRETS | python -c 'import json, sys; print(json.load(sys.stdin)["host"])')
export PGPORT=$(echo $RDS_SECRETS | python -c 'import json, sys; print(json.load(sys.stdin)["port"])')
export PGUSER=$(echo $RDS_SECRETS | python -c 'import json, sys; print(json.load(sys.stdin)["username"])')
export PGPASSWORD=$(echo $RDS_SECRETS | python -c 'import json, sys; print(json.load(sys.stdin)["password"])')
export PGDATABASE=$(echo $RDS_SECRETS | python -c 'import json, sys; print(json.load(sys.stdin)["dbname"])')


echo "Copying data from S3 into EC2 for upload to RDS/Redshift"
aws s3 cp s3://s3-eventbridge-batch/sample-data.txt sample-data.txt

echo "Connecting to RDS DB ${PGDATABASE} on port ${PGPORT}"

psql -f 'rds-db-update.sql'


REDSHIFT_SECRETS=$(aws secretsmanager get-secret-value --secret-id Redshift-credentials --query SecretString --output text)


export PGHOST=$(echo $REDSHIFT_SECRETS | python -c 'import json, sys; print(json.load(sys.stdin)["host"])')
export PGPORT=$(echo $REDSHIFT_SECRETS | python -c 'import json, sys; print(json.load(sys.stdin)["port"])')
export PGUSER=$(echo $REDSHIFT_SECRETS | python -c 'import json, sys; print(json.load(sys.stdin)["username"])')
export PGPASSWORD=$(echo $REDSHIFT_SECRETS | python -c 'import json, sys; print(json.load(sys.stdin)["password"])')
export PGDATABASE=$(echo $REDSHIFT_SECRETS | python -c 'import json, sys; print(json.load(sys.stdin)["dbname"])')



echo "Connecting to Redshift cluster db ${PGDATABASE} on port ${PGPORT}"

psql -f 'redshift-db-update.sql'




