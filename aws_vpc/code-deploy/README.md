
## Create and Execute New Deployment

The cloudformation nested stack in templates folder automatically creates the application and
deployment group with configuration required for code deployment to EC2 instance. In addition,
when the EC2 instance is created, the code deploy agent is also installed and started.
Alternatively, the agent can be installed manually on Amazon Linux instance
https://docs.aws.amazon.com/codedeploy/latest/userguide/codedeploy-agent-operations-install-linux.html
When we first create deployment using the command below https://docs.aws.amazon.com/cli/latest/reference/deploy/create-deployment.html
- we specify the names of existing  deployment group and application name and source code location (either github or S3).
Additionally we can specify optional arg for `file-exists-behaviour`.If existing files from
previous deployment are found - this will fail the deployment by default so we will set  this to overwrite.

```
aws deploy create-deployment \
    --application-name DeployEC2 \
    --deployment-group-name EC2-DeploymentGroup \
    --description EC2-flask-deployment \
    --file-exists-behavior OVERWRITE \
    --github-location repository=ryankarlos/AWS-VPC,commitId=a3abc7a00a103d1714cb198b376bfd71fdd043bf

{
    "deploymentId": "d-KQGZVR58I"
}
```

 We can also set `--ignore-application-stop-failures` option to control what happens if ApplicationStop ,
  BeforeBlockTraffic , or AfterBlockTraffic deployment lifecycle eventdeployment lifecycle event to an
  instance fails. The default behaviour during a deployment is that the AWS CodeDeploy agent runs the
  scripts specified for ApplicationStop (BeforeBlockTraffic/AfterBlockTraffic if present) events
  in the AppSpec file from the previous successful deployment.
All other scripts are run from the AppSpec file in the current deployment. If one of these scripts contains
  an error and  does not run successfully, the deployment can fail. Hence to prevent this we can either

    * Set `--ignore-application-stop-failures` to specify that the ApplicationStop , BeforeBlockTraffic , and
      AfterBlockTraffic failures should be ignored. This is the recommended way

    * ssh into the EC2 instance and delete ou can delete the file, that CodeDeploy uses to keep track of the
      previous successful deployment in the following path /opt/codedeploy-agent/deployment-root/deployment-instructions/

We have defined an AppSpec file at the root of the repo for codedeploy to run the tasks
on the instance, following the example listed in the AWS docs
https://docs.aws.amazon.com/codedeploy/latest/userguide/reference-appspec-file.html#appspec-reference-server

The CodeDeploy agent copies the application revision files in github source location to a temporary location:
`/opt/codedeploy-agent/deployment-root/deployment-group-id/deployment-id/deployment-archive` folder on
Amazon Linux. During the deployment lifecycle Install event, the CodeDeploy agent copies the revision files
from the temporary location to the final destination folder.
The source and destination path of the main application files (`aws-vpc/aws-flask`) to be copied over is
specified in  the files section of the AppSpec.yaml. If we ssh into ec2 instance after successful deployment,
we should see the application files in `/home/ec2-user/sample-app` from where the application is run.

The hooks section contain the various lifecycle events as described in the AWS docs:
https://docs.aws.amazon.com/codedeploy/latest/userguide/reference-appspec-file-structure-hooks.html
Here, we use some of these for the flask deployment.

  * ApplicationStop – This deployment lifecycle event occurs even before the application revision is downloaded.
    It stops the flask server which is currently running - which will be restarted in the ApplicationStart
    step with the most recent changes to the application code.
* BeforeInstall – Runs preinstall tasks like updating already installed packages, installing python3.8
and postgresql/psql in the container
  * AfterInstall – Installs the python packages for flask app from requirements.txt
  * ApplicationStart – Start flask server  or restart it after it was stopped during ApplicationStop event.
    the `start_server.sh` script runs the application silently and redirects all stdout and stderr to dev/null.
    This is necessary to allow the codedeploy event to succeed/exit successfully after the web server is started.
    Else it will stall and fail after the specified timeout (300 secs)

<img src="https://github.com/ryankarlos/AWS-VPC/blob/master/screenshots/code-deploy-console-successful-deployment-stages.png"></img>



