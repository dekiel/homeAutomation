#! /Users/i319037/github/dekiel/homeAutomation/venv/bin/python3
import smtplib, ssl
from email.message import EmailMessage

smtp =
smtp_port = '587'
smtp_sender =
smtp_to =

if __name__ == '__main__':
    msg = EmailMessage()
    msg.set_content("tekst przykladowy")
    msg['Subject'] = "temat"
    msg['From'] = smtp_sender
    msg['To'] = smtp_to
    #context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp, 587) as server:
        server.user =
        server.password =
        #server.auth_plain()
        server.login(smtp_sender, server.password)
        server.sendmail(smtp_sender, smtp_to, msg)
        #server.send_message(msg)
