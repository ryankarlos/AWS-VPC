import os
import sys

import boto3
import psycopg2
from flask import Flask
from db_connect import query_rds
import logging
from constants import header_text, home_link, footer_text, query

log = logging.getLogger("werkzeug")


def say_hello(username="AWS user"):
    results = query_rds(query)
    dbname = results["db_name"]
    count = results["total_rows"]
    email = results["person_detail"]["email"]
    state = results["person_detail"]["state"]
    postal = results["person_detail"]["postal"]
    address = results["person_detail"]["address"]
    return (
        "\n<body><p>Hello {}!.</p>"
        "<p>There are {} entries in the RDS db '{}'. <br> "
        "The person associated with email '{}' lives in {}, {}, {} </p></body> ".format(
            username, count, dbname, email, address, state, postal
        )
    )


def main(debug=False):
    """
    Runs the main app. Elastic Beanstalk looks for an 'application'
    callable by default. Added rules for the index page depending on whether name
    is appended to site URL or not.
    Setting debug to True enables debug output. Set to false before deploying a production app.
    """
    application = Flask(__name__)
    application.add_url_rule(
        "/", "index", (lambda: header_text + say_hello() + footer_text)
    )

    application.add_url_rule(
        "/<username>",
        "hello",
        (lambda username: header_text + say_hello(username) + home_link),
    )
    application.debug = debug
    application.run(host="0.0.0.0", port=80)


if __name__ == "__main__":
    main()
