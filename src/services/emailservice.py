import os
import smtplib
from email.message import Message
from dotenv import load_dotenv

load_dotenv()

email_address = os.getenv('EMAIL_ADDRESS')
psw = os.getenv('EMAIL_PSW')

class EmailService:
    def __init__(self):
        self.email_address = email_address
        self.psw = psw

    def enviar_email(self, subj: str, corpo_email: str, email_seg: str):

        msg = Message()
        msg['Subject'] = subj
        msg['From'] = self.email_address
        msg['To'] = email_seg
        password = self.psw 
        msg.add_header('Content-Type', 'text/html')
        msg.set_payload(corpo_email)
        r =  {'from': self.email_address, 'psw': self.psw}
        print(r)

        s = smtplib.SMTP('smtp.gmail.com: 587')
        s.starttls()
        # Login Credentials for sending the mail
        s.login(msg['From'], password)
        s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
        print('Email enviado')
        s.quit()