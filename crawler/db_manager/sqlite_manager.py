from sqlite3 import connect, Error
import logging


class SqliteManager:

	def __init__(self, db_name):
		self.database_file = db_name
		self.connection = self.create_connection()
		self.users = self.select_all_users()
		self.tawasol_users = self.get_keywords_accounts_for_users()

	def create_connection(self):
		""" create a database connection to the SQLite database
		:param
		:return: Connection object or None
		"""
		try:
			connection = connect(self.database_file)
			return connection
		except Error as e:
			logging.warn('Problem in sqlite: %s' % e)
			return None

	def select_all_users(self):
		"""
		Get all Tawasol users in the users table
		:param:
		:return: users list
		"""
		users = []
		cursor = self.connection.cursor()
		try:
			cursor.execute('SELECT * FROM users')
			rows = cursor.fetchall()
			users = [row[0] for row in rows]
			print users
			return users
		except Error as e:
			logging.warn('Problem in users - sqlite: %s' % e)
			return None

	def get_keywords_accounts_for_users(self):
		"""
		Get keywords and accounts for all users in Tawasol
		:param
		:return: tawasol users dictionary with hashtags and accounts
		"""
		tawasol_dict = dict()
		cursor = self.connection.cursor()
		for user in self.users:
			print 'user in users', user
			cursor.execute('SELECT * FROM keywords WHERE email=?', (user,))
			hashtags_rows = cursor.fetchall()
			print 'hashtag rows', hashtags_rows
			hashtags = [row[1] for row in hashtags_rows]
			##
			cursor.execute('SELECT * FROM accounts WHERE email=?', (user,))
			accounts_rows = cursor.fetchall()
			accounts = [row[1] for row in accounts_rows]
			user_dict = dict()
			user_dict['keywords'] = hashtags
			user_dict['accounts'] = accounts
			tawasol_dict[user] = user_dict
		return tawasol_dict

	def get_userScreenID_from_account(self, account_name):
		"""
		NOT used
		:param account_name: screen_name of twitter user
		:return:
		"""
		cursor = self.connection.cursor()
		cursor.execute('SELECT userID FROM accounts WHERE accountName=?', (account_name,))
		ids = cursor.fetchall()
		user_screen_id = None
		for id in ids:
			for iid in id:
				if iid is not None:
					user_screen_id = iid
		return user_screen_id

	def insert_userID_into_accounts(self, user_id, account):
		"""
		NOT used
		:param user_id:
		:param account:
		:return:
		"""
		cursor = self.connection.cursor()
		cursor.execute('UPDATE accounts SET userID=? WHERE accountName=?', (user_id, account,))
