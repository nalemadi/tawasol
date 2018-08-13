from flask import Flask, render_template, Response, redirect, url_for, request, session, abort
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user

app = Flask(__name__)
# flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

class User(UserMixin):
	def __init__(self, name):
		self.id = name
		self.name = str(name)
		self.password = self.name + "_secret"

	def __repr__(self):
		return "%s/%s" % (self.name, self.password)

"""
@app.route('/')
def hello_world():
	return 'Hello World!'
"""

# callback to reload the user object
@login_manager.user_loader
def load_user(userid):
	return User(userid)


@app.route("/login", methods=["GET", "POST"])
def login():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		if password == "tawasol_admin_secret" and username == "tawasol_admin":
			user = User(username)
			print user
			login_user(user)

			next = request.args.get('next')
			print next
			return redirect(next or url_for('index'))
		else:
			return abort(401)
	else:
		return render_template('login.html')

@app.route("/logout")
@login_required
def logout():
	logout_user()
	return render_template('index.html')

@app.errorhandler(401)
def page_not_found(e):
	return Response('<p>Login failed</p>')


@app.route('/')
def index():
	return render_template('index.html')

"""
if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=5009)
"""