import os
import smtplib
import email.message
from dotenv import load_dotenv

load_dotenv()

email_address = os.getenv('EMAIL_ADDRESS')
psw = os.getenv('EMAIL_PSW')

def enviar_email(subj: str, corpo_email: str, email_seg: str):

    msg = email.message.Message()
    msg['Subject'] = subj
    msg['From'] = email_address
    msg['To'] = email_seg
    password = psw 
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(corpo_email)

    s = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    s.starttls()
    # Login Credentials for sending the mail
    s.login(msg['From'], password)
    s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
    print('Email enviado')
    s.quit()