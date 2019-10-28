from flask import Flask, render_template, Response, redirect, url_for, request, session, flash, jsonify, current_app
from flask_login import LoginManager, login_required, login_user, logout_user
from tawasol_api.database import Users, Keywords, Accounts, Tokens, db
from tawasol_api import pcrypt
from app import results_channels, REDIS_DB, REDIS_NAMESPACE, REDIS_CONFIG
# from tawasol_report_generator import results_channels, REDIS_DB
import json
from flask_security.decorators import roles_required
from flask_security import Security, SQLAlchemyUserDatastore
from flask_mail import Mail, Message
import uuid
import datetime
import time
from sqlalchemy import and_
import subprocess
from subprocess import PIPE


def run_shell_script_restart_crawler():
    #f = open('[REDACTED_FPATH]tawasol/cron.log', 'a')
    subprocess.call('sh [REDACTED_FPATH]tawasol/tawasol_restart_crawler_process.sh', shell=True)


def run_shell_script_restart_report():
    subprocess.call('sh [REDACTED_FPATH]tawasol/tawasol_restart_report_generator_process.sh', shell=True)


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tawasol.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "secret_key"
#app.config['SECRET_KEY'] = 'super-secret'

# Security config
#user_datastore = SQLAlchemyUserDatastore(db, Users, Role)
#security = Security(app, user_datastore)
app.config['SECURITY_RECOVERABLE'] = True
app.config['SECURITY_RESET_URL'] = '/reset'

# Mail config
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USERNAME'] = '[REDACTED_EMAIL]'
app.config['MAIL_PASSWORD'] = '[REDACTED_P]'
#app.config['DEFAULT_MAIL_SENDER'] = '[REDACTED_EMAIL]'
mail = Mail(app)

db.init_app(app)
with app.test_request_context():
    db.create_all()

# flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# alert-messages
err_USER_NOT_FOUND = 'User not found'
err_EMAIL_NOT_REGIS = 'This email is not registered'
err_PASS_NOT_MATCH = 'Those passwords did not match. Try again'
err_WRONG_PASS = 'Wrong password. Try again'
warn_NO_KEY_CHANGE = 'There are no changes in Keywords'
warn_NO_ACC_CHANGE = 'There are no changes in Accounts'
succ_KEY_CHANGED = 'Keywords are successfully updated'
succ_ACC_CHANGED = 'Accounts are successfully updated'
err_NEW_PASS_SIMILAR = 'The new password is similar to current password. Try again'
succ_CHANGE_PASS = 'Your password has been changed successfully'
err_EMAIL_EXIST = 'This email is already registered'
warn_SIMILAR_USERNAME = 'Similar username'
succ_USERNAME_CHANGED = 'Username is successfully updated'
succ_EMAIL_PASS = 'Email sent, please check your email inbox'
succ_RESET_PASS = 'Your password has been reset successfully'
err_TOKEN_NOT_EXIST = 'There is no matching token'

# alert-messages-categories
user_not_exist_cat = 'user_not_exist'
user_not_found_cat = 'user_not_found'
user_exist_cat = 'user_exist'
wrong_password_cat = 'wrong_password'
no_update_cat = 'no_update'
settings_changed_cat = 'settings_changed'
password_changed_cat = 'password_changed'
similar_user_cat = 'similar_user'
profile_changed_cat = 'profile_changed'
email_sent_cat = 'email_sent'
token_not_exist_cat = 'token_not_found'

