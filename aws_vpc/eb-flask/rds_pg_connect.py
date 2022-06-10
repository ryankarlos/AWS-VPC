import psycopg2
import sys
import boto3
import os
import json
from botocore.exceptions import ClientError


ENDPOINT = "pg-non-default.cg9we74vymgv.us-east-1.rds.amazonaws.com"
PORT = "5432"
USER = "ryankarlos"
REGION = "us-east-1"
DBNAME = "postgresdev"
SECRET_NAME = "RDS-DB-credentials"

# gets the credentials from .aws/credentials
session = boto3.Session(profile_name="default")
client = session.client("rds")


def get_secret():

    session = boto3.session.Session()
    client = session.client(
        service_name="secretsmanager",
        region_name=REGION,
    )

    try:
        get_secret_value_response = client.get_secret_value(SecretId=SECRET_NAME)
    except ClientError as e:
        if e.response["Error"]["Code"] == "ResourceNotFoundException":
            print("The requested secret " + SECRET_NAME + " was not found")
        elif e.response["Error"]["Code"] == "InvalidRequestException":
            print("The request was invalid due to:", e)
        elif e.response["Error"]["Code"] == "InvalidParameterException":
            print("The request had invalid params:", e)
        elif e.response["Error"]["Code"] == "DecryptionFailure":
            print(
                "The requested secret can't be decrypted using the provided KMS key:", e
            )
        elif e.response["Error"]["Code"] == "InternalServiceError":
            print("An error occurred on service side:", e)
    else:
        # Secrets Manager decrypts the secret value using the associated KMS CMK
        # Depending on whether the secret was a string or binary, only one of these fields will be populated
        if "SecretString" in get_secret_value_response:
            text_secret_data = get_secret_value_response["SecretString"]
            return text_secret_data
        else:
            binary_secret_data = get_secret_value_response["SecretBinary"]
            return binary_secret_data


def query_db(query="""SELECT COUNT(*) FROM persons"""):
    secret_data = get_secret()
    password = json.loads(secret_data)["password"]
    dbname = json.loads(secret_data)["dbname"]
    dbi = json.loads(secret_data)["dbInstanceIdentifier"]
    try:
        conn = psycopg2.connect(
            host=ENDPOINT, port=PORT, database=DBNAME, user=USER, password=password
        )
        cur = conn.cursor()
        cur.execute(query)
        query_result = cur.fetchone()[0]
        print(query_result)
        return query_result, dbname, dbi
    except Exception as e:
        print("Database connection failed due to {}".format(e))


if __name__ == "__main__":
    query_db()
