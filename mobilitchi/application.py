from flask import Flask, request, render_template, session, url_for,redirect, jsonify
import sqlite3, os, math, bcrypt, ast, datetime, random, smtplib, re, webbrowser
from flask_apscheduler import APScheduler
from unidecode import unidecode
import modules.central as central
from modules.central import sms_free, mail_free


application = app = Flask(__name__)
scheduler=APScheduler()
app.secret_key=os.urandom(24)
database=central.database.database('test')
mail_engine=central.mail()

def sender_dec(types, code, station, metode_dict, mail, user_id):
	for vl in range(10):
		time.sleep(1)
		horaire_message=central.horaire_.get_horaire(types, code, station)
		if type(horaire_message)==dict:
			break
	for key, value in metode_dict.items():
		if key==mail_free:
			horaire_message=central.message_treatment.message_rep(central.json_gestion.detype(types), code, station.replace("+", " "), horaire_message, 'html')
			message=horaire_message.replace('%', ' ')
			mail_free(value, message, central.mail_create.message_create(message, central.get_link()))
		else:
			horaire_message=central.message_treatment.message_rep(central.json_gestion.detype(types), code, station.replace("+", " "), horaire_message, 'sms')
			message=horaire_message.replace('%', ' ')
			sms_free(message, value)
	enregistre_envoie(metode_dict, mail, code, station, types, str(datetime.date.today().strftime('%D')), 'facturation')



def enregistre_envoie(recent_plat_l, mail, nom, station, types, date, met):
	data = database.select_with_c({"key":("recent"), "table":("user"), "condition": [("mail"), (mail,)] })
	recent= {"data":[],"data_len":0 } if str(data)=="(None,)" else ast.literal_eval("".join(data)) 
	if met=='facturation':
		recent['data'].append({'data'+str(int(recent["data_len"])+1):{'heure':datetime.datetime.now().strftime('%H:%M'), 'prix':0, 'nom': nom, 'station':station, 'type': types, 'date': date}})
	recent['data_len']=int(recent['data_len'])+1
	database.update({"key":"user", "table":"recent", "to_set": str(recent) ,"condition": ["mail", mail,]})
	return True


def progra_plat(types, nom, station, platform_dict, mail, user_id):
	sender_dec(types, nom, station , platform_dict, mail, user_id)

def rp(a):
	a=list(a)
	while a[0]=='%':
		del a[0]
	while a[len(a)-1]=='%':
		del a[len(a)-1]
	return ''.join(a)

def subtract_h(heure):
	heure=heure.split(':')
	if heure[0]=="00":
		heure[0]="23"
	else:
		heure[0]=str(int(heure[0])-1)
	return heure[0]+":"+heure[1]


@app.route('/factice/horaire.recv/ppv4.fr/PMNDnnnnDN2301opzddfDn/<mail>')
def tst_index(mail):
	try:
		horaire_message=central.horaire_.get_horaire('metro', '8', 'balard')
		horaire_message=central.message_treatment.message_rep(central.json_gestion.detype('metro'), '8', 'balard', horaire_message, 'html')
		mail_engine.send_mail(mail, "Essaie Mobilit'chi!",horaire_message, central.mail_create.message_create(horaire_message, central.get_link()))
		return central.json_interact['session_essaie']['sucess']
	except:
		return central.json_interact['session_essaie']['unsucess']


@app.route('/recent-activite')
def activite():
	if session.get('mail'):
		data = database.select_with_c({"key":("recent"), "table":("user"), "condition": [("mail"), (session["mail"],)]})
		print(data)
		if data==(None,):
			return render_template('recent.html', data=data, lens=0)
		data=ast.literal_eval(''.join(data))
		data_l_in_l=[list(list(list(data['data'])[x].values())[0].values()) for x in range(int(data['data_len']))]
		data = [item for sublist in data_l_in_l for item in sublist]
		return render_template('recent.html', data=data, lens=len(data))
	else:
		return redirect(url_for('connexion_try'))


