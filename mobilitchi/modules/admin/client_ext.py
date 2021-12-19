from . import admin_dtc 
def client_exist(number):
	emplacement=admin_dtc.get_emplacement_sqlite()
	fichier=emplacement+'/test.sqlite3'
	connecteur= sqlite3.connect(fichier)
	curseur = connecteur.cursor()
	curseur.execute('SELECT mail FROM user WHERE (sms)=(?)', (str(number),))
	try:
		mail="".join(curseur.fetchone())
	except:
		return False
	curseur.execute('SELECT user_id FROM user WHERE (sms)=(?)', (str(number),))
	user_id="".join(curseur.fetchone())
	return [mail, user_id]