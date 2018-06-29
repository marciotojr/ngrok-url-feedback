import os
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
from os.path import basename


def fetch_send(send_from, send_to, password, folder=None, convert=True):
    if convert:
        send_mail(send_from, send_to, "Convert", "", password, get_files(folder))
    else:
        send_mail(send_from, send_to, "", "", password, get_files(folder))


def get_files(folder='toSend'):
    if folder is None:
        folder = 'toSend'
    send_files = []
    queue = os.listdir(folder)
    for i in range(len(queue)):
        queue[i] = folder + os.path.sep + queue[i]
    for item in queue:
        if os.path.isfile(item):
            send_files.append(item)
        if os.path.isdir(item):
            for sub_item in os.listdir(item):
                queue.append(item + os.path.sep + sub_item)
    return send_files


def send_mail(send_from, send_to, subject, text, password, files=None):

    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = send_to
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(text))

    for f in files or []:
        with open(f, "rb") as fil:
            part = MIMEApplication(
                fil.read(),
                Name=basename(f)
            )
        # After the file is closed
        part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
        msg.attach(part)

    server = smtplib.SMTP('smtp.gmail.com', 587)
#    server.connect("smtp.gmail.com", 587)

    server.starttls()
    server.login(send_from, password)

    server.sendmail(send_from, send_to, msg.as_string())
    server.close()