@app.route('/supp/<p>/', methods=['post', 'get'])
def supp(p):
	if session.get('user'):
		data = database.select_with_c({"key":("data"), "table":("user") ,"condition": [("mail"), (session["mail"],)]})
		data=ast.literal_eval("".join(data))
		del data['data'][int(p)]
		data['data_len']=int(data["data_len"])-1
		data = database.update({"key":"user", "table":"data", "to_set": str(data) ,"condition": ["mail", session["mail"],]})
		session['data']=data
		session['erreur']=''
		session['sucess']='Alerte de passage supprimé.'
		return redirect(url_for('dashB',))
	else:
		return redirect(url_for('connexion_try'))



@app.route('/newkey', methods=['post', 'get'])
def newkey():
	if session.get('user'):
		number=request.form['new_number']
		mail=request.form['new_mail']
		mdp=request.form['mdpP']
		if number!='' or mail!='' or mdp!='':
			if mail=='' and mdp=='':
				up_number(number)
			elif number=='' and mdp=='':
				up_mail(mail)
			elif number=='' and mail=='':
				up_mdp(mdp)
			elif mail!='' and number!='' and mdp=='':
				up_number(number)
				up_mail(mail)
				up_mdp(mdp)
			session.pop('user',None)
			return render_template('connexion.html', inscri_sucess='Vos nouvelles coordonnées sont enregistrée ! Connecter vous !')
		else:
			return redirect(url_for('metode'))

	else:
		return redirect(url_for('co'))



def update_add_new_platform(platform, to_change):
	database.update({"key":"user", "table":platform, "to_set": str(to_change) ,"condition": ["mail", session["mail"],]})



@app.route('/admin/bypass', methods=['post', 'get'])
def admin():
	if str(request.remote_addr)=='127.0.0.1':
		return render_template('connexion_admin.html')
	else:
		return redirect(url_for('qatrcen4'))


@app.route('/admin/pw-11=123',  methods=['post', 'get'])
def admin_dir():
	if session.get('pw')!=None and session.get('pm')!=None and str(request.remote_addr)=='127.0.0.1':
		return render_template('admin.html')
	else:
		return redirect(url_for('qatrcen4'))


@app.route('/404')
def qatrcen4():
	return render_template('404.html')


@app.route('/admin/message', methods=['post', 'get'])
def admin_msg():
	if str(request.remote_addr)=='127.0.0.1':
		msg=request.form['message']
		emplacement=central.admin_dtc.get_emplacement_sqlite()
		fichier=emplacement+'/admin.sqlite3'
		connecteur= sqlite3.connect(fichier)
		curseur = connecteur.cursor()
		curseur.execute("update admin SET message=(?)",(msg,))
		connecteur.commit()
		return redirect('/admin/pw-11=123')
	else:
		return redirect(url_for('qatrcen4'))



@app.route('/admin_co', methods=['post', 'get'])
def admin_connex():
	if str(request.remote_addr)=='127.0.0.1':
		us=request.form['us']
		pw=request.form['pw']
		emplacement=central.admin_dtc.get_emplacement_sqlite()
		fichier=emplacement+'/admin.sqlite3'
		connecteur= sqlite3.connect(fichier)
		curseur = connecteur.cursor()

		#curseur.execute('create table admin (connexion, password, message)')
		#connecteur.commit()
		#curseur.execute('insert into admin (connexion, password) values (?, ?)', ( us,pw ))
		#connecteur.commit()

		curseur.execute('SELECT connexion from admin')
		check= "".join(curseur.fetchone())
		curseur.execute('SELECT password from admin')
		mdp= "".join(curseur.fetchone())
		if password_retrive(us, check) and password_retrive(pw, mdp):
			session['pw']=True
			session['pm']=True
			return redirect(url_for('admin_dir'))
		else:
			return redirect(url_for('admin'))
	else:
		return redirect(url_for('home'))



