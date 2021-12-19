from datetime import datetime,timedelta
def message_erreur(message):
	message=message.split(' ')
	return f"Le {message[0]} {message[1]} n'est pas disponible pour le moment à l'arrêt {message[2]}."

def heure_cal(minute):
	try:
		return (datetime.now() + timedelta(minutes=int(minute))).strftime('%H:%M')
	except:
		return ''

def message_rep(types, code, station, message_dict, formats):
	try:
		if 'SERVICE' in list(message_dict.values())[0][0] and 'SERVICE' in list(message_dict.values())[1][0]:
			return f'Le service est terminé pour le {types} {code}.'
		else:
			try:
				if formats=="html":
					return ' '.join(f"<h1>Prochains passages du {types} {code} à l'arrêt {station} :</h1><br><br> %% <h2>{list(message_dict.values())[0][0]} vers {list(message_dict.keys())[0]} {' à '+heure_cal(list(message_dict.values())[0][0][0:2]) if list(message_dict.values())[0][0][0:2].isnumeric()or list(message_dict.values())[0][0][0].isnumeric()else ''} {' (prochain dans '+list(message_dict.values())[0][1] if list(message_dict.values())[0][1][0:2].isnumeric() or list(message_dict.values())[0][1][0].isnumeric()else list(message_dict.values())[0][1]}) <br> %% {list(message_dict.values())[1][0]} vers {list(message_dict.keys())[1]} {' à '+heure_cal(list(message_dict.values())[1][0][0:2]) if list(message_dict.values())[1][0][0:2].isnumeric()or list(message_dict.values())[1][0][0].isnumeric() else ''}{' (prochain dans '+ list(message_dict.values())[1][1] if list(message_dict.values())[1][1][0:2].isnumeric() or list(message_dict.values())[1][1][0].isnumeric() else list(message_dict.values())[0][1]})".split()).replace('%', '\n')+"</h2>"
				else:
					return ' '.join(f"Prochains passages du {types} {code} à l'arrêt {station} : %% {list(message_dict.values())[0][0]} vers {list(message_dict.keys())[0]} {' à '+heure_cal(list(message_dict.values())[0][0][0:2]) if list(message_dict.values())[0][0][0:2].isnumeric()or list(message_dict.values())[0][0][0].isnumeric()else ''} {' (prochain dans '+list(message_dict.values())[0][1] if list(message_dict.values())[0][1][0:2].isnumeric() or list(message_dict.values())[0][1][0].isnumeric()else list(message_dict.values())[0][1]})  %% {list(message_dict.values())[1][0]} vers {list(message_dict.keys())[1]} {' à '+heure_cal(list(message_dict.values())[1][0][0:2]) if list(message_dict.values())[1][0][0:2].isnumeric()or list(message_dict.values())[1][0][0].isnumeric() else ''}{' (prochain dans '+ list(message_dict.values())[1][1] if list(message_dict.values())[1][1][0:2].isnumeric() or list(message_dict.values())[1][1][0].isnumeric() else list(message_dict.values())[0][1]})".split()).replace('%', '\n')
			except:
				return " ".join(f"Service  indisponible  pour  le  {code}.")
	except:
		return(message_dict)