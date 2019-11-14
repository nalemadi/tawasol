__author__ = 'noora'

from flask_login import UserMixin
#from flask_security import RoleMixin
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Users(UserMixin, db.Model):
	"""An admin user capable of viewing reports.
	:param str username: username of user
	:param str email: email address of user
	:param str password: encrypted password for the user

	"""
	__tablename__ = 'users'
	username = db.Column(db.String)
	email = db.Column(db.String, primary_key=True)
	password = db.Column(db.String)
	# roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))

	def is_active(self):
		"""True, as all users are active."""
		print 'is_active'
		return True

	def get_id(self):
		"""Return the email to satisfy Flask-Login's requirements."""
		#print 'database, userid', self.username
		return self.email

	def is_anonymous(self):
		"""False, as anonymous users aren't supported."""
		print 'is_anonymous'
		return False


class Keywords(db.Model):

	__tablename__ = 'keywords'

	keywordID = db.Column(db.INTEGER, primary_key=True)
	keywordName = db.Column(db.String)
	email = db.Column(db.String, db.ForeignKey(Users.email), nullable=False)

	#user = db.relationship('Users', lazy='joined') #foreign_keys='Users.email'

	def is_active(self):
		print 'is_active'
		return True

	def get_id(self):
		return self.keywordsID


	def is_anonymous(self):
		print 'hashtag is_anonymous'
		return False


class Accounts(db.Model):

	__tablename__ = 'accounts'

	accountID = db.Column(db.INTEGER, primary_key=True)
	accountName = db.Column(db.String)
	email = db.Column(db.String, db.ForeignKey(Users.email), nullable=False)
	userID = db.Column(db.INTEGER)

	#user = db.relationship('Users', foreign_keys='Users.username')
	#user = db.relationship('Users', lazy='joined')

	def is_active(self):
		print 'is_active'
		return True

	def get_id(self):
		return self.accountID

	def is_anonymous(self):
		return False


class Tokens(db.Model):

	__tablename__ = 'tokens'

	id = db.Column(db.INTEGER, primary_key=True)
	token = db.Column(db.String)
	email = db.Column(db.String, db.ForeignKey(Users.email), nullable=False)
	created = db.Column(db.INTEGER)
	expired = db.Column(db.INTEGER)

	def get_id(self):
		return self.id
