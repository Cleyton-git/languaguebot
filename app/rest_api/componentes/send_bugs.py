import smtplib
from email.message import EmailMessage

def Func_send_bugs(tele_id, msg_user):
    email_send = "cleytoncontato281@gmail.com"
    password_app = "pagi ppgm fjcf pgaw"

    msg = EmailMessage()
    msg['Subject'] = "Melhoria ou bug"
    msg['From'] = email_send
    msg['To'] = email_send
    msg.set_content(msg_user)
    
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=10) as smtp:
        smtp.login(email_send, password_app)
        smtp.send_message(msg)
        print("LOG EMAIL: ENVIADINHO DA SILVA")
    return
        