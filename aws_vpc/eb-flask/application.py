from flask import Flask
import psycopg2
import sys
import boto3
import os
from rds_pg_connect import query_db, get_secret


header_text = """
    <html>\n<head> <title>EB Flask Test</title> </head>\n<body>"""
instructions = """
    <p><em>Hint</em>: This is a RESTful web service! Append a username
    to the URL (for example: <code>/Thelonious</code>) to say hello to
    someone specific.</p>\n"""
home_link = '<p><a href="/">Back</a></p>\n'
footer_text = "</body>\n</html>"


def say_hello(username="AWS user"):
    count_results, dbname, _ = query_db()
    return "<p>Hello {}!. There are {} entries in the RDS db '{}' </p>\n".format(
        username, count_results, dbname
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
        "/", "index", (lambda: header_text + say_hello() + instructions + footer_text)
    )

    application.add_url_rule(
        "/<username>",
        "hello",
        (lambda username: header_text + say_hello(username) + home_link + footer_text),
    )
    application.debug = debug
    application.run()


if __name__ == "__main__":
    main()
