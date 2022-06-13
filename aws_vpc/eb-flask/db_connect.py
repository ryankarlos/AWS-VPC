import json
import os
import sys

import boto3
import psycopg2
from botocore.exceptions import ClientError
from constants import query, REGION, SECRET_NAME


def get_secret():
    ssm = boto3.client("ssm", region_name="us-east-1")
    access_key_id = ssm.get_parameter(Name="ACCESS_KEY_ID", WithDecryption=True)[
        "Parameter"
    ]["Value"]
    secret_access_key = ssm.get_parameter(
        Name="SECRET_ACCESS_KEY", WithDecryption=True
    )["Parameter"]["Value"]

    session = boto3.Session(
        aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key
    )

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


def query_rds(query):
    secret_data = get_secret()
    secret_dict = json.loads(secret_data)
    password = secret_dict["password"]
    user = secret_dict["username"]
    dbname = secret_dict["dbname"]
    endpoint = secret_dict["host"]
    port = secret_dict["port"]
    dbi = secret_dict["dbInstanceIdentifier"]
    try:
        conn = psycopg2.connect(
            host=endpoint, port=port, database=dbname, user=user, password=password
        )
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
            "db_name": dbname,
            "db_identifier": dbi,
            "total_rows": count_result,
            "person_detail": person_result,
        }
        # uncomment for debugging
        # print(json.dumps(results, indent=4))
        return results
    except Exception as e:
        print("Database connection failed due to {}".format(e))


if __name__ == "__main__":
    query_rds(query)
