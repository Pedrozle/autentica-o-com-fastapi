import smtplib
import email.message

def enviar_email(corpo_email: str, email_seg: str):

    msg = email.message.Message()
    msg['Subject'] = "Autenticação de dois fatores"
    msg['From'] = 'pedrozle9@gmail.com'
    msg['To'] = f"{email_seg}"
    password = 'atmhekakyfyoidhn' 
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(corpo_email )

    s = smtplib.SMTP('smtp.gmail.com: 587')
    s.starttls()
    # Login Credentials for sending the mail
    s.login(msg['From'], password)
    s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
    print('Email enviado')
