from flask_restful import Resource, reqparse
from models.usuario import UserModel
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from werkzeug.security import safe_str_cmp
from blacklist import BLACKLIST
import traceback
from flask import make_response, render_template

atributos= reqparse.RequestParser()
atributos.add_argument('login', type=str, required=True, help='The field login cannot be blank')
atributos.add_argument('senha', type=str, required=True, help='The field senha cannot be blank')
atributos.add_argument('email', type=str)
atributos.add_argument('ativado', type=bool)




class User(Resource):

	def get(self, user_id):

		user = UserModel.find_user(user_id)

		if user:
			return user.json()
		return {'message': 'user not found'}, 404

	@jwt_required() # Requere login	
	def delete(self, user_id):
		user= UserModel.find_user(user_id)
		if user:
			try:
				user.delete_user()
			except:
				return{'message':'An internal error to delete from database'}, 500

			return {'message':'hotel deleted' },200
			
		return {'message':'hotel not found' },404


class UserRegister(Resource):

	def post(self):
		
		dados= atributos.parse_args()
		
		if not dados.get('email') or dados.get('email') is None:
			return {'message': "The email cannot be left blank"},400

		if UserModel.find_user_by_email(dados['email']):
			return {"message": "The mail '{}' already exists".format(dados['email'])}, 400 #BAD REQUEST


		if UserModel.find_by_login(dados['login']):
			return {"message": "Login '{}' already exists".format(dados['login'])},400 #BAD REQUEST

		user= UserModel(**dados)
		user.ativado = False # EVITA USUARIO MALISIOSO
		try:
			user.save_user()
			try:
				user.send_confirmation_email()
			except:
				return {'message':'Problem with Mailing api'}, 500 #Created
		except:
			user.delete_user()
			traceback.print_exc()

			return {'message':'Database internal error'}, 500 #Created


		return {'message':'User created successfuly confirmation email sent'}, 201 #Created


class UserLogin(Resource):

	@classmethod
	def post(cls):

		dados= atributos.parse_args()

		user= UserModel.find_by_login(dados['login'])

		if user and safe_str_cmp(user.senha, dados['senha']):
			if user.ativado:
				token_de_acesso=create_access_token(identity = user.user_id)
				return {"Access_token":token_de_acesso},200
			return {"message":'user not activated'},400
		
		return {'message':'The username or login are incorrect'}, 401 #Unathorise



class UserLogout(Resource):

	@jwt_required()
	def post(self):
		jwt_id = get_jwt()['jti'] # JWT Token identifier
		BLACKLIST.add(jwt_id)
		return {'message': 'Logged out successfully'}


class UserConfirm(Resource):
	#raiz/confirmation/{user_id}
	@classmethod
	def get(cls,user_id):
		user = UserModel.find_user(user_id)
		
		if not user:
			return{'message':"User id '{}' not found".format(user_id)}, 404

		user.ativado=True
		user.save_user()
		headers={'Content-Type':'text/html'}
		#return{'message':"User id '{}' activated succcesfully".format(user_id)}, 200
		return make_response(render_template('user_confirm.html', email=user.email, usuario=user.login),200, headers)