# @security.reset_password_context_processor
# def reset_password_context_processor():


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
        is_exist = is_user_exist(email)
        if is_exist:
            flash(err_EMAIL_EXIST, user_exist_cat)
        else:
            password = request.form['password']
            repassword = request.form['repassword']
            try:
                assert password == repassword
                user = Users(
                    username=username,
                    email=email,
                    password=pcrypt.generate_password_hash(password))
                db.session.add(user)
                db.session.commit()
                login_user(user)
                # restart report generation when creating new user
                print 'account created ... restarting report generator'
                run_shell_script_restart_report()
                print 'restart is done'
                return redirect(url_for('home'))
            except AssertionError as error:
                print 'assertion error', error
                flash(err_PASS_NOT_MATCH, wrong_password_cat)
            except Exception as exception:
                print 'new user exception', exception
                flash(err_EMAIL_NOT_REGIS, user_not_exist_cat)
        return render_template('new_user.html')
    else:
        return render_template('new_user.html')


@app.route('/get_info/<user_id>', methods=['GET','POST'])
def get_info(user_id):
    if user_id:
        broken = user_id.split('@')
        user_name = broken[0].lower()
        results_channels[user_name] = '%s:%s_%s' % (REDIS_NAMESPACE, REDIS_CONFIG['channels']['results'], user_name)
        #read from redis channel
        print 'current redis channel name:', results_channels[user_name]

        data = REDIS_DB.lrange(results_channels[user_name], 0, -1)[0]
        json_data = json.loads(data)
        return jsonify(json_data)
    else:
        return None


@app.route("/home", methods=["GET", "POST"])
@login_required
def home():
    user_email = session['user_id']
    user = Users.query.get(user_email)
    current_username = user.username.title()
    return render_template('home.html', authenticated=True, current_username=current_username, user_email=user_email)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        print "login, POST"
        userEmail = request.form['email']
        password = request.form['password']
        user = Users.query.get(userEmail)
        if user:
            print 'user email found:', userEmail
            if pcrypt.check_password_hash(password, user):
                login_user(user)
                next = request.args.get('next')
                print 'next:', next
                return redirect(url_for('home'))#redirect(next or url_for("index"))
            else:
                flash(err_WRONG_PASS, wrong_password_cat)
        else:
            flash(err_USER_NOT_FOUND, user_not_found_cat)
        return render_template('index.html')
    else:
        print "login, GET"
        return render_template('index.html')


