from .json_files import json_gestion
from .admin import admin_dtc
from .api_treatement import horaire_, station_get
from .message_maker import mail_create, message_demande, message_treatment
from .senders.send_platform_free import sms_free, mail_free
from .db import database
from .response_app import response_app
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib, json, os


with open(os.getcwd()+"/modules/json_files/interaction.json") as f:
    json_interact=json.loads(f.read())

"""
PROBLEM:
try : https://www.google.com/settings/security/lesssecureapps

"""

class mail:
    def __init__(self):
        self.server = smtplib.SMTP('smtp.gmail.com:587')
        self.server.starttls()
        self.server.login('mobilitchi@gmail.com', 'sarusman1971')

    def send_mail(self, mail,subject, message, bodyContent):
        message = MIMEMultipart()
        message['Subject'] = subject
        message['From'] = 'mobilitchi@gmail.com'
        message['To'] = mail

        message.attach(MIMEText(bodyContent, "html"))
        msgBody = message.as_string()
        self.server.sendmail('mobilitchi@gmail.com', mail ,msgBody)
        return True


def get_link():
	return "http://localhost:8000"
