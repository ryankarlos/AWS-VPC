#!/bin/bash

db_username=$1
db_password=$2
client_ip=$3
repo_root=$4
natgateway=${5-true}
elasticip=${6-true}

echo ""
echo "Uploading templates to s3:"
aws s3 cp ${repo_root}/templates/ s3://cf-templates-wnxns0c4jjl4-us-east-1 --recursive
echo ""
echo "Creating nested stacks:"
echo ""
aws cloudformation create-stack \
--stack-name Nested-RDS-Redshift-EC2-VPC \
--template-body "file://${repo_root}/templates/nested-stack.yaml" \
--parameters ParameterKey=RDSDBUsername,ParameterValue=$db_username \
ParameterKey=RDSDBPassword,ParameterValue=$db_password \
ParameterKey=RedshiftUsername,ParameterValue=$db_username \
ParameterKey=RedshiftPassword,ParameterValue=$db_password \
ParameterKey=UserIP,ParameterValue="${client_ip}/32" \
ParameterKey=InstanceType,ParameterValue=t2.micro \
ParameterKey=CreateNatGateway,ParameterValue=$natgateway \
ParameterKey=CreateElasticIP,ParameterValue=$elasticip \

