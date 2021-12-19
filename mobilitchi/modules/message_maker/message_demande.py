from ..import central

def horaire_send(types, code , station):
	return horaire_.get_horaire(types, code , station)


def stationd(types, code):
	return f'Station desservi par la ligne {code}: \n'+', '.join(station_get.station_(types, code))


def message_rep(message):
	messages=message.lower().split(' ')
	if 'aid' in messages:
		return'Pour avoir un horaire de passage : horaire <type> <nom> <station>.\nPour avoir les stations : station <type> <nom>'
	messages=[i.lower() for i in messages if i!='']
	meta=messages[0]
	types=messages[1]
	nom=messages[2]
	if 'sta'in meta:
		nom=''.join([messages[c] for c in range(2,len(messages))]).lower().replace(' ','+')
		return stationd(types, nom.replace(' ', '%'))

	elif 'hor' in meta:
		try:
			station=messages[3]
			station=''.join([messages[c] for c in range(3,len(messages))])
		except:
			pass
		station=station_get.station_comp(types,nom, station)
		if station==False:
			return "'Votre transport n'est pas reconnu.' Demander moi uniquement des transport RATP. (cette demande n'a pas été facturé sur votre compte)"
		if "n'est pas disponible" in station:
			return "'Votre transport n'est pas reconnu.' Demander moi uniquement des transport RATP. (cette demande n'a pas été facturé sur votre compte)"
		return horaire_send(types, nom, station.lower().replace(' ','+')).replace('+', ' ')
	else:
		return 'Je ne comprend pas votre demande. Pour avoir un horaire de passage : horaire <type> <nom> <station>. Pour avoir les stations : station <type> <nom>'