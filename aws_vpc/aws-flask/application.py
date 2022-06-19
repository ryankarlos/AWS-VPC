import os
import sys

import boto3
import psycopg2
from flask import Flask
from db_connect import query_db
import logging
from constants import header_text, footer_text, error_text

log = logging.getLogger("werkzeug")


def index():
    return header_text + footer_text


def main(service_name, email):
    query = [
        """SELECT COUNT(*) FROM persons""",
        """SELECT * FROM persons WHERE email LIKE '%{}%'""".format(email),
    ]
    results = query_db(query, service_name)
    if results is None:
        return error_text + '<p><a href="/">Back</a></p>\n'
    else:
        dbname = results["db_name"]
        count = results["total_rows"]
        email = results["person_detail"]["email"]
        state = results["person_detail"]["state"]
        postal = results["person_detail"]["postal"]
        address = results["person_detail"]["address"]
        return (
            "\n<body><p>There are {} entries in the {} db '{}'. <br> "
            "The person associated with email '{}' lives in {}, {}, {} </p></body> ".format(
                service_name, count, dbname, email, address, state, postal
             )
            + '<p><a href="/">Back</a></p>\n'
            )


if __name__ == "__main__":
    application = Flask(__name__)
    application.add_url_rule("/", "index", index)

    application.add_url_rule(
        "/<service_name>/<email>", "main", main
    )
    debug = False
    application.debug = debug
    application.run(host="0.0.0.0", port=80)
