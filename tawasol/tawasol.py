from flask import Flask, render_template, Response, redirect, url_for, request, session, abort
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user
from database import Users, Keywords, Accounts, db
import pcrypt

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tawasol.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "secret_key"

db.init_app(app)
with app.test_request_context():
	db.create_all()

# flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

"""
class Users(UserMixin):
	def __init__(self, name):
		self.id = name
		self.name = str(name)
		self.password = self.name + "_secret"

	def __repr__(self):
		return "%s/%s" % (self.name, self.password)
"""
"""
@app.route('/')
def hello_world():
	return 'Hello World!'
"""

# callback to reload the user object
@login_manager.user_loader
def load_user(user_id):
	print 'load_user - userid:', user_id
	#return Users(userid)
	return Users.query.get(user_id)


@app.route('/new_user', methods=["GET", "POST"])
def new_user():
	if request.method == 'POST':

		username = request.form['username']
		email = request.form['email']
		password = request.form['password']
		repassword = request.form['repassword']

		try:
			assert password == repassword
		except AssertionError as error:
			print error
			return render_template('new_user.html')
		except Exception as exception:
			print exception
			return render_template('new_user.html')
		user = Users(
			username=username,
			email=email,
			password=pcrypt.generate_password_hash(password))
		db.session.add(user)
		db.session.commit()
	return render_template('new_user.html')


@app.route("/login", methods=["GET", "POST"])
def login():
	if request.method == 'POST':
		print "login, POST"
		userEmail = request.form['email']
		password = request.form['password']
		user = Users.query.get(userEmail)
		if user:
			print 'user email found:', userEmail
			if pcrypt.check_password_hash(password):
				login_user(user)
				next = request.args.get('next')
				print 'next:', next
				return redirect(url_for('profile'))#redirect(next or url_for("index"))
			else:
				return Response('<p>Password Wrong</p>')
		else:
			return Response('<p>user not found</p>')
			print 'user not found'
	else:
		print "login, GET"
		return render_template('login.html')


