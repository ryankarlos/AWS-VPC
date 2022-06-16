FROM amazonlinux:latest

RUN yum -y install unzip aws-cli
RUN amazon-linux-extras install postgresql10
ADD aws_vpc/batch/update-rds-db.sh /tmp/update-rds-db.sh
ADD sql/db-update.sql /tmp/db-update.sql
RUN chmod +x /tmp/update-rds-db.sh
WORKDIR /tmp

ENTRYPOINT ["/tmp/update-rds-db.sh"]
