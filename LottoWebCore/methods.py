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


def sendMail(method, data, message=None, mail_subject=None, mail_to=None):
    #
    print(method)
    #
    try:
        if method == 'ATV':
            ticket_id = data['ticket_id']
            raffle = data['raffle']
            name = data['name']
            phone = data['phone']
            email = data['email']
            mail_to = email
            seller_name = data['seller']
            seller_email = data['seller_email']
            prizes = data['prizes']
            #
            mail_subject = "Bilhete #{ticket_id} - {raffle}".format(raffle=raffle, ticket_id=ticket_id)
            #
            message = """
            <html>
              <head></head>
                <body>
                    <p>Olá {name},<br><br>
                    O bilhete #<b style='font-weight: bold;'>{ticket}</b> foi ativado com sucesso e encontra-se 
                    habilitado para o <b style='font-weight: bold;'>{raffle}</b>.
                    <br><br>
                    Você estará concorrendo a: <b style='font-weight: bold;'>{prizes}</b>. 
                    <br><br>
                    Verifique se as informações abaixo estão corretas e nos contate caso haja alguma divergência.
                    <br><br>
                    Ticket: #<b style='font-weight: bold;'>{ticket}</b><br>
                    Nome: <b style='font-weight: bold;'>{name}</b><br>
                    E-mail: <b style='font-weight: bold;'>{email}</b><br>
                    Telefone: <b style='font-weight: bold;'>{phone}</b><br>
                    Vendedor: <b style='font-weight: bold;'>{seller_name}</b><br>
                    <br>
                    Atenciosamente,<br>
                    {seller_name}<br>
                    {seller_email}<br>
                </p>
              </body>
            </html>
                    """.format(name=name,
                               raffle=raffle,
                               ticket=ticket_id,
                               prizes=prizes,
                               seller_name=seller_name,
                               seller_email=seller_email,
                               phone=phone,
                               email=email)
            #
        elif method == 'FIX':
            ticket_id = data['ticket_id']
            raffle = data['raffle']
            name = data['name']
            phone = data['phone']
            email = data['email']
            seller_name = data['seller']
            seller_email = data['seller_email']
            mail_to = seller_email
            #
            mail_subject = "Bilhete #{ticket_id} - {raffle}".format(raffle=raffle, ticket_id=ticket_id)
            #
            message = """
            <html>
              <head></head>
                <body>
                    <p>Olá {seller_name},<br><br>
                    O proprietário do bilhete #<b style='font-weight: bold;'>{ticket} ({raffle})</b> nos contatou e 
                    pediu para que você verifique os dados inseridos em nosso sistema.<br><br>Caso seja necessário, 
                    contate-o diretamente utilizando os dados no canhoto e obtenha as informações necessárias para 
                    corrigir o registro do bilhete.
                    <br><br>
                    Ticket: #<b style='font-weight: bold;'>{ticket}</b><br>
                    Nome: <b style='font-weight: bold;'>{name}</b><br>
                    E-mail: <b style='font-weight: bold;'>{email}</b><br>
                    Telefone: <b style='font-weight: bold;'>{phone}</b><br>
                    <br>
                    Atenciosamente,<br>
                    <a href="https://lottohub.herokuapp.com">LottoHUB Team</a><br>
                </p>
              </body>
            </html>
                    """.format(name=name,
                               raffle=raffle,
                               ticket=ticket_id,
                               seller_name=seller_name,
                               seller_email=seller_email,
                               phone=phone,
                               email=email)
        elif method == 'WRN':
            ticket_id = data['ticket_id']
            raffle = data['raffle']
            seller_name = data['seller']
            seller_email = data['seller_email']
            mail_to = seller_email
            mail_subject = "Bilhete #{ticket_id} - {raffle}".format(raffle=raffle, ticket_id=ticket_id)
            message = """
            <html><head></head><body><p>Olá {seller_name},<br><br>
            O proprietário do bilhete #<b style='font-weight: bold;'>{ticket} ({raffle})</b> nos contatou e 
            e informou que o mesmo ainda se encontra inativo.<br>Verifique os dados no canhoto do bilhete e
            ative-o em nosso sistema.<br><br>Por configurar-se como má conduta, o recebimento de múltiplas 
            denuncias pode levar a suspensão de sua conta. <br> Evite e-mails de notificação ativando o 
            bilhete assim que possível.<br><br>Atenciosamente,<br> 
            <a href="https://lottohub.herokuapp.com">LottoHUB Team</a></p></body></html>""".format(
                raffle=raffle,
                ticket=ticket_id,
                seller_name=seller_name,
                seller_email=seller_email)
        #
        msg = MIMEText(message, 'html')
        msg['Subject'] = mail_subject
        msg['From'] = "naoresponda@lottohub.org"
        msg['To'] = mail_to
        #
        s = smtplib.SMTP('smtp.mailgun.org', 587)
        #
        s.login('postmaster@sandboxd3dfea09ed314d159446475220793ee0.mailgun.org',
                '552d7ce24b77987e6b58d72725f1d0ec-dc5f81da-be718cec')
        s.sendmail(msg['From'], msg['To'], msg.as_string())
        s.quit()
    except Exception as e:
        print(e)
