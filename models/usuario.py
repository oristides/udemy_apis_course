from sql_alchemy import banco
from flask import request, url_for
import api_key_configs
import requests


MAILGUN_DOMAIN= api_key_configs.MAILGUN_DOMAIN
MAILGUN_API_KEY=api_key_configs.MAILGUN_API_KEY
FORM_TITLE= api_key_configs.FORM_TITLE 
FROM_EMAIL= api_key_configs.FROM_EMAIL


class UserModel(banco.Model):
	__tablename__= 'usuarios'

	user_id = banco.Column(banco.Integer, primary_key=True)
	login = banco.Column(banco.String(40), nullable=False, unique=True)
	senha =  banco.Column(banco.String(40), nullable=False)
	ativado = banco.Column(banco.Boolean, default=False)
	email= banco.Column(banco.String(80), nullable=False, unique=True)

	def __init__(self,login,senha, email, ativado):
		self.login=login
		self.senha=senha
		self.email = email
		self.ativado=ativado

	def send_confirmation_email(self):
		#precisa entrar no link # raiz/confirmacai/user_id
		
		# http://127.0.0.1:5000/
		#http://127.0.0.1:5000 
		link = request.url_root[:-1] +  url_for('userconfirm', user_id= self.user_id)
		return requests.post("https://api.mailgun.net/v3/{}/messages".format(MAILGUN_DOMAIN),
			auth=("api", MAILGUN_API_KEY),
			data={"from": '{}<{}>'.format(FORM_TITLE,FROM_EMAIL),
			"to": self.email,
			"subject": "Login Confirmation",
			"text": "Click to on the following link to confirm:{}".format(link),
			"html":'<html><p> lick to on the following link to confirm: <a href="{}">CONFIRMAR EMAIL</a> </p></hatml>'.format(link)
			}
			)
		

	def json(self):
		return {
		'user_id':self.user_id,
		'login':self.login,
		'ativado':self.ativado
		}

	@classmethod
	def find_user(cls, user_id):
		
		user= cls.query.filter_by(user_id=user_id).first() #Select * from hoteis where hotel_id=**hotel_id
		if user:
			return user
		return None

	@classmethod
	def find_by_login(cls, login):
		
		user= cls.query.filter_by(login=login).first() #Select * from hoteis where hotel_id=**hotel_id
		if user:
			return user
		return None
		
	@classmethod
	def find_user_by_email(cls, email):
		
		user= cls.query.filter_by(email=email).first() #Select * from hoteis where hotel_id=**hotel_id
		if user:
			return user
		return None

	def save_user(self):
		banco.session.add(self)
		banco.session.commit()

	
	def delete_user(self):
		banco.session.delete(self)
		banco.session.commit()


