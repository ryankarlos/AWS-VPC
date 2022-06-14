#!/bin/bash

db_username=$1
db_password=$2
client_ip=$3

echo ""
echo "Uploading templates to s3:"
aws s3 cp templates/ s3://cf-templates-wnxns0c4jjl4-us-east-1 --recursive
echo ""
echo "Creating nested stacks:"
echo ""
aws cloudformation create-stack \
--stack-name Nested-RDS-Redshift-EC2-VPC \
--template-body file://templates/nested-stack.yaml \
--parameters ParameterKey=RDSDBUsername,ParameterValue=$db_username \
ParameterKey=RDSDBPassword,ParameterValue=$db_password \
ParameterKey=RedshiftUsername,ParameterValue=$db_username \
ParameterKey=RedshiftPassword,ParameterValue=$db_password \
ParameterKey=UserIP,ParameterValue=$client_ip \
ParameterKey=InstanceType,ParameterValue=t2.micro \
ParameterKey=CreateNatGateway,ParameterValue=true \
ParameterKey=CreateElasticIP,ParameterValue=true \

