__author__ = 'Noora'
from flask import Flask
from flask_restful import Api
from resources import GenerateKey
from common.database import db
import os

app = Flask(__name__)
api = Api(app)

#api.add_resource(, '/api/v1/tawasol', endpoint="")
api.add_resource(GenerateKey, '/api/v1/access/generate_key', endpoint="keys")

if __name__ == '__main__':
	# TODO: sqlite for login info, check best practices
	if not os.path.exists('tawasol.sqlite'):
		db.create_all()

	app.run(debug=True, host='0.0.0.0', port=5009)
