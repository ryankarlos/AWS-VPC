REGION = "us-east-1"
RDS_SECRET_NAME = "RDS-credentials"
REDSHIFT_SECRET_NAME = "Redshift-credentials"

header_text = """
    <html>\n<head> <h1>EB Flask Test</h1> </head>"""
error_text = "<hmtl>\n<body><p>This email does not exist !</p></body></html>"
footer_text = (
    "\n<footer><p><em>Welcome!</em>: This is a RESTful web service.Append a service_name (redshift or rds) "
    "and email address to the URL. For example: <a href='/rds/fake_james61@example.net'>here</a> or "
    "<a href='/redshift/fake_julie74@example.com'>here</a>) to check data associated with email in the "
    "db.</p></p></footer></html>"
)
