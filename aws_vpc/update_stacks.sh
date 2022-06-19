#!/bin/bash

repo_root=$1

echo ""
echo "Uploading templates to s3:"
aws s3 cp ${repo_root}/templates/ s3://cf-templates-wnxns0c4jjl4-us-east-1 --recursive
echo ""
echo "Updating nested stacks:"
echo ""

aws cloudformation update-stack --stack-name Nested-RDS-Redshift-EC2-VPC \
--template-body file://templates/nested-stack.yaml \
--capabilities CAPABILITY_NAMED_IAM \
--parameters ParameterKey=RDSDBPassword,UsePreviousValue=true \
ParameterKey=UserIP,UsePreviousValue=true ParameterKey=RSPassword,UsePreviousValue=true \
ParameterKey=RDSDBUsername,UsePreviousValue=true ParameterKey=RSUsername,UsePreviousValue=true \



