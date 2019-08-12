from flask import Flask,jsonify,request
from flask_restful import Resource,Api,reqparse
from anime import print_similar_animes2
from flask_cors import CORS
from resources.user import UserRegister,UserSignin
from models.user import UserModel

#from flask_restful.utils import cors




app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = '12345'
cors = CORS(app, resources={r"*": {"origins": "*"}})
#CORS(app)
api=Api(app)


@app.before_first_request
def create_tables():
	db.create_all()

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response



class anime(Resource):
	def get(self,name):
		return jsonify(print_similar_animes2(name)) 

api.add_resource(anime,'/anime/<string:name>')	
api.add_resource(UserRegister,'/register')
api.add_resource(UserSignin,'/signin')			

#@app.route('/anime/<string:name>')   
#def print_animes(name):
#	return jsonify(print_similar_animes2(name))


     		



if __name__ == '__main__':
	from db import db
	db.init_app(app)
	app.run(port=5000,debug=True)

