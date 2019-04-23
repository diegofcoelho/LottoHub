import hashlib
import smtplib
import time
from email.mime.text import MIMEText

import requests
from sendgrid import SendGridAPIClient


def create_hash():
    ticket_hash = hashlib.sha1()
    ticket_hash.update(str(time.time()).encode('utf-8'))
    # return ticket_hash.hexdigest()[:-10]
    return ticket_hash.hexdigest()[:10]


def create_tickets():
    return 0


#
# def send_email():
#     message = {
#         'personalizations': [
#             {
#                 'to': [
#                     {
#                         'email': 'diegofcoelho@gmail.com'
#                     }
#                 ],
#                 'subject': 'Sending with Twilio SendGrid is Fun'
#             }
#         ],
#         'from': {
#             'email': 'diegofcoelho@gmail.com'
#         },
#         'content': [
#             {
#                 'type': 'text/plain',
#                 'value': 'and easy to do anywhere, even with Python'
#             }
#         ]
#     }
#
#     try:
#         sg = SendGridAPIClient('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')
#         response = sg.send(message)
#         print(response.status_code)
#         print(response.body)
#         print(response.headers)
#     except Exception as e:
#         print(e.message)
#         print('Error')

#
# def send_simple_message():
#     return requests.post(
#         "https://api.mailgun.net/v3/sandboxd3dfea09ed314d159446475220793ee0.mailgun.org",
#         auth=("api", "9cf144f07dc4fa362fdfeef96da0d137-dc5f81da-32005054"),
#         data={"from": "dfcoelho@live.com",
#               "to": ["coelho@ufs.br"],
#               "subject": "Hello",
#               "text": "Testing some Mailgun awesomness!"})
#
# send_simple_message()


def sendMail(mail_to, data):
    #
    ticket_id = data['ticket_id']
    sorteio = data['sorteio']
    nome = data['nome']
    seller = data['seller']
    prizes = data['prizes']
    #
    message = 'Olá {}, \n\nO bilhete {} foi cadastrado para o sorteio {}.' \
              '\n\nVocê estará concorrendo a: {}. \n\nVerifique se as informações cadastradas estão corretas e nos ' \
              'contate a qualquer momento.\n\nAtenciosamente\n{}'.format(nome, ticket_id, sorteio, prizes, seller)
    msg = MIMEText(message)
    msg['Subject'] = "{}: Bilhete [{}]".format(sorteio, ticket_id)
    msg['From'] = "noreply@lottohub.org"
    msg['To'] = mail_to

    s = smtplib.SMTP('smtp.mailgun.org', 587)

    s.login('postmaster@sandboxd3dfea09ed314d159446475220793ee0.mailgun.org',
            '552d7ce24b77987e6b58d72725f1d0ec-dc5f81da-be718cec')
    s.sendmail(msg['From'], msg['To'], msg.as_string())
    s.quit()
