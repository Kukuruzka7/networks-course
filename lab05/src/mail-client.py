import argparse
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os


def send_email(receiver_email, subject, message, format='txt'):
    smtp_server = os.getenv("SERVER")
    port = int(os.getenv("PORT"))
    sender_email = os.getenv("MAIL")
    password = os.getenv("PASSWORD")

    msg = MIMEMultipart()
    msg['From'] = sender_email
    # мне очень хотелось поменять отправителя, но никто мне не разрешал этого сделать :(
    # а в spbu.ru не получилось зайти
    msg['To'] = receiver_email
    msg['Subject'] = subject

    if format == 'html':
        body = MIMEText(message, 'html')
    else:
        body = MIMEText(message, 'plain')

    msg.attach(body)

    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()
        server.starttls()
        server.login(sender_email, password)
        server.send_message(msg)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('email')
    args = parser.parse_args()
    receiver_email = args.email
    subject_html = 'Письмо в html'
    message_html = '<h1>Ура, оно пришло!</h1>'
    send_email(receiver_email, subject_html, message_html, format='html')
    subject_txt = 'Письмо в txt'
    message_txt = 'Ура, оно пришло!\nС уважением,\nРозалина'
    send_email(receiver_email, subject_txt, message_txt)
