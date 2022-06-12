sudo yum update -y
sudo yum install ruby -y
sudo yum install wget -y
sudo amazon-linux-extras install python3.8 -y
sudo yum install postgresql postgresql-devel python-devel -y # adds pg_config required for pip install psycopg2
cd /home/ec2-user/sample-app
sudo python3.8 -m pip install -r requirements.txt
