__author__ = 'noora'

from flask_restful import Resource, abort, reqparse
from common.database import db
from common.models import User


class GenerateKey(Resource):
	def get(self):
		parser = reqparse.RequestParser()
		parser.add_argument('name', type=str)
		parser.add_argument('adminpwd', required=True, type=str, help='required admin password to create new API keys.')
		args = parser.parse_args()
		adminpwd = args['adminpwd']
		if adminpwd != 'qcriqarta':
			abort(400, message="Wrong admin password. Contact Noora Alemadi: nalemadi@hbku.edu.qa")
		name = args['name']
		if name is None:
			abort(400, message="missing argument")
		elif User.query.filter_by(name=name).first() is not None:
			return {'name': name,
			        'key': User.query.filter_by(name=name).first().key,
			        'message': 'Existing user. Returned her existing key'}, 201
		user = User(name=name)
		user.generate_key()
		db.session.add(user)
		db.session.commit()
		return {'name': user.name,
		        'key': user.key,
		        'message': 'Successfully added new user.'}, 201

	def post(self):
		parser = reqparse.RequestParser()
		parser.add_argument('name', type=str)
		parser.add_argument('adminpwd', required=True, type=str, help='admin passwd to create new API keys.')
		args = parser.parse_args()
		adminpwd = args['adminpwd']
		if adminpwd != 'qcriqarta':
			abort(400, message="Wrong admin password. Contact Noora Alemadi: nalemadi@hbku.edu.qa")
		name = args['name']
		if name is None:
			abort(400, message="missing argument")
		elif User.query.filter_by(name=name).first() is not None:
			return {'name': name,
			        'key': User.query.filter_by(name=name).first().key,
			        'message': 'Existing user. Returned her existing key'}, 201
		user = User(name=name)
		user.generate_key()
		db.session.add(user)
		db.session.commit()
		return {'name': user.name,
		        'key': user.key,
		        'message': 'Successfully added new user.'}, 201