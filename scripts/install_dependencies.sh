sudo yum update -y
sudo yum install ruby -y
sudo yum install wget -y
sudo amazon-linux-extras install python3.8 -y
sudo yum install postgresql postgresql-devel python-devel -y # adds pg_config required for pip install psycopg2
# if running this in appsepc yml 'Before install' stage, code deploy copies full repo into /opt/codedeploy-agent/deployment-root/
# so this path to requirements.txt needs to be relative to appspec.yml.
pwd
cd aws_vpc/eb-flask
sudo python3.8 -m pip install -r requirements.txt