@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
	#
	print '=== profile ==='
	#user_test = session['curr_user']
	#print user_test
	#
	user_email = session['user_id']
	user = Users.query.get(user_email)

	# get keywords from Database for current user
	keywords = get_all_keywords(user_email)
	# get accounts from Database for current user
	accounts = get_all_accounts(user_email)

	#data = session.query(Keywords).options(db.joinedload(Keywords.user, innerjoin=True))
	#keywords = session.query(Keywords).filter(Users.username == username).all()
	#data = db.session.query(Users, Keywords).join(Users).all()

	if request.method == 'POST':
		if user:
			print 'Profile POST:', user.username
			submitted_keywords = request.form['keywords']
			submitted_accounts = request.form['accounts']
			print 'keywords:', submitted_keywords, ', accounts:', submitted_accounts

			if submitted_keywords:
				print 'submitted_keywords is not None', submitted_keywords
				keywords_broken = [k.strip().lower() for k in submitted_keywords.split(',') if len(k.strip()) > 1]
			else:
				print 'empty submitted keywords'
				keywords_broken = None
			if submitted_accounts:
				print 'submitted_accounts is not None', submitted_accounts
				accounts_broken = submitted_accounts.split(',')
			else:
				print 'empty submitted accounts'
				accounts_broken = None

			if keywords_broken:
				if keywords:
					print 'previous keywords is not None'
					keywords_from_DB = keywords.strip().split(',')
					print 'keywords_from_DB:', keywords_from_DB, 'keywords_broken', keywords_broken

					new_keywords = list(set(keywords_broken) - set(keywords_from_DB))
					removed_keywords = list(set(keywords_from_DB) - set(keywords_broken))

					# add new keywords
					# TODO: Noora: Check that you are not adding the same keyword twice.
					for new_keyword in new_keywords:
						n_keyword = Keywords(
							keywordName=new_keyword,
							email=user.email)
						db.session.add(n_keyword)
						db.session.commit()
						print 'keyword:', new_keyword, 'is added!'

					# remove deleted keywords
					for removed_keyword in removed_keywords:
						db.session.query(Accounts.accountID).filter_by(accountName=removed_keyword).delete()
						db.session.commit()
						print 'keyword:', removed_keyword, 'is removed!'
				else:
					# first time to add keywords
					print 'keywords is None'
					for n_keyword in keywords_broken:
						print ' ==== first time======', n_keyword
						if n_keyword:
							exists = db.session.query(Keywords.keywordID).filter_by(keywordName=n_keyword).scalar()
							print 'keyword', n_keyword, 'exists:', exists
							if not exists:
								keyword_insert = Keywords(
									keywordName=n_keyword,
									email=user.email)
								db.session.add(keyword_insert)
								db.session.commit()
								print 'keyword:', n_keyword, 'is added!'
			else:
				# delete all keywords
				print 'delete all keywords'
				db.session.query(Keywords).delete()
				db.session.commit()

			if accounts_broken:
				if accounts:
					print 'previous accounts is not None'
					accounts_from_DB = accounts.strip().split(',')
					print 'accounts-from DB:', accounts_from_DB, 'accounts_broken', accounts_broken

					new_accounts = list(set(accounts_broken) - set(accounts_from_DB))
					removed_accounts = list(set(accounts_from_DB) - set(accounts_broken))

					# add new accounts
					for new_account in new_accounts:
						f_account = Accounts(
							accountName=new_account,
							email=user.email)
						db.session.add(f_account)
						db.session.commit()
						print 'account:', new_account, 'is added!'

					# remove deleted accounts
					for removed_account in removed_accounts:
						db.session.query(Accounts.accountID).filter_by(accountName=removed_account).delete()
						db.session.commit()

				else:
					# first time to add accounts
					print 'account is None'
					for account in accounts_broken:
						if account:
							exists = db.session.query(Accounts.accountID).filter_by(accountName=account).scalar()
							print 'account', account, 'exists:', exists
							if not exists:
								f_account = Accounts(
									accountName=account,
									email=user.email)
								db.session.add(f_account)
								db.session.commit()
								print 'account', account, 'is added!'
			else:
				# delete all accounts
				print 'delete all accounts'
				db.session.query(Accounts).delete()
				db.session.commit()

			#get updated keywords and accounts from DB
			keywords = get_all_keywords(user_email)
			accounts = get_all_accounts(user_email)
			#return render_template('profile.html', username=user.username, user_keywords=keywords, user_accounts=accounts)
			return render_template('profile.html', authenticated=True, current_username=user.username, user_keywords=keywords, user_accounts=accounts)
		else:
			print 'user not found'
	else:
		#Accounts.query.delete() #debuging
		#Keywords.query.delete() #debuging
		#db.session.commit() #debuging
		print 'Profile GET'
		print 'current user', user_email

		#return render_template('profile.html', username=user.username, user_keywords=keywords, user_accounts=accounts)
		return render_template('profile.html', authenticated=True, current_username=user.username, user_keywords=keywords, user_accounts=accounts)


def get_all_keywords(user_email):
	print 'get_all_keywords'
	existing_keywords = db.session.query(Keywords).filter(Keywords.email == user_email)
	# for hash in existing_keywords:
	#	print hash.keywordName, ',', hash.email
	all_keywords = [keyword_.keywordName for keyword_ in existing_keywords]
	if len(all_keywords) > 1:
		keywords = ','.join(all_keywords)
	elif len(all_keywords) == 1:
		keywords = all_keywords[0]
	else:
		keywords = None
	return keywords


def get_all_accounts(user_email):
	print 'get_all_accounts'
	existing_accounts = db.session.query(Accounts).filter(Accounts.email == user_email)
	all_accounts = [account_.accountName for account_ in existing_accounts]
	if len(all_accounts) > 1:
		accounts = ','.join(all_accounts)
	elif len(all_accounts) == 1:
		accounts = all_accounts[0]
	else:
		accounts = None
	return accounts


@app.route("/logout")
@login_required
def logout():
	print '=== logout ==='
	logout_user()
	return render_template('login.html')


@app.route('/contact')
def contact():
	return render_template('contact.html')


@app.errorhandler(401)
def page_not_found(e):
	return Response('<p>Login failed</p>')


@app.route('/')
def index():
	print '== index =='
	return render_template('index.html')

"""
if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=5009)
"""