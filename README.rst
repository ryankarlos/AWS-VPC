=======
VPC in AWS
=======

This repo shows examples of AWS options for configuring VPC and allowing network traffic to internet
and other services


#### AWS VPC Basics

A VPC is basically a virtual network segment that is provided to AWS customers in our cloud, similar to a traditional
network that you'd operate in your on-prem infra or data center [1]. Naturally, a network would come with subnets which are
logical divisions of the same. You can have a single subnet or multiple subnets depending on your need. In AWS, we
classify the subnet further as a "Public" or "Private" subnet. The most basic difference between the two is that, for
instances in a "public" subnet, we can talk "back" to them from internet, while instances in "private" subnet are
unreachable from the internet. See AWS references [2,3]

Also, "public" and "private" are just nomenclature or logical names used for subnets. The "thing" that makes a subnet
public is an AWS solution called as "Internet Gateway" (let's call it IGW for sake of reference for this mail). As our
docs put it, an IGW enables resources (like EC2 instances) in your public subnets to connect to the internet if the
resource has a public IPv4 address or an IPv6 address. Similarly, resources on the internet can initiate a connection
to resources in your subnet using the public IPv4 address or IPv6 address. IGW basically serves two purposes: to
provide a target in your VPC route tables for internet-routable traffic, and to perform network address translation (NAT)
for instances that have been assigned public IPv4 addresses. For this to be possible, the route table attached to a
"public" subnet should have a route configured with default gateway pointing to IGW attached to the said VPC. Also,
one can connect back to a public instance from internet using the Elastic IP or auto-assigned public IP configured in
instance configuration. IGW is discussed in [4].

Now, instances in a "private" subnet wont have any routes pointing their default gateway to an IGW (else they wont be
called private). Thus, they wont be able to talk out to the internet. However, there are scenarios where instances in
"private" subnets would need internet access (say for performing updates). This is where NAT gateway (let's call it NGW
for sake of reference for this mail) fits in. A NGW basically allows instances in "private" subnet to connect to
services outside the VPC, however, external services cannot initiate a connection with those instances. The NGW replaces
the source IP address of the instances with the IP address of the NAT gateway. Thus, for private instances to be able
to talk to internet, the NGW associated with them should itself be in a "public" subnet. The internet flow then looks
like below:

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

References:

[1] https://docs.aws.amazon.com/vpc/latest/userguide/how-it-works.html
[2] https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Scenario1.html
[3] https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Scenario2.html
[4] https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Internet_Gateway.html
[5] https://docs.aws.amazon.com/vpc/latest/userguide/VPC_SecurityGroups.html


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
