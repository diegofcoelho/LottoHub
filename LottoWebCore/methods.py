import hashlib
import os
import time

from sendgrid import sendgrid, Content, Email, Mail


def create_hash():
    ticket_hash = hashlib.sha1()
    ticket_hash.update(str(time.time()).encode('utf-8'))
    # return ticket_hash.hexdigest()[:-10]
    return ticket_hash.hexdigest()[:10]


def create_tickets():
    return 0


def send_email():
    sg = sendgrid.SendGridAPIClient()
    from_email = Email("noreply@lottohub.org")
    subject = "Hello World from the SendGrid Python Library!"
    to_email = Email("diegofcoelho@gmail.com")
    content = Content("text/plain", "Hello, Email!")
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    print(response.status_code)
    print(response.body)
    print(response.headers)