@app.route('/number.new', methods=['post', 'get'])
def add_number():
	number=request.form['number_user']
	if number[0:3]=="+33" or number=='':
		if number=='':
			update_add_new_platform('sms', "")
		try:
			int(number[4: len(number)])
			update_add_new_platform('sms', number)
			session['success_plat']='Numéro changé.'
		except:
			session['erreur_plat']='Entrer un numéro valide et français pour continuer.'
			return redirect(url_for('metode'))
	else:
		session['erreur_plat']="Entrer un numéro français et valide."
	return(redirect(url_for('metode')))



@app.route('/mail.new', methods=['post', 'get'])
def add_mail():
	new_mail=request.form['mail_user']
	if '@' in new_mail and '.' in new_mail:
		update_add_new_platform('mail', new_mail)
		session['success_plat']='Adresse mail changé.'
		session['user']=new_mail
		session['mail']=new_mail
		return redirect(url_for('metode'))
	else:
		session['erreur_plat']='Format de votre adresse mail invalide.'
		return redirect(url_for('metode'))


@app.route('/messenger.new', methods=['post', 'get'])
def add_messenger():
	messenger=request.form['messenger_user']
	update_add_new_platform('messenger', messenger)
	session['success_plat']='Messenger changer'
	session['erreur_plat']='Entrer un nom messenger valide.'
	return(redirect(url_for('metode')))


@app.route('/whatsapp.new', methods=['post', 'get'])
def add_whatsapp():
	number=request.form['whatapp_user']
	if number[0:3]=="+33" or number=="":
		if number=='':
			update_add_new_platform('WhatsApp', "")
		try:
			int(number[4: len(number)])
			update_add_new_platform('WhatsApp', number)
			session['success_plat']='Numéro WhatsApp changé.'
		except:
			session['erreur_plat']="Entrer un numéro français et valide."
			return redirect(url_for('metode'))
	else:
		session['erreur_plat']="Entrer un numéro français et valide."
	return(redirect(url_for('metode')))




@app.route('/delete_user', methods=['post', 'get'])
def delete_user():
	database.delete({"key":("user"), "condition": [("mail"), (session["mail"],)]})
	session.pop('user',None)
	return render_template('connexion.html', inscri_sucess="Votre compte à été supprimé. N'hésiter pas à vous inscrire !")


@app.route('/request_log_try_v_43_32log', methods=['post','get'])
def request_():
	emplacement=central.admin_dtc.get_emplacement_sqlite()
	fichier=emplacement+'/test.sqlite3'
	connecteur= sqlite3.connect(fichier)
	curseur = connecteur.cursor()
	d=curseur.execute('SELECT * from user')
	for i in d:
		pass
	connecteur.commit()
	curseur.close()
	connecteur.close()
	return redirect(url_for('home'))


@app.route('/metode', methods=['post', 'get'])
def metode():
	if session.get('user'):
		try:
			data=database.select_with_c({"key":("sms"), "table":("user"), "condition": [("mail"), (session["mail"],)]})
			sms="".join(data)
			if sms=='':
				sms='Aucun numéro enregistré'
		except:
			sms='Aucun numéro enregistré'
		try:
			e=session['erreur_plat']
		except:
			session['erreur_plat']=""
		try:
			e=session['success_plat']
		except:
			session['success_plat']=""
		return render_template('methode.html', user=session['user'], mail=session['mail'], sms=sms, erreur=session['erreur_plat'], sucess=session['success_plat'])
	else:
		return redirect(url_for('co'))

def id_regis():
	emplacement=central.admin_dtc.get_emplacement_sqlite()
	fichier=emplacement+'/id.sqlite3'
	connecteur= sqlite3.connect(fichier)
	curseur = connecteur.cursor()
	curseur.execute('create table id (id TEXT)')
	connecteur.commit()



def atribute_check(a):
	emplacement=central.admin_dtc.get_emplacement_sqlite()
	fichier=emplacement+'/id.sqlite3'
	connecteur= sqlite3.connect(fichier)
	curseur = connecteur.cursor()
	id_l=curseur.execute('SELECT * from id')
	for i in id_l:
		if int(remove(str(i)))==a:
			return False
	curseur.execute('insert into id values (?)', (a,))
	connecteur.commit()
	curseur.close()
	connecteur.close()
	return True

