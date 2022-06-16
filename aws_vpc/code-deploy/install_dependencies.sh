#!/bin/bash

sudo yum update -y
sudo yum install ruby -y
sudo yum install wget -y
sudo amazon-linux-extras install python3.8 -y
sudo yum install postgresql postgresql-devel python-devel -y # adds pg_config required for pip install psycopg2
pwd

