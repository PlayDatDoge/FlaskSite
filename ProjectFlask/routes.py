from flask import redirect, url_for, render_template, request,session  
from .models import db, User,login_manager
import flask_login
from flask_login import login_user, login_required, logout_user , current_user
from flask import current_app as app

@app.route('/index')
@app.route('/')
@login_required
def index():
	if not flask_login.current_user.is_authenticated:
		if 'user' in session:
			if logged_user := User.query.filter_by(username=session['user']).first():
				login_user(logged_user)
		else:
			return redirect(url_for('login'))
	if flask_login.current_user.is_authenticated:
		return render_template('index.html')

@app.route('/logout')
@login_required
def logout():
	if 'user' in session:
		session['user'] = ''
	logout_user()
	return redirect(url_for('login'))	
								

@app.route('/login', methods=['POST', 'GET'])
def login():
	if request.method == 'POST':
		username12 = request.form['username']
		password = request.form['password']
		if logged_user := User.query.filter_by(username=username12).first():
			if password == logged_user._hashedpassword:
				session['user'] = logged_user.username
				login_user(logged_user)
				print(current_user)
				return redirect(url_for('index'))

	return render_template('login.html')



@app.route('/register', methods=['POST', 'GET'])
def register():
	if request.method == "POST":
		username = request.form['username']
		password = request.form['password']
		email = request.form["email"]
		if not  User.query.filter_by(username=username).first():
			db.session.add(User(username=username, _hashedpassword=password, email=email))
			db.session.commit()
			return redirect(url_for('login'))
	return render_template('register.html')

@login_required
@app.route('/myteam',methods=['POST', 'GET'])
def myteam():
	return render_template('myteam.html')

@login_required
@app.route('/player',methods=['POST', 'GET'])
def player():
	return render_template('player.html')
	
# fix the error handler

@login_manager.unauthorized_handler
def unauthorized():
	# if not 'user' in session:
	return redirect(url_for('login'))


@app.errorhandler(404)
def error_handler(error):
	print(error)
	return render_template("404.html")