def atribute_id():
	id_=random.randint(10000000, 90000000)
	while 1:
		if atribute_check(id_)==True:
			break
		else:
			id_=random.randint(10000000, 90000000)
	return id_

def data_(username, passW):
	wait = database.select_with_c({"key":"nom", "table":"user", "condition": ["mail", (username,)]})
	if remove(str(wait))==None or remove(str(wait))=='None':
		return None
	else:
		session['pren']=remove(str(wait))

	wait = ''.join(database.select_with_c({"key":("mot_de_passe"), "table":("user"), "condition": [("mail"), (username,)]}))
	if password_retrive(passW, wait)==True:
		wait = ''.join(database.select_with_c({"key":("data"), "table":("user"), "condition": [("mail"), (username,)]}))
		if wait.isnumeric():
			return 'Validation'
	else:
		return False
	return True

def whith_check(env_met):
	if env_met=='sms':
		data = database.select_with_c({"key":("sms"), "table":("user"), "condition": [("mail"), (session["mail"],)]})
		for e in data:
			if (remove(str(e)))==None:
				return False
		return True
	if env_met=='mail':
		return not session["mail"].isnumeric()

@app.route('/envoie_method', methods=['post', 'get'])
def envoie_method():
	env_met=request.form['send_method']
	data = database.select_with_c({"key":("valid"), "table":("user"), "condition": [("mail"), (session["mail"],)]})
	for i in dav:
		i=remove(str(i))
	if whith_check(env_met)==True:
		data = database.update({"key":"user", "table":"valid", "to_set": str(env_met) ,"condition": ["mail", session["mail"],]})
		session['envois']=env_met
		session['erreur']=''
	else:
		if env_met=='sms':
			session['erreur']="Aucun numéro enregistré"
		else:
			session['erreur']="Aucune adresse mail enregistré"
	return redirect(url_for('dashB',))

@app.route('/station_', methods=['post','get'])
def station_():
	if session.get('user'):
		types=request.form['type']
		code=request.form['code']
		station=central.station_get.station_(types, code)
		if station==False:
			session['erreur']='Transport non-reconnu'
			session['station']=['Transport non-reconnu']
		else:
			session['station']=station
		return redirect(url_for('dashB'))

@app.route('/validation.link/<username>/<code>/',methods=['POST','GET'])
def validation_link(username, code):
	number_check=number_check_v(username)
	if str(code)==number_check:
		create_update_dt(username)
		session['user']=username
		session['envois']='mail'
		return 'Votre compte a été valider. Connecter vous à votre compte Mobilitchi pour continuer.'
	else:
		return 'Code de validation faux. Suivez le lien envoyé à votre adresse mail '+username+ '\n Please follow the link send to '+username

def number_check_v(mail):
	data = database.select_with_c({"key":("data"), "table":("user"), "condition": [("mail"), (mail,)]})
	number_check=remove(str(data)).replace(' ', '')
	return number_check

@app.route('/validation.log/',methods=['POST','GET'])
def validation():
	if session.get('mail'):
		username=session['mail']
		number_check=number_check_v(username)
		print(number_check)
		if str(request.form['validN'])==number_check:
			create_update_dt(username)
			session['data']=''
			session['user']=username
			session['envois']='mail'
			return redirect(url_for('dashB',))
		else:
			return render_template('validation.html',user=session['mail'], error='Code de validation incorrect')
	else:
		return redirect(url_for('connexion_try'))

def create_update_dt(mail):
	data=str({'data':[], 'data_len': 0})
	database.update({"key":"user", "table":"data", "to_set": str(data) ,"condition": ["mail", mail,]})

