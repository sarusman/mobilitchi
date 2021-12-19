from .. import central
import json, sqlite3, requests
from unidecode import unidecode
def station_(types, code):
	types=types.replace('%', ' ')
	code=code.replace('%', ' ')
	emplacement=central.admin_dtc.get_emplacement_sqlite()
	fichier=emplacement+'/station.sqlite3'
	connecteur= sqlite3.connect(fichier)
	curseur = connecteur.cursor()
	#curseur.execute('create table station_exist (types, nom, station_list)')
	curseur.execute('SELECT station_list from station_exist WHERE types=? and nom=?', (types, code))
	stat_w=curseur.fetchone()
	if stat_w!=None and stat_w!=[] and type(stat_w)==list:
		curseur.close()
		connecteur.close()
		return "".join(sta_w.split('+'))
	try:
		#form_lien=urllib2.urlopen(f'https://api-ratp.pierre-grimaud.fr/v4/stations/{json_files.types(types)}/{code}').read()
		form_lien=(requests.get(f'https://api-ratp.pierre-grimaud.fr/v4/stations/{central.json_gestion.types(types)}/{code}').text)
	except:
		print(f'https://api-ratp.pierre-grimaud.fr/v4/stations/{central.json_gestion.types(types)}/{code}')
		curseur.close()
		connecteur.close()
		return False
	parsed_json = json.loads(form_lien)
	try:
		station_list= [parsed_json['result']['stations'][i]['name'] for i in range(len(parsed_json['result']['stations']))]
		curseur.execute('insert into station_exist (types, nom, station_list) values (?,?,?)',  (types, code, '+'.join(station_list)))
		connecteur.commit()
		curseur.close()
		connecteur.close()
		return station_list
	except :
		return False


def station_comp(types, code,station):
	station_l=station_(types, code)
	if station_l==False:
		return False
	for i in range(len(station_l)):
		if unidecode(station.replace('%', '').lower()) in unidecode(station_l[i].replace(' ', '').lower()):
			return station_l[i]
	return False





