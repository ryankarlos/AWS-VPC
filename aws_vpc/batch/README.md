### Configuring AWS Batch Job to update DB on S3 data update



<img src=https://github.com/ryankarlos/AWS-VPC/blob/master/screenshots/batch-update-db-date-ecs-architecture.png></img>


Build docker image and push to ECR

````
sh scripts/docker/ecs-image.sh <USERNAME> <ACCT_ID>

[+] Building 0.8s (11/11) FINISHED
 => [internal] load build definition from Dockerfile                       0.0s
 => => transferring dockerfile: 37B                                        0.0s
 => [internal] load .dockerignore                                          0.0s
 => => transferring context: 2B                                            0.0s
 => [internal] load metadata for docker.io/library/amazonlinux:latest      0.6s
 => [1/6] FROM docker.io/library/amazonlinux:latest@sha256:246ef631c75ea8  0.0s
 => [internal] load build context                                          0.0s
 => => transferring context: 357B                                          0.0s
 => CACHED [2/6] RUN yum -y install unzip aws-cli                          0.0s
 => CACHED [3/6] RUN amazon-linux-extras install postgresql10              0.0s
 => CACHED [4/6] ADD scripts/batch/update-rds-db.sh /usr/local/bin/update  0.0s
 => CACHED [5/6] ADD sql/db-update.sql /usr/local/bin/db-update.sql        0.0s
 => CACHED [6/6] WORKDIR /tmp                                              0.0s
 => exporting to image                                                     0.0s
 => => exporting layers                                                    0.0s
 => => writing image sha256:438321fe6588c1e7e19d106d00a93b87f7a8ab3bd7760  0.0s
 => => naming to docker.io/library/awsbatch-rds                            0.0s
Login Succeeded
The push refers to repository [<ACCT_ID>.dkr.ecr.us-east-1.amazonaws.com/awsbatch-rds]
5f70bf18a086: Pushed
0ab790bb8819: Pushed
0e41a0aa33ec: Pushed
1c57756df816: Pushed
8aac9b525d16: Pushed
2ce46c79ab58: Pushed
latest: digest: sha256:a75c7f445bab278b9cf42146bd8e1af33c7aa792d57337a4d9f4d91f29db4ccc size: 1575
```

#### Upload data to S3 and trigger Batch Job


