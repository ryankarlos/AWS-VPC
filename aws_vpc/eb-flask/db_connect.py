import json
import os
import sys

import boto3
import psycopg2
from botocore.exceptions import ClientError
from constants import REGION, REDSHIFT_SECRET_NAME, RDS_SECRET_NAME


def get_secret(secret_name):
    client = boto3.client('secretsmanager', region_name=REGION)

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
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
            secret_data = get_secret_value_response["SecretString"]

        else:
            secret_data = get_secret_value_response["SecretBinary"]
        secret_dict = json.loads(secret_data)
        endpoint = secret_dict["host"]
        port = secret_dict["port"]
        dbname = secret_dict["dbname"]
        user = secret_dict["username"]
        password = secret_dict["password"]
        return {
            "host": endpoint,
            "port": port,
            "dbname": dbname,
            "user": user,
            "password": password,
        }


def query_db(query, service):
    if service == "rds":
        secrets_dict = get_secret(RDS_SECRET_NAME)
    elif service == "redshift":
        secrets_dict = get_secret(REDSHIFT_SECRET_NAME)
    else:
        raise ValueError("service argument must be either 'rds' or 'redshift'")
    try:
        conn = psycopg2.connect(**secrets_dict)
        with conn.cursor() as cur:
            for q in query:
                cur.execute(q)
                query_result = cur.fetchall()[0]
                if len(query_result) < 2:
                    count_result = query_result[0]
                else:
                    person_result = {
                        "email": query_result[1],
                        "state": query_result[2],
                        "postal": query_result[3],
                        "address": query_result[4],
                    }
        results = {
            "db_name": secrets_dict["dbname"],
            "total_rows": count_result,
            "person_detail": person_result,
        }
        # uncomment for debugging
        print(json.dumps(results, indent=4, default=str))
        return results
    except Exception as e:
        print("Database connection failed due to {}".format(e))


if __name__ == "__main__":
    email = "fake_julie74@example.com"
    query = [
        """SELECT COUNT(*) FROM persons""",
        """SELECT * FROM persons WHERE email LIKE '{}%'""".format(email),
    ]
    query_db(query=query, service="redshift")
