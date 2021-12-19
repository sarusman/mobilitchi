def types(name):
	types={
		"bus":"buses",
		"metro":"metros",
		"tramway":"tramways",
		"noctilien":"noctiliens",
		"rer": "rers"
	}
	try:
		return types[name]
	except:
		return name

def detype(name):
	types={
		"buses":"bus",
		"metros":"metro",
		"tramways":"tramway",
		"noctiliens":"noctilien",
		"rers": "rer"
	}
	try:
		return types[name]
	except:
		return name



def platform(name):
	platform={
		"what_app": "WhatsApp",
		"messenger":"Messenger",
		"discord":"Discord",
		"sms":"Numéro",
		"mail":"adresse mail"

	}
	return platform[name]


def trad_days():
	return { "Monday": "Lundi",
	"Tuesday": "Mardi",
	"Wednesday":"Mercredi",
	"Thursday":"Jeudi",
	"Friday":"Vendredi",
	"Saturday":"Samedi",
	"Sunday":"Dimanche"
	}


def trad_day(day):
	day_a={ "Monday": "Lundi",
	"Tuesday": "Mardi",
	"Wednesday":"Mercredi",
	"Thursday":"Jeudi",
	"Friday":"Vendredi",
	"Saturday":"Samedi",
	"Sunday":"Dimanche"
	}
	try:
		return [day_a[i] for i in day]
	except:
		return day