@app.route("/crawling_settings", methods=["GET", "POST"])
@login_required
def crawling_settings():
    is_changed = False
    print '=== crawling_settings ==='
    user_email = session['user_id']
    user = Users.query.get(user_email)

    # get keywords from Database for current user
    keywords = get_all_keywords(user_email)
    # get accounts from Database for current user
    accounts = get_all_accounts(user_email)

    if request.method == 'POST':
        if user:
            current_username = user.username.title()
            print 'Profile POST:', user.username
            submitted_keywords = request.form['keywords']
            submitted_accounts = request.form['accounts']
            print 'keywords:', submitted_keywords, ', accounts:', submitted_accounts

            # ==== Start Keywords Processing ==== #
            if submitted_keywords:
                print 'submitted_keywords is not None', submitted_keywords
                keywords_broken = [k.strip().lower() for k in submitted_keywords.split(',') if len(k.strip()) > 1]
                if keywords_broken:
                    is_changed = True
                    if keywords:
                        keywords_from_db = keywords.strip().split(',')
                        print 'keywords_from_db:', keywords_from_db, 'keywords_broken', keywords_broken

                        new_keywords = list(set(keywords_broken) - set(keywords_from_db))
                        removed_keywords = list(set(keywords_from_db) - set(keywords_broken))

                        if not new_keywords and not removed_keywords:
                            flash(warn_NO_KEY_CHANGE, no_update_cat)
                        else:
                            # add new keywords
                            insert_into_keywords(new_keywords, user.email)

                            # remove deleted keywords
                            remove_keyword_from_db(removed_keywords)
                            ####
                            flash(succ_KEY_CHANGED, settings_changed_cat)
                    else:
                        # first time to add keywords
                        print 'keywords is None in DB, adding new keywords'
                        insert_into_keywords(keywords_broken, user.email)
                        flash(succ_KEY_CHANGED, settings_changed_cat)
                else:
                    print 'broken keywords is empty'
                    flash(warn_NO_KEY_CHANGE, no_update_cat)

            else:
                print 'empty submitted keywords'
                if keywords:
                    is_changed = True
                    delete_all_records_from_keywords(user_email)
                    flash(succ_KEY_CHANGED, settings_changed_cat)
                else:
                    flash(warn_NO_KEY_CHANGE, no_update_cat)
            # ==== END Keywords Processing ==== #

            # ==== Start Accounts Processing ==== #
            if submitted_accounts:
                print 'submitted_accounts is not None', submitted_accounts
                #accounts_broken = submitted_accounts.split(',')
                accounts_broken = [k.strip().lower() for k in submitted_accounts.split(',') if len(k.strip()) > 1]
                if accounts_broken:
                    is_changed = True
                    if accounts:
                        accounts_from_db = accounts.strip().split(',')
                        print 'accounts_from_db:', accounts_from_db, 'accounts_broken', accounts_broken

                        new_accounts = list(set(accounts_broken) - set(accounts_from_db))
                        removed_accounts = list(set(accounts_from_db) - set(accounts_broken))

                        if not new_accounts and not removed_accounts:
                            flash(warn_NO_ACC_CHANGE, no_update_cat)
                        else:
                            # add new accounts
                            insert_into_accounts(new_accounts, user.email)

                            # remove deleted accounts
                            remove_account_from_db(removed_accounts)
                            ####
                            flash(succ_ACC_CHANGED, settings_changed_cat)
                    else:
                        # first time to add keywords
                        print 'accounts is None in DB, adding new accounts'
                        insert_into_accounts(accounts_broken, user.email)
                        flash(succ_ACC_CHANGED, settings_changed_cat)
            else:
                print 'empty submitted accounts'
                if accounts:
                    is_changed = True
                    delete_all_records_from_accounts(user.email)
                    flash(succ_ACC_CHANGED, settings_changed_cat)
                else:
                    flash(warn_NO_ACC_CHANGE, no_update_cat)
            # ==== END Accounts Processing ==== #

            #get updated keywords and accounts from DB
            keywords = get_all_keywords(user_email)
            accounts = get_all_accounts(user_email)

            if is_changed:
                # restarting the crawler and report generator if there is any change
                print 'There are changes in Keywords/Accounts ... restarting the crawler and report generator'
                run_shell_script_restart_crawler()
                run_shell_script_restart_report()
                print 'restart is done'

            return render_template('crawling_settings.html', authenticated=True, current_username=current_username, user_keywords=keywords, user_accounts=accounts)
        else:
            flash(err_USER_NOT_FOUND, user_not_found_cat)
            return render_template('index.html')
    else:
        print 'crawling_settings GET', 'current user', user_email
        current_username = user.username.title()
        return render_template('crawling_settings.html', authenticated=True, current_username=current_username, user_keywords=keywords, user_accounts=accounts)


def get_all_keywords(user_email):
    print 'get_all_keywords'
    existing_keywords = db.session.query(Keywords).filter(Keywords.email == user_email)
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


def insert_into_keywords(array, user_email):
    for n_keyword in array:
        if n_keyword:
            exists = db.session.query(Keywords.keywordID).filter_by(keywordName=n_keyword).filter_by(email=user_email).scalar()
            print 'keyword', n_keyword, 'exists:', exists
            if not exists:
                keyword_insert = Keywords(
                    keywordName=n_keyword,
                    email=user_email)
                db.session.add(keyword_insert)
                db.session.commit()
                print 'keyword:', n_keyword, 'is added!'


def insert_into_accounts(array, user_email):
    for account in array:
        if account:
            exists = db.session.query(Accounts.accountID).filter_by(accountName=account).filter_by(email=user_email).scalar()
            print 'account', account, 'exists:', exists
            if not exists:
                f_account = Accounts(
                    accountName=account,
                    email=user_email)
                db.session.add(f_account)
                db.session.commit()
                print 'account', account, 'is added!'


