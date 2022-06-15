
CREATE TABLE IF NOT EXISTS persons (
  id varchar(10) NOT NULL,
  email varchar(50) NOT NULL,
  state varchar(3) NOT NULL,
  postal INTEGER(10) NOT NULL,
  address varchar(250) NOT NULL DEFAULT
  PRIMARY KEY (id)
);

TRUNCATE TABLE persons;

\COPY persons FROM 's3://s3-eventbridge-batch/sample-data.txt' WITH DELIMITER ',' CSV;
