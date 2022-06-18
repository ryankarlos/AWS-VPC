
CREATE TABLE IF NOT EXISTS persons (
  id varchar(10) NOT NULL,
  email varchar(50) NOT NULL,
  state varchar(3) NOT NULL,
  postal NUMERIC(10) NOT NULL,
  address varchar(250) NOT NULL,
  PRIMARY KEY (id)
);


TRUNCATE TABLE persons;

SELECT COUNT(*) FROM persons;


\echo 'copying data into redshift table'

COPY persons from 's3://s3-eventbridge-batch/sample-data.txt' iam_role default region 'us-east-1' delimiter ',' ;

SELECT COUNT(*) FROM persons;