def remove_keyword_from_db(removed_keywords):
    for removed_keyword in removed_keywords:
        db.session.query(Keywords.keywordID).filter_by(keywordName=removed_keyword).delete()
        db.session.commit()
        print 'keyword:', removed_keyword, 'is removed!'


def remove_account_from_db(removed_accounts):
    for removed_account in removed_accounts:
        db.session.query(Accounts.accountID).filter_by(accountName=removed_account).delete()
        db.session.commit()


def delete_all_records_from_accounts(email):
    print '=== delete_all_records_from_accounts === for:', email
    #db.session.query(table).delete()
    db.session.query(Accounts.accountID).filter_by(email=email).delete()
    db.session.commit()


def delete_all_records_from_keywords(email):
    print '=== delete_all_records_from_keywords === for:', email
    #db.session.query(table).delete()
    print db.session.query(Keywords.keywordID).filter_by(email=email)
    db.session.query(Keywords.keywordID).filter_by(email=email).delete()
    db.session.commit()


def is_user_exist(email):
    print '=== is_user_exist ==='
    is_exist = db.session.query(db.exists().where(Users.email == email)).scalar()
    return is_exist


def update_password(email, new_password):
    add_password = pcrypt.generate_password_hash(new_password)
    Users.query.filter_by(email=email).update(dict(password=add_password))
    db.session.commit()


def update_username(email, username):
    Users.query.filter_by(email=email).update(dict(username=username))
    db.session.commit()


def insert_into_tokens(code, email):
    created_at = datetime.datetime.now()
    expired_at = created_at + datetime.timedelta(minutes=10)
    create_epoch = int(time.mktime(created_at.timetuple()) + created_at.microsecond / 1E6)
    expire_epoch = int(time.mktime(expired_at.timetuple()) + expired_at.microsecond / 1E6)

    token = Tokens(
        token=code,
        email=email,
        created=create_epoch,
        expired=expire_epoch)
    db.session.add(token)
    db.session.commit()


def check_token(token, email):
    is_exist = db.session.query(db.exists().where(and_(Tokens.token == token, Tokens.email == email))).scalar()
    return is_exist


def is_token_valid(token, email):
    #result = db.session.query(db.exists().where(and_(Tokens.token == token, Tokens.email == email))).scalar() #.filter(Tokens.email == email, Tokens.token == token)
    result = db.session.query(Tokens).filter(Tokens.email == email, Tokens.token == token)
    existing_token = [token_.expired for token_ in result]
    exp_time_epoch = existing_token[0]
    e_date = datetime.datetime.fromtimestamp(int(exp_time_epoch))
    now_date = datetime.datetime.now()
    if e_date > now_date:
        return True
    else:
        return False


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    print '=== Profile ==='
    user_email = session['user_id']
    user = Users.query.get(user_email)
    if user:
        current_username = user.username.title()
        if request.method == 'POST':
            print 'profile user', user
            if 'password' in request.form.keys():
                password = request.form['password']
                if pcrypt.check_password_hash(password, user):
                    new_password = request.form['new_password']
                    renew_password = request.form['renew_password']
                    try:
                        assert new_password == renew_password
                        #check if current and new password are similar
                        if password == new_password:
                            flash(err_NEW_PASS_SIMILAR, wrong_password_cat)
                        else:
                            # generate new encrypted password
                            update_password(user_email, new_password)
                            flash(succ_CHANGE_PASS, password_changed_cat)
                    except AssertionError as error:
                        print error
                        flash(err_PASS_NOT_MATCH, wrong_password_cat)
                    except Exception as exception:
                        print exception
                        flash(err_PASS_NOT_MATCH, wrong_password_cat)
                else:
                    flash(err_WRONG_PASS, wrong_password_cat)
                #return render_template('profile.html', authenticated=True, current_user=user, current_username=current_username)
            ###
            elif 'username' in request.form.keys():
                username = request.form['username']
                if username:
                    if username == user.username:
                        flash(warn_SIMILAR_USERNAME, similar_user_cat)
                    else:
                        update_username(user_email, username)
                        flash(succ_USERNAME_CHANGED, profile_changed_cat)
                else:
                    flash(warn_SIMILAR_USERNAME, similar_user_cat)
            return render_template('profile.html', authenticated=True, current_user=user, current_username=current_username)
        else:
            print 'GET'
            return render_template('profile.html', authenticated=True, current_user=user, current_username=current_username)

    return render_template('index.html')


