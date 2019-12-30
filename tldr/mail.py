import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from tldr import conf


def send(sender, recipients, subject, **args):
    msg = MIMEMultipart("alternative")
    msg["From"] = sender
    msg["Subject"] = subject
    msg["To"] = ", ".join(recipients)

    if "text" in args:
        msg.attach(MIMEText(args["text"].encode("utf-8"), "plain"))

    if "html" in args:
        msg.attach(MIMEText(args["html"].encode("utf-8"), "html"))

    server = smtplib.SMTP_SSL(conf['SMTP_HOST'])
    server.login(conf['SMTP_USER'], conf['SMTP_PASS'])
    server.sendmail(sender, recipients, msg.as_string())
    server.quit()
