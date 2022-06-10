from flask import Flask
import psycopg2
import sys
import boto3
import os
from rds_pg_connect import query_db

header_text = """
    <html>\n<head> <title>EB Flask Test</title> </head>"""
home_link = '<p><a href="/">Back</a></p>\n'
footer_text = "\n<footer><p><em>Hint</em>: This is a RESTful web service! Append a username " \
              "to the URL (for example: <code>/John</code>) to say hello to " \
              "someone specific.</p></p></footer></html>"


def say_hello(username="AWS user"):
    results = query_db()
    dbname = results['db_name']
    count = results['total_rows']
    email = results['person_detail']['email']
    state = results['person_detail']['state']
    postal = results['person_detail']['postal']
    address = results['person_detail']['address']
    return "\n<body><p>Hello {}!.</p>" \
           "<p>There are {} entries in the RDS db '{}'. <br> " \
           "The person associated with email '{}' lives in {}, {}, {} </p></body> ".format(
        username, count, dbname, email, address, state, postal
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
    application.run()


if __name__ == "__main__":
    main()