@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    # check app password from gmail
    print '=== forgot_password ==='
    if request.method == 'POST':
        email = request.form['email']
        exist = is_user_exist(email)
        if exist:
            code = str(uuid.uuid4())
            insert_into_tokens(code, email)
            # email user
            #body_html = render_template('reset_password.html', user_email=email)
            body_text = render_template('password_reset.txt', user_email=email, code=code)
            msg = Message('TAWASOL - Reset Password Request', sender=app.config['MAIL_USERNAME'], recipients=[email])
            msg.body = body_text
            mail.send(msg)
            flash(succ_EMAIL_PASS, email_sent_cat)
            #mail(email, "Password reset request", body_html, 'test')
        else:
            flash(err_EMAIL_NOT_REGIS, user_not_exist_cat)
    return render_template('forgot_password.html')


@app.route('/reset_password/<email>/<token>', methods=['GET', 'POST'])
def reset_password(email, token):
    print '==== reset password ===='
    print email, token
    exist = is_user_exist(email)
    if exist:
        if request.method == 'POST':
            print 'reset pass == post'
            password = request.form['new_password']
            re_password = request.form['renew_password']
            try:
                assert password == re_password
                ###
                update_password(email, password)
                flash(succ_RESET_PASS, password_changed_cat)
            except AssertionError as error:
                print 'assertion error', error
                flash(err_PASS_NOT_MATCH, wrong_password_cat)
            return render_template('reset_password.html')
        else:
            print 'user exists == GET'
            is_token_exist = check_token(token, email)
            if is_token_exist:
                is_valid = is_token_valid(token, email)
                if is_valid:
                    return render_template('reset_password.html')
                else:
                    return render_template('expired_token.html')
            else:
                print 'token not exist'
                flash(err_TOKEN_NOT_EXIST, token_not_exist_cat)
                return render_template('reset_password.html')
    else:
        print 'user NOT exists'
        flash(err_EMAIL_NOT_REGIS, user_not_exist_cat)
        return render_template('index.html')


@app.route('/logout')
@login_required
def logout():
    print '=== logout ==='
    logout_user()
    return redirect(url_for('index'))


@app.route('/contact')
def contact():
    if 'user_id' in session.keys():
        user_email = session['user_id']
        user = Users.query.get(user_email)
        current_username = user.username.title()
        return render_template('contact.html', authenticated=True, current_user=user, current_username=current_username)
    else:
        return render_template('contact.html')


@app.route('/about')
def about():
    if 'user_id' in session.keys():
        user_email = session['user_id']
        user = Users.query.get(user_email)
        current_username = user.username.title()
        return render_template('about.html', authenticated=True, current_user=user, current_username=current_username)
    else:
        return render_template('about.html')


@app.errorhandler(401)
def page_not_found(e):
    return Response('<p>Login failed</p>')


@app.route('/')
def index():
    print '== index =='
    return render_template('index.html')

# TODO future feature
# @admin.route('/admin')
# @roles_required('admin')
# def index():
#     return render_template('admin_index.htm')
#
#
# @admin.route('/author/create', methods=['GET', 'POST'])
# @roles_required('admin')
# def create_author():
# 	return None
