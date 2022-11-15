import os
import sendgrid
import tomli
from sendgrid.helpers.mail import *
import yaml
import datetime

time_now = datetime.datetime.now()
# dd/mm/YY H:M:S
dt_string = time_now.strftime("%d/%m/%Y %H:%M:%S")

with open("config.toml", mode="rb") as t:
    config = tomli.load(t)

with open('base.html', mode="r") as html:
    base_email = html.read()

with open('email_addys.yaml', mode="r") as emails:
    email_addys = yaml.safe_load(emails)

sg = sendgrid.SendGridAPIClient(
    api_key=config["sendgrid"]["api_key"]
)

from_email = Email(config["email"]["from"])
subject = f"[ACTION REQUIRED] {config['email']['subject']}"

for email in email_addys["emails"]:
    to_email = To(email)
    content = Content(MimeType.html, base_email)
    mail = Mail(from_email, to_email, subject, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    print(f"---> Sent the email to {email}, with a status code of {response.status_code}")

# The statements below can be included for debugging purposes
#print(response.status_code)
#print(response.body)
#print(response.headers)