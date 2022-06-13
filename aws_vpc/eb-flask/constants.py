REGION = "us-east-1"
SECRET_NAME = "RDS-DB-credentials"

header_text = """
    <html>\n<head> <title>EB Flask Test</title> </head>"""
home_link = '<p><a href="/">Back</a></p>\n'
footer_text = (
    "\n<footer><p><em>Hint</em>: This is a RESTful web service! Append a username "
    "to the URL (for example: <code>/John</code>) to say hello to "
    "someone specific.</p></p></footer></html>"
)

query = [
    """SELECT COUNT(*) FROM persons""",
    """SELECT * FROM persons WHERE email LIKE 'fake_cgonzales%'""",
]
