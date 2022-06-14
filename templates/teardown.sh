#!/bin/bash

# this command first filters the query to only return existing nested stacks with matching names. Then clean
# with sed to remove "" and , from output of grep to then use in aws cf delete stack call
id=$(aws cloudformation list-stacks --query 'StackSummaries[?StackStatus==`CREATE_COMPLETE`].StackName' \
| grep 'Nested-RDS-Redshift-EC2-VPC' | sed 's/[",]//g')

for name in $id; do
    echo ""
    echo "Deleting stack $name"
    aws cloudformation delete-stack --stack-name $name
done;

