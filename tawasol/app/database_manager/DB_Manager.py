import pymongo
from pymongo import MongoClient
import logging
import yaml

__author__ = 'noora'


class DBManager:

	def __init__(self):
		self.config = yaml.load(open('config/db.yml'))
		self.host = self.config['host']
		self.port = self.config['port']
		self.db_name = self.config['db_name']
		self.connection =  MongoClient(self.host, self.port)
		self.connect_to_db()

	def connect_to_db(self):
		try:
			self.connection = MongoClient(self.host, self.port, connect=False)
		except pymongo.errors.ConnectionFailure, e:
			logging.warn('Problem connecting to : {} \n {}'.format(self.db_name, e))

		return self.connection

	def connect_to_collection(self, collection_name):
		try:
			connection = MongoClient(self.host, self.port)
			records = connection[self.config['db_name']]['collections'][collection_name]
		except pymongo.errors.ConnectionFailure, e:
			logging.warn('Problem connecting to: {} \n {}'.format(self.config['db_name'], e))
			records = None
		return records
