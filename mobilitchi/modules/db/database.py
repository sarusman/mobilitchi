import sqlite3 as db
import os, ast
from .. import central

class database():
	def __init__(self, name):
		self.connector=db.connect(f'{central.admin_dtc.get_emplacement_sqlite()}/{name}.sqlite3',  check_same_thread=False)
		self.cursor=self.connector.cursor()

	def create(self):
		curseur.execute('CREATE TABLE user (nom TEXT, mail TEXT, mot_de_passe TEXT, data TEXT, data_clear TEXT,  sms TEXT, send TEXT, user_id TEXT, discord TEXT, WhatsApp TEXT, messenger TEXT, TEXT, total_disponible TEXT, recent TEXT, version TEXT, month TEXT, month_send TEXT)')

	def select(self, dtc):
		self.cursor.execute("SELECT {key} FROM {table}".format(key=dtc["key"] , table=dtc["table"]))
		return self.cursor.fetchall()

	def select_with_c(self, dtc):
		self.cursor.execute("SELECT {key} FROM {table} WHERE {key1} = (?)".format(key=dtc["key"] , table=dtc["table"], key1=dtc["condition"][0]), dtc["condition"][1])
		return self.cursor.fetchone()

	def update(self, dtc):
		self.cursor.execute("UPDATE {key} SET {table}=(?) WHERE ({key1})=(?)".format(key=dtc["key"] , table=dtc["table"], key1=dtc["condition"][0]), (dtc["to_set"],dtc["condition"][1]))
		self.connector.commit()

	def insert(self, dtc):
		self.cursor.execute('INSERT INTO {key} {table_tpl} VALUES ({len_})'.format(key=dtc["key"], table_tpl=dtc["table_tpl"], len_=("?,"*len(dtc["data_tpl"]))[0:len(dtc["data_tpl"])*2-1]), dtc["data_tpl"])
		self.connector.commit()

	def delete(self, dtc):
		self.cursor.execute('DELETE FROM {key} WHERE ({key1})=(?)'.format(key=dtc['key'], key1=dtc['condition'][0]), (dtc['condition'][1]))
		self.connector.commit()

	def close(self):
		self.cursor.close()
		self.connector.close()