@app.route('/connexion.log',methods=['POST','GET'])
def connexion_try():
	if request.method =='POST':
		name=request.form['mailP']
		passW=request.form['password']
		session['mail']=name
		enter=data_(name,passW)

		session['station']=''
		session['met']=''
		session['erreur']=''
		if enter=='Validation':
			session['mail']=name
			return render_template('validation.html', user=name)

		elif enter=='version':
			session['user']=name
			return redirect(url_for('version'))

		elif enter==None:
			session.pop('user',None)
			return render_template('connexion.html',username_err="Adresse mail non-reconnu.")

		elif enter==False:
			session.pop('user',None)
			return render_template('connexion.html',username_err='Mot de passe incorrect.')

		elif enter==True:
			session['user']=name
			return redirect(url_for('dashB'))

	else:
		try:
			e=session["sucess"]
		except:
			session["sucess"]=''
		return render_template('connexion.html', inscri_sucess=session["sucess"])

def format(mailf):
	if mailf==None:
		session['envois']='sms'
	else:
		session['envois']='mail'
	return session['envois']


def user_id_check(user_id):
	user_i=database.select({"key":("user_id"), "table":("user")})
	for i in user_i:
		if int(''.join(remove(str(i))))==user_id:
			curseur.close()
			connecteur.close()
			return False
	return True

def change_password(mail, user_id):
	if user_id_check(user_id) and exist_clien(mail):
		session['sucess']='Un email vous à été envoyé à l\'adresse mail suivante : '+mail

def change_pass(mail, user_id, password):
	emplacement=central.admin_dtc.get_emplacement_sqlite()
	fichier=emplacement+'/test.sqlite3'
	connecteur= sqlite3.connect(fichier)
	curseur = connecteur.cursor()
	password=password_hash(password)
	curseur.execute("update user SET mot_de_passe=(?) WHERE (mail,user_id)=(?,?)", (password, mail, user_id))
	connecteur.commit()
	curseur.close()
	connecteur.close()

@app.route('/password.up/<mail>/<user_id>/<rd>',methods=['POST','GET'])
def changer_passw(mail, user_id, rd):
	if session.get('bypass')!=None and user_id_check(user_id)==True and exist_clien(mail)==True:
		return render_template('change_mdp.html', mail=mail, user_id=user_id)
	else:
		return render_template('404.html')


@app.route('/password.ups/<mail>/<user_id>/',methods=['POST','GET'])
def passW_change(mail, user_id):
	password=request.form['password']
	if password==request.form['password_confi']:
		change_pass(mail, user_id, password)
		session['sucess']='Votre mot de passe à été modifié. Connecter vous pour continuer'
		return redirect(url_for('connexion_try'))

@app.route('/password.change_clear',methods=['post'])
def pw_change_route():
	mail=request.form['mail_user']
	user_id=get_user_id(mail)
	session['bypass']='True'
	message='Lien de modification de votre mot de passe : '+central.get_link()+'/password.up/'+mail+'/'+str(user_id)+'/'+str(random.randint(1000000, 10000000))
	mail_engine.send_mail(mail,'Changement de votre mot de passe Mobilitchi', message, render_template("mail_template.html", message=message, link=central.get_link()))
	change_password(mail, user_id)
	return redirect(url_for('connexion_try'))


@app.route('/password.change')
def pass_wchange():
	return render_template('mail_mdp_c.html')

def password_hash(password):
	password=password.encode()
	h_password=bcrypt.hashpw(password, bcrypt.gensalt())
	return h_password.decode()

def password_retrive(password_check, password_org):
	password_check=password_check.encode()
	password_org=password_org.encode()
	return True if bcrypt.checkpw(password_check, password_org) else False

def create_data(username, password, coordonn):
	fir=random.randint(1000000,9000000)
	while True:
		user_id=random.randint(100000,900000)
		if user_id_check(user_id)==True:
			break
	session['valid']=fir
	if exist_clien(coordonn)==True:
		return False
	password=password_hash(password)
	database.insert({"key":"user", "table_tpl":"(nom, mail, mot_de_passe, data, user_id, total_disponible, version, month, month_send)", "data_tpl":(username, coordonn, password, fir, user_id, '10', '', '0', '0')})
	return True

