import smtplib, requests
from unidecode import unidecode
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def sms_free(message, numéro):
	report = {"value1": numéro, "value2": 'Mobilitchi\n'+message}
	try:
		requests.post("https://maker.ifttt.com/trigger/trigger_ifttte/with/key/dq4uw7XCdzOpCk_uiTWcgkaC5FRtBKAVXseOc_idwES", data=report)
		return True
	except:
		requests.post("https://maker.ifttt.com/trigger/trigger_ifttte/with/key/dq4uw7XCdzOpCk_uiTWcgkaC5FRtBKAVXseOc_idwES", data="Une erreur est survenue")


def discord_free(message, id):
	...


def WhatsApp_free(message, numéro):
	...

def mail_frefe(message, dmail):
	conex=smtplib.SMTP('smtp.gmail.com:587')
	conex.starttls()
	conex.login('mobilitchi@gmail.com', 'sarusman1971')
	message='Subject: {}\n\n{}'.format('Votre horaire Mobilitchi ', unidecode('Mobilitchi\n '+message))
	conex.sendmail('mobilitchi@gmail.com', dmail ,message)
	return True


def mail_free(mail, message, bodyContent):
    message = MIMEMultipart()
    message['Subject'] = 'Votre horaire Mobilitchi'
    message['From'] = 'mobilitchi@gmail.com'
    message['To'] = mail

    message.attach(MIMEText(bodyContent, "html"))
    msgBody = message.as_string()

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login('mobilitchi@gmail.com', 'sarusman1971')
    server.sendmail('mobilitchi@gmail.com', mail ,msgBody)

    server.quit()

def messenger_free(message, nom):
	...