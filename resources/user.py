import sqlite3
from flask_restful import Resource,Api,reqparse
from db import db
from models.user import UserModel
from werkzeug.security import safe_str_cmp
from flask import jsonify


class UserRegister(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument('username',
		type=str,
		required=True,
		help="This field cannot be blank"
		)

	parser.add_argument('password',
		type=str,
		required=True,
		help="This field cannot be blank"
		)

	def post(self):
		data = UserRegister.parser.parse_args()
		
		if UserModel.find_by_username(data['username']):
			return {"message" : "user exists"},400

		user = UserModel(data['username'],data['password'])
		user.save_to_db()
		user =  UserModel.find_by_username(data['username'])
		return jsonify(user.username) 

class UserSignin(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument('username',
		type=str,
		required=True,
		help="username This field cannot be blank"
		)

	parser.add_argument('password',
		type=str,
		required=True,
		help="password This field cannot be blank"
		)

	def post(self):
		data = UserSignin.parser.parse_args()
		
		user =  UserModel.find_by_username(data['username'])
		if user and  safe_str_cmp(user.password,data['password']):
			return jsonify(user.username)
		else:
			return {"message" : "user failed to sign up "},401
				

		
