### Configuring AWS Batch Job to update DB on S3 data update

<img src=https://github.com/ryankarlos/AWS-VPC/blob/master/screenshots/batch-update-db-date-ecs-architecture.png></img>


Build docker image and push to ECR

````
sh scripts/docker/ecs-image.sh <USERNAME> <ACCT_ID>

[+] Building 36.0s (14/14) FINISHED
 => [internal] load build definition from Dockerfile                       0.0s
 => => transferring dockerfile: 428B                                       0.0s
 => [internal] load .dockerignore                                          0.0s
 => => transferring context: 2B                                            0.0s
 => [internal] load metadata for docker.io/library/amazonlinux:latest      2.0s
 => [internal] load build context                                          0.0s
 => => transferring context: 1.12kB                                        0.0s
 => [1/9] FROM docker.io/library/amazonlinux:latest@sha256:246ef631c75ea8  0.0s
 => CACHED [2/9] RUN yum -y install unzip aws-cli                          0.0s
 => [3/9] RUN amazon-linux-extras install python3.8 -y                    22.9s
 => [4/9] RUN amazon-linux-extras install postgresql10                     8.2s
 => [5/9] ADD aws_vpc/batch/update-db.sh /tmp/update-db.sh                 0.0s
 => [6/9] ADD sql/rds-db-update.sql /tmp/rds-db-update.sql                 0.0s
 => [7/9] ADD sql/redshift-db-update.sql /tmp/redshift-db-update.sql       0.0s
 => [8/9] RUN chmod +x /tmp/update-db.sh                                   0.4s
 => [9/9] WORKDIR /tmp                                                     0.0s
 => exporting to image                                                     2.2s
 => => exporting layers                                                    2.2s
 => => writing image sha256:beec1e752b7bf81c12e332d923319b55cff2820cf448c  0.0s
 => => naming to docker.io/library/awsbatch-rds                            0.0s
Login Succeeded
The push refers to repository [<ACCT_ID>.dkr.ecr.us-east-1.amazonaws.com/awsbatch-rds]
5f70bf18a086: Layer already exists
374c4222b9e1: Pushed
14679570a55f: Pushed
aed807940e63: Pushed
5f0c96b8fba7: Pushed
4f1ed007001e: Pushed
8fcc60dd6b69: Pushed
8aac9b525d16: Layer already exists
2ce46c79ab58: Layer already exists
latest: digest: sha256:811461221b1ea602e33dc8fec236ca4a08861aa446d1c8d39a2ef9135db4444c size: 2202

````

#### Upload data to S3 and trigger Batch Job

To trigger the batch job - copy sample-data.txt into s3 bucket path as below. This will create
a cloudtrail event which triggers EventBridge which sends the event to the batch job queue
set as target.
We have already configured the batch job parameters in cloud formation - including the cmd parameters for
the ECR image entrypoint script, which will execute once the container is deployed and running in
ECS Fargate

```
aws s3 cp data/sample-data.txt s3://s3-eventbridge-batch/sample-data.txt

upload: data/sample-data.txt to s3://s3-eventbridge-batch/sample-data.txt
```


<img src=https://github.com/ryankarlos/AWS-VPC/blob/master/screenshots/aws-batch-dashboard.png></img>

<img src=https://github.com/ryankarlos/AWS-VPC/blob/master/screenshots/aws-batch-jobs-status.png></img>

<img src=https://github.com/ryankarlos/AWS-VPC/blob/master/screenshots/aws-batch-logs.png></img>


