import json
import os
import subprocess
import time
from email.utils import formatdate
from subprocess import call

import email_sender


def send_email(config_file='parameters.config'):
    with open(config_file) as data_file:
        parameters = json.load(data_file)
        urls = start_ngrok(parameters['PATH'],parameters['connection_type'],parameters['port'])
        subject = "NGROK started at " + parameters['machine']
        #time = strftime("%d/%m/%Y at %H:%M:%S", gmtime())
        time = formatdate(localtime=True)
        msg = parameters['user'] + ",\nThe ngrok process were set in " + parameters['machine'] + " at " + time
        msg += "\nThe available URLs are above:\n"
        for url in urls:
            url = url['public_url']
            msg += url + "\n"
        msg += "Current port: " + parameters['port']
        print(msg)
        print(subject)
        email_sender.send_mail(parameters['email-from'], parameters['email-to'], subject, msg, parameters['password'])


def start_ngrok(PATH, connection_type="http", port="80"):
    call(["pkill", "ngrok"])
    time.sleep(3)
    subprocess.Popen([PATH, connection_type, port])
    time.sleep(10)
    os.system("curl  http://localhost:4040/api/tunnels > tunnels.json")

    with open('tunnels.json') as data_file:
        datajson = json.load(data_file)

    return datajson['tunnels']


send_email()