def exist_clien(mail):
	data = database.select_with_c({"key":("data"), "table":("user"), "condition": [("mail"), (mail,)]})
	try:
		if type(''.join(data))==str:
			return True
	except:
		return False

def remove(a):
	a=a.replace('\\','').replace(')','').replace('(','').replace("'",'').replace(",",'').replace("[",'').replace("]",'')
	return a

def number(mail):
	emplacement=central.admin_dtc.get_emplacement_sqlite()
	fichier=emplacement+'/test.sqlite3'
	connecteur= sqlite3.connect(fichier)
	curseur = connecteur.cursor()
	curseur.execute("SELECT sms FROM user WHERE (mail)=(?)",(mail,))
	try:
		if "".join(curseur.fetchone())!='':
			return True
		else:
			return False
	except:
		return False

def get_user_platform_id(platform_list, mails, user_id):
	emplacement=central.admin_dtc.get_emplacement_sqlite()
	fichier=emplacement+'/test.sqlite3'
	connecteur= sqlite3.connect(fichier)
	curseur = connecteur.cursor()
	platform_dict={}
	platform_func={'mail':central.mail_free, 'sms':central.sms_free}
	if "sms" in platform_list and len(platform_list)==1:
		curseur.execute("SELECT sms FROM user WHERE (mail, user_id)=(?,?)",(mails, user_id))
		try:
			e="".join(curseur.fetchone())
			if e=='':
				session['erreur']="Aucun compte "+central.json_gestion.platform("sms")+' enregistré sur votre compte. Rendez vous dans paramètre pour en ajouter.'
			else:
				platform_dict[platform_func["sms"]]=e
		except:
			session['erreur']="Aucun compte "+central.json_gestion.platform("sms")+' enregistré sur votre compte. Rendez vous dans paramètre pour en ajouter.'
	elif "sms" in platform_list:
		curseur.execute("SELECT sms FROM user WHERE (mail, user_id)=(?,?)",(mails, user_id))
		try:
			e="".join(curseur.fetchone())
			if e=='':
				session['erreur']="Aucun compte "+central.json_gestion.platform("sms")+' enregistré sur votre compte. Rendez vous dans paramètre pour en ajouter.'
			else:
				platform_dict[platform_func["sms"]]=e
		except:
			session['erreur']="Aucun compte "+central.json_gestion.platform("sms")+' enregistré sur votre compte. Rendez vous dans paramètre pour en ajouter.'

	if "mail" in platform_list:
		platform_dict[platform_func["mail"]]=mails
	return platform_dict

def subtract_h(heure):
	heure=heure.split(':')
	if heure[0]=="00":
		heure[0]="23"
	else:
		heure[0]=str(int(heure[0])-1)
	return heure[0]+":"+heure[1]

