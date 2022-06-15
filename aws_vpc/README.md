### Web server and an Amazon RDS DB instance in same VPC

In this example we will create a web server running on an Amazon EC2 instance and create a MySQL database instance.
Both the Amazon EC2 instance and the DB instance run in a virtual private cloud (VPC) based on the Amazon VPC service.
you specify the VPC, subnets, and security groups when you create the DB instance. You also specify them when you
create the EC2 instance to host your web server. The VPC, subnets, and security groups are required for the
DB instance and the web server to communicate. After the VPC is set up, this tutorial shows you how to create
the DB instance and install the web server. You connect your web server to your DB instance in the VPC using
the DB instance endpoint endpoint.

This example is based on the tutorials in https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_Tutorials.WebServerDB.CreateVPC.html#CHAP_Tutorials.WebServerDB.CreateVPC.VPCAndSubnets

We will need the following requirements:

1) Both RDS and webserver on EC2 need to be within a VPC
2) Need to be able to access the data in RDS DB from internet but restricted to certain IP addresses
2) Allow communication between web server and RDS DB
3) Allow access to S3 to RDS in VPC

#### Running application locally

Assuming you are in the virutal env `virt` setup in `../README.md` , run `python application.py`
as below, which should show the address the server is running on. Navigate to this .e.g
http://127.0.0.1:5000 as in logs below

```
(virt) (base) rk1103@Ryans-MacBook-Air eb-flask % python application.py

 * Serving Flask app 'application' (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://127.0.0.1:5000 (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
```

Now we will deploy and run this application on AWS EC2 instance inside a VPC and access it from our
web browser by configuring security rules

### Creating AWS resources and deploying to AWS E2 instance

