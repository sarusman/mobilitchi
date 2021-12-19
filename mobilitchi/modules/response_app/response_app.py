from ..senders import send_platform_free
from ..api_treatement import horaire_
import requests

def messge_treat(messge):
	messge = messge.split()
	transport_type = messge[1]
	adresse = messge[2]
	station = ''.join(messge[3:])
	return horaire_.get_horaire(transport_type, adresse, station)

def get_message(message):
	number= message.split()[0]
	try:
		only_message = messge_treat(messsge)
	except:
		only_message = 'Pour demander un horaire : "Horaire <type de transport> <numéro du transport> <station>"'
	finally:
		send_platform_free.sms_free(only_message, number)


