
# VPC in AWS


This repo shows examples of AWS options for configuring VPC and allowing network traffic to internet
and other services. Using two examples:

1) Deploying flask application in ec2 instance and communicating with RDS in same VPC
2) Communicating betweein Redshift and RDS DB in separate VPC

#### Setup venv

First `cd` to the root of the repo and then run the following command to setup a virtual env named `virt` and activate it

```
$ virtualenv virt
$ source virt/bin/activate
```

Install the dependencies from the `requirements.txt` file. If you want to install the development dependencies then
install from `requirements_dev.txt`

```
$ pip install -r requirements.txt
```

To view installed dependencies in the environmentrun `pip freeze`


#### Create AWS resource using CloudFormation

The AWS Cloudformation templates are stored in `templates` folder. These are arranged in a heirarchy (nested stacks) where the root stack `nested-stack.yaml`
is the  top level stack referencing the other nested stacks (`redshift.yaml`,`rds.yaml`, `VPC.yaml`). More info about nested stacks in the AWS docs https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-nested-stacks.html

Root stack `nested-stack.yaml` uses the AWS::CloudFormation::Stack resource to reference the child stack template containing the required resouce configuration,
with a `DeletionPolicy::Retain`. The nested AWS::CloudFormation::Stack definition in the parent stack template matches the actual nested stack's template
which needs to be uploaded to S3 and https url referenced in the `TemplateURL` property.

To validate cloud formation template(s) run the following command as below (replacing the template path with the path to your template) which should return a ValidationError if the template is malformed or contains incorrect keys, syntax errors or references to logical ids etc

```
$ aws cloudformation validate-template --template-body file://templates/redshift.yaml

An error occurred (ValidationError) when calling the ValidateTemplate operation: Template format error: Unrecognized parameter type: Bool
```

To create all the nested stacks and root stack, use create-stack action for cloudformation via cli https://docs.aws.amazon.com/cli/latest/reference/cloudformation/create-stack.html
Replace <username> and <password> with the required usernames and passwords you wish to set for redhsift cluster and rds db instance
respectively. <ip> should be the client ip you wish to grant access to the db (must be of the format 191.255.255.255/24). Note the trailing
slash .Can be checked by launching EC2 instance from console - Network Settings -> tick the 'Allow SSH traffic from' box and select 'My IP'
from the dropdown which should show your IP address in the required format.

```
$ aws cloudformation create-stack \
> --stack-name Nested-RDS-Redshift-VPC \
> --template-body file://templates/nested-stack.yaml \
> --parameters ParameterKey=RDSDBUsername,ParameterValue=<username> \
> ParameterKey=RDSDBPassword,ParameterValue=<password> \
> ParameterKey=RedshiftUsername,ParameterValue=<username> \
> ParameterKey=RedshiftPassword,ParameterValue=<password> \
> ParameterKey=UserIP,ParameterValue=<ip>
  ```

 Alternatively, from the console:
    * create stack with new resources
    * upload sample tempate (root stack template i.e. `nested_stack.yaml`)
    * add stack details -> input stack name and parameters if required
    * Leave default settings in configure stack options and review steps
    * Before creating stack, tick the `I acknowledge` checkboxes in capabilites section


If successful you should see the parent stack and nested stacks all created successfully as in the
image below, where `Nested-RDS-Redshift-VPC` is the root stack and the three above are the child stacks which
were referenced in the root stack template. The resources (logical-id, physics-id and
type) created can  be found in the 'resources' tab for each stack.
If there is an error, then check the reason in the 'events' tab of the child stack that has thrown the error.

<img src=https://github.com/ryankarlos/AWS-VPC/blob/master/screenshots/Nested-Stack-console.png></img>

### AWS VPC Basics

