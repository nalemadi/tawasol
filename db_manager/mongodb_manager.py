from pymongo import MongoClient, errors
import logging

__author__ = 'noora'


class MongodbManager:

	def __init__(self, mongo_config):
		self.config = mongo_config
		self.host = self.config['host']
		self.port = self.config['port']
		self.db_name = self.config['db_name']
		self.mongo_connection = MongoClient(self.host, self.port)
		self.connect_to_mongodb()

	def connect_to_mongodb(self):
		try:
			self.mongo_connection = MongoClient(self.host, self.port)#, connect=True)
		except errors.ConnectionFailure as e:
			logging.warn('Problem connecting to : {} \n {}'.format(self.db_name, e))

		return self.mongo_connection

	def connect_to_collection(self, collection_name):
		try:
			records = self.mongo_connection[self.db_name][collection_name]
		except errors.ConnectionFailure as e:
			logging.warn('Problem connecting to: {} \n {}'.format(self.config['db_name'], e))
			records = None
		return records