@app.route('/postdata', methods=['GET','POST'])
def add_data():
	jour=['Monday','Tuesday','Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
	platform=['mail', 'sms', 'WhatsApp']
	if session.get('user'):
		mail=session['mail']
		jours_l=[i for i in jour if request.form.get(i) != None]
		platform_l=[i for i in platform if request.form.get(i) != None]
		if not number(session['mail']):
			platform_l.remove("sms")
		types=request.form['type'].replace(' ', '')
		nom=request.form['nom_transport'].replace(' ','%')
		station=rp(request.form['station'].replace(' ','%'))
		heure=request.form['heure'].replace(' ','')
		#heure=subtract_h(heure)
		jour_schedule=(''.join([i.lower()[0:3]+'-' for i in jours_l if i!='']))
		id_=str(atribute_id())#sarusmandu92@gmail.com
		user_id=get_user_id(mail)
		platform_dict=get_user_platform_id(platform_l, mail, user_id)
		if platform_dict==False:
			return redirect(url_for('dashB',))

		station=central.station_get.station_comp(types, nom, station)
		if station:
			if len(jours_l)>1:
				for i in jours_l:
					shedule_add(id_, central.json_gestion.types(types), nom, station, heure[0:2], heure[3:5], i.lower()[0:3]+'d', platform_dict, mail, user_id)
					id_=str(atribute_id())#sarusmandu92@gmail.com
			else:
				shedule_add(id_, central.json_gestion.types(types), nom, station, heure[0:2], heure[3:5], jour_schedule, platform_dict, mail, user_id)
			data = database.select_with_c({"key":("data"), "table":("user"), "condition": [("mail"), (mail,)]})
			data=ast.literal_eval("".join(data))
			data['data'].append({id_:{'platform':platform_l, 'heure':heure, 'types':types, 'nom':nom, 'station':station, 'jours': jours_l }})
			data['data_len']=str(int(data['data_len'])+1)
			data = database.update({"key":"user", "table":"data", "to_set": str(data) ,"condition": ["mail", mail]} )
			session['erreur']=''
			session['sucess']='Votre alerte de passage à été ajouté avec succès !'
		else:
			session['sucess']=''
			session['erreur']="Transport non-reconnu. Ajouter un transport proposé par la RATP."
		return redirect(url_for('dashB',))
	else:
		return redirect(url_for('connexion_try'))

@app.route('/detail')
def detail():
	return render_template('elements.html')

@app.route('/contact')
def contact():
	msg=session.get('msg') if session.get('msg')!=None else ''
	return render_template('contact.html', msg=msg)

@app.route('/contact/message/receive/<nom>/<mail>/<message>')
def get_msg_contact(nom, mail, message):
	message= str(unidecode('NOM: {nom}\n MAIL: {mail}\n MESSAGE: {message}\n').format(nom=nom, mail=mail, message=message))
	mail_engine.send_mail('sarusmandu92@gmail.com', 'MSG', message, render_template("mail_template.html", message=message, link=central.get_link()))
	mail_engine.send_mail(mail, 'Reception de votre message', "Nous avons bien recu votre demande. Vous obtiendrez une reponse sous 48 heures. ", render_template("mail_template.html", message=message, link=central.get_link()))
	session["msg"]='Votre demande à été envoyer. Nous vous prendrons en charge sous 48h.'
	return redirect(url_for('contact'))

def trad_day():
	pass

@app.route('/dash',methods=['POST','GET'])
def dashB():
	if session.get('mail'):
		mail=session['mail']
		data = database.select_with_c({"key":("data"), "table":("user"), "condition": [("mail"), (mail,)]})
		data=ast.literal_eval("".join(data))
		dayd=central.json_gestion.trad_days()
		user=session.get('pren') if session.get('pren')!=None and session.get('pren')!='' else mail
		session['erreur']=session.get('erreur') if session.get('erreur')!=None  else ''
		session['sucess']=session.get('sucess') if session.get('sucess')!=None else ''
		return render_template('dashboard.html', user=user,len=int(data['data_len']), data = data, 
				station=session['station'], leni=len(session['station']), meta=session['met'], erreur=session['erreur'],
		 		succes=session['sucess'], get_day=dayd, nbr=number(mail))

	else:
		return redirect(url_for('connexion_try'))

def get_user_id(mail):
	data = database.select_with_c({"key":("user_id"), "table":("user"), "condition": [("mail"), (mail,)]})
	return ("".join(data))

def alert_m():
		emplacement=central.admin_dtc.get_emplacement_sqlite()
		fichier=emplacement+'/admin.sqlite3'
		connecteur= sqlite3.connect(fichier)
		curseur = connecteur.cursor()
		curseur.execute("SELECT message FROM admin")
		t="".join(curseur.fetchone())
		return t

@app.route('/', methods=['GET','POST'])
def home():
	return render_template('index.html', message=str(alert_m()))

@app.route('/inscription')
def inscription():
	return render_template('inscription.html')

@app.route('/co')
def co():
	if session.get('user'):
		return redirect(url_for('dashB'))
	else:
		return render_template('connexion.html')

@app.route('/logout')
def logout():
	session.pop('user',None)
	return redirect(url_for('home'))

def shedule_cancel(id_):
	try:
		scheduler.remove_job(str(id_))
	except:
		pass

def  shedule_add(id_, types, nom, station, heure, minute, day, platform_dict, mail, user_id):
	day=day[0:len(day)-1]
	if str(heure)+':'+str(minute)==datetime.datetime.now().strftime("%H:%M"):
		progra_plat(types, nom, station, platform_dict, mail, user_id)
	else:
		scheduler.add_job(id=str(id_), func=progra_plat, trigger='cron', args=[types, nom, station, platform_dict, mail, user_id] ,day_of_week=day,  hour=heure, minute=minute)

@app.route('/condition',methods=['POST','GET'])
def condition():
	return render_template('protected.html')

@app.route('/inscri?',methods=['POST','GET'])
def dmd_in():
	name=request.form['nomP']
	mail=request.form['mailP']
	mdp=request.form['mdpP']
	if create_data(name, mdp,mail)==True:
			message='Bonjour,\n\n Votre code de validation est '+str(session['valid'])+' \n Lien de validation : \n '+central.get_link()+'/validation.link/'+mail+'/'+str(session['valid'])
			if mail_engine.send_mail(mail, "Validation de votre compte Mobilit'chi",message, render_template("mail_template.html", message=message, link=central.get_link())):
				return render_template('connexion.html', inscri_sucess='Votre inscription a été enregistrer ! Vérifier vos messages pour valider votre inscription !')
			else:
				return render_template('inscription.html',erreur='Entrer une adresse mail valide.')
	else:
		return render_template('inscription.html',erreur='Votre adresse mail ou numéro est déja utilisé. Essayez de vous connecter.')

@app.errorhandler(404)
def error_404(e):
	return render_template('404.html'), 404

@app.before_first_request
def reload():
	mail_l = database.select({"key":"mail", "table":"user"})
	mail_l=["".join(x) for x in mail_l]
	error_l=[]
	for i in range(len(mail_l)):
		data = database.select_with_c({"key":"data", "table":"user", "condition": [("mail"), (mail_l[i],)]})
		data=ast.literal_eval("".join(data))
		if type(data)==dict:
			try:
				us_=get_user_id(mail_l[i])
				for x in range(int(data['data_len'])):
					list(data['data'][x].values())[0]['id_']= list(data['data'][x])[0]
				d=[list(data['data'][x].values()) for x in range(int(data['data_len']))]
				d = [item for sublist in d for item in sublist]
				for x in range(len(d)):
					id_=d[x]['id_']
					if len(d[x]['jours'])>3:
						for m in d[x]['jours']:
							shedule_add(id_, d[x]['types'], d[x]['nom'], d[x]['station'], (d[x]['heure'])[0:2], (d[x]['heure'])[3:5], m.lower()[0:4],get_user_platform_id(d[x]['platform'],mail_l[i] , us_), mail_l[i], us_) 
							id_=str(atribute_id())
					else:
						shedule_add(d[x]['id_'], d[x]['types'], d[x]['nom'], d[x]['station'], (d[x]['heure'])[0:2], (d[x]['heure'])[3:5], (''.join([i.lower()[0:3]+'-' for i in d[x]['jours'] if i!=''])),get_user_platform_id(d[x]['platform'],mail_l[i] , us_), mail_l[i], us_) 
			except:
				error_l.append(mail_l[i])
	print(f'FAIT {str(error_l)} {datetime.datetime.now().strftime("%H:%M:%S")}')



@app.route('/recept-message', methods=['POST','GET'])
def recept():
	message=request.get_data()
	number=message.split()[0]
	data = database.select_with_c({"key":("data"), "table":("user"), "condition": [("sms"), (number,)]})
	try:
		if type(''.join(data))==str:
			central.response_app.get_message(message)
	except:
		central.sms_free(number, "Vous n'etes pas inscrit😔. Rendez vous sur mobilitchi.com/inscri pour en profiter gratuitement!")




if __name__ == '__main__':
	scheduler.start()
	app.run(debug=True, port=8000)


