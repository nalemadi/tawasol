#!/usr/bin/python

import sqlite3
from sqlite3 import Error


class SqliteManager:

	def __init__(self):
		self.database_file = '/Users/noora/PyCharm-Projects/tawasol/tawasol/tawasol.sqlite'
		self.connection = self.create_connection()
		self.users = self.select_all_users()

	def create_connection(self):
		""" create a database connection to the SQLite database
		:param
		:return: Connection object or None
		"""
		try:
			connection = sqlite3.connect(self.database_file)
			return connection
		except Error as e:
			print 'error', e
		return None

	def select_all_users(self):
		"""
		Query all rows in the users table
		:param:
		:return: users list
		"""
		cursor = self.connection.cursor()
		#cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
		#print cursor.fetchall()
		cursor.execute('SELECT * FROM users')

		rows = cursor.fetchall()

		users = [row[1] for row in rows]
		#print self.users
		return users


	def get_hashtags_accounts_for_user(self):
		"""
		:param users_arr:
		:return:
		"""
		tawasol_dict = {}
		cursor = self.connection.cursor()
		for user in self.users:
			#print user,
			cursor.execute('SELECT * FROM hashtags WHERE email=?', (user,))
			hashtags_rows = cursor.fetchall()
			hashtags = [row[1] for row in hashtags_rows]
			#print hashtags,

			##
			cursor.execute('SELECT * FROM accounts WHERE email=?', (user,))
			accounts_rows = cursor.fetchall()
			accounts = [row[1] for row in accounts_rows]
			#print accounts
			user_dict = {}
			user_dict['hashtags'] = hashtags
			user_dict['accounts'] = accounts
			tawasol_dict[user] = user_dict
		#print tawasol_dict
		return tawasol_dict

"""
if __name__ == '__main__':

	db = SqliteManager()

	# create a database connection
	conn = db.create_connection()
	with conn:
		print '1. Query all users'
		users = db.select_all_users()
		##
		print '2. Query hashtags and accounts for user:'
		db.get_hashtags_accounts_for_user()
"""