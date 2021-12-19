import  json, requests, re
from .. import central
import urllib.request as urllib2
def get_horaire(types, code, station):
	types=types.replace('%', ' ')
	station=station.lower().replace(' ', '+')
	#form_lien=urllib2.urlopen(f'https://api-ratp.pierre-grimaud.fr/v4/schedules/{json_files.types(types)}/{code}/{station}/A+R').read()
	form_lien=(requests.get(f'https://api-ratp.pierre-grimaud.fr/v4/schedules/{central.json_gestion.types(types)}/{code}/{station}/A+R').text)
	parsed_json = json.loads(form_lien)
	if parsed_json['result']['schedules'][0]['message']=='Schedules unavailable':
		return central.message_treatment.message_erreur(f'{types} {code} {station}')
	else:
		horaire={}
		for i in range(0,len(parsed_json['result']['schedules']),2):
			horaire[parsed_json['result']['schedules'][i]['destination']]=[]
		for o in range(len(parsed_json['result']['schedules'])):
			horaire[parsed_json['result']['schedules'][o]['destination']].append(parsed_json['result']['schedules'][o]['message'])
		return horaire