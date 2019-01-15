import pymongo
from pymongo import MongoClient
import logging

__author__ = 'noora'


class mongoDB_manager:

	def __init__(self, mongo_config):
		self.config = mongo_config #yaml.load(open('config/db.yml'))
		self.host = self.config['host']
		self.port = self.config['port']
		self.db_name = self.config['db_name']
		self.mongo_connection = MongoClient(self.host, self.port)
		self.connect_to_mongodb()

	def connect_to_mongodb(self):
		try:
			self.mongo_connection = MongoClient(self.host, self.port)#, connect=True)
		except pymongo.errors.ConnectionFailure, e:
			logging.warn('Problem connecting to : {} \n {}'.format(self.db_name, e))

		return self.mongo_connection

	def connect_to_collection(self, collection_name):
		try:
			#connection = MongoClient(self.host, self.port)
			records = self.mongo_connection[self.db_name][collection_name]
		except pymongo.errors.ConnectionFailure, e:
			logging.warn('Problem connecting to: {} \n {}'.format(self.config['db_name'], e))
			records = None
		return records