A VPC is basically a virtual network segment that is provided to AWS customers in our cloud, similar to a traditional
network that you'd operate in your on-prem infra or data center [1]. Naturally, a network would come with subnets which are
logical divisions of the same. You can have a single subnet or multiple subnets depending on your need. In AWS, we
classify the subnet further as a "Public" or "Private" subnet. The most basic difference between the two is that, for
instances in a "public" subnet, we can talk "back" to them from internet, while instances in "private" subnet are
unreachable from the internet. See AWS references [2,3]

Also, "public" and "private" are just nomenclature or logical names used for subnets. The "thing" that makes a subnet
public is an AWS solution called as "Internet Gateway" (lets denote this 'IGW' for future reference). As per AWS docs, an
IGW enables resources (like EC2 instances) in your public subnets to connect to the internet if the resource has a public
IPv4 address or an IPv6 address. Similarly, resources on the internet can initiate a connection to resources in your
subnet using the public IPv4 address or IPv6 address. IGW basically serves two purposes: to provide a target in your
VPC route tables for internet-routable traffic, and to perform network address translation (NAT)
for instances that have been assigned public IPv4 addresses. For this to be possible, the route table attached to a
"public" subnet should have a route configured with default gateway pointing to IGW attached to the said VPC. Also,
one can connect back to a public instance from internet using the Elastic IP or auto-assigned public IP configured in
instance configuration. IGW is discussed in [4].

Now, instances in a "private" subnet wont have any routes pointing their default gateway to an IGW (else they wont be
called private). Thus, they wont be able to talk out to the internet. However, there are scenarios where instances in
"private" subnets would need internet access (say for performing updates). This is where NAT gateway (lets denote this 'NGW'
for future reference) fits in. A NGW basically allows instances in "private" subnet to connect to services outside the
VPC, however, external services cannot initiate a connection with those instances. The NGW replaces the source IP address
of the instances with the IP address of the NAT gateway. Thus, for private instances to be able to talk to internet,
the NGW associated with them should itself be in a "public" subnet. The internet flow then looks like below:

(Private Instance) ----> NGW -----> IGW ---> Internet

We will also have scenarios where we would need instances in one VPC to talk to other instances in a different VPC in
same or different AWS accounts. This can be achieved by means of solutions like "VPC Peering Connection" or a "AWS
Transit Gateway". At the core of it, you would basically have a route for remote VPC subnet with the "gateway" pointing
to either a VPC peering connection or Transit GW as appropriate.

Now, apart from VPC, we have multiple other AWS provided solutions (like RDS, S3, etc). These services are usually
reachable from internet. However, AWS also allows connecting to such services via AWS backbone network without need of
IGW or NGW. Thus, you can have "private" instances which don't have access to internet talk to these public AWS
solutions by means of "Endpoints". The gist of it, again, is a route for those services pointing to "Endpoint" as
gateway. Traffic between an Amazon VPC and a service does not leave the Amazon network when going via an endpoint:

* AWS PrivateLink is a service which basically provides Amazon VPCs with a secure and scalable way to privately connect
to such hosted services. AWS PrivateLink traffic does not use public IP addresses nor traverse the internet.
There are two types of VPC endpoints, namely Interface endpoints and Gateway endpoints.
* Gateway Endpoints are limited to providing connectivity to Amazon S3 and DynamoDB service only and they do not leverage AWS PrivateLink.
* Interface endpoints enable connectivity to services over AWS PrivateLink. These services include some AWS managed services,
services hosted by other AWS customers and partners in their own Amazon VPCs (referred to as endpoint services),
and supported AWS Marketplace partner services.

Now, further access for IP's is controlled individually at each instance level by means of Security Group (SG).
SG's are discussed in reference [5]

#### References
1) https://docs.aws.amazon.com/vpc/latest/userguide/how-it-works.html
2) https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Scenario1.html
3) https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Scenario2.html
4) https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Internet_Gateway.html
5) https://docs.aws.amazon.com/vpc/latest/userguide/VPC_SecurityGroups.html


### Credits

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
