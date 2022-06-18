FROM amazonlinux:latest

RUN yum -y install unzip aws-cli
RUN amazon-linux-extras install python3.8 -y
RUN amazon-linux-extras install postgresql10
ADD aws_vpc/batch/update-db.sh /tmp/update-db.sh
ADD sql/rds-db-update.sql /tmp/rds-db-update.sql
ADD sql/redshift-db-update.sql /tmp/redshift-db-update.sql
RUN chmod +x /tmp/update-db.sh
WORKDIR /tmp

ENTRYPOINT [ "/tmp/update-db.sh"]
