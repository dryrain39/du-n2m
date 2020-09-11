import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_mail(config, subject, html, text):
    smtp = smtplib.SMTP(config["server"]["addr"], config["server"]["port"])
    smtp.ehlo()
    smtp.starttls()
    smtp.login(config["account"]["id"], config["account"]["pw"])

    msg = MIMEMultipart("alternative")
    msg.attach(MIMEText(text, 'plain'))
    msg.attach(MIMEText(html, 'html'))

    msg['Subject'] = subject
    msg['From'] = config["sender"]
    msg['To'] = config["sendto"]
    smtp.sendmail(config["sender"], config["sendto"], msg.as_string())

    smtp.quit()
