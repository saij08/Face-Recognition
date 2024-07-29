##https://www.youtube.com/watch?v=CBuu17j_WnA
##myaccount.google.com\lesssecureapps

import smtplib
from email.message import EmailMessage
import os

def send(send_to,name):
    print(send_to)
    print(name)
    sender_mail_id = '@gmail.com'
    password = ''

    msg = EmailMessage()
    msg['Subject'] = 'Attendance status of ' + name
    msg['From'] = sender_mail_id
    msg['To'] = send_to
    msg.set_content(name + " is absent today. Please tell him/her do not bunk the lectures")

    with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp:

        smtp.login(sender_mail_id,password)
        smtp.send_message(msg)
