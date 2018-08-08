__author__ = 'Noora'
from flask import Flask
from flask_restful import Api
import os

app = Flask(__name__)
api = Api(app)

#api.add_resource(, '/api/v1/tawasol', endpoint="")

if __name__ == '__main__':

	app.run(debug=True, host='0.0.0.0', port=5009)
