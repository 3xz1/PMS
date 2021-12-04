from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime, timedelta
from dateutil.relativedelta import *
from simplecrypt import encrypt, decrypt
from base64 import b64encode, b64decode

# local imports
from .models import Users, Services
from . import db
from .password_check import check_password_criteria, check_hibp, return_password_criteria



auth = Blueprint('auth', __name__)


@auth.route('/change_password')
def change_password():
	return render_template('change_password.html')

@auth.route('/change_password', methods=['POST'])
def change_password_post():
	try:
		username = request.form.get('username')
		password = request.form.get('password')
		new_password = request.form.get('new_password')
		new_password_check = request.form.get('new_password_check')
	except:
		flash('Please check your input.')
		return redirect(url_for('auth.login'))

	if(new_password != new_password_check):
		flash("New passwords doesn't match")
		return redirect(url_for('auth.change_password'))
	try:
		user = Users.query.filter_by(username=username).first()
		if user:
			check_pw = user.verify_password(password=password)
			if check_pw:
				if(check_password_criteria(new_password) == False):
					flash(return_password_criteria(), 'error')
					return redirect(url_for('auth.change_password'))
				elif(check_hibp(password) == True):
					flash("Password was already found in a breach please create a secure passowrd", 'error')
					return redirect(url_for('auth.change_password'))
				else:
					user = Users.query.filter_by(username=username).first()
					user.password = new_password
					db.session.commit()
					flash('Password changes successfuly')
					return redirect(url_for('auth.login'))
			else:
				flash("Wrong Password")
				return redirect(url_for('auth.change_password'))
		else:
			flash("User doesn't exists")
			return redirect(url_for('auth.change_password'))
	except:
		flash('Servie not reachable. Try again later.')
		return redirect(url_for('auth.login'))

	flash("User doesn't exsists")
	return redirect(url_for('auth.change_password'))


@auth.route('/get_services')
@login_required
def get_services():
	return render_template('services.html')

@auth.route('/get_services', methods=['POST'])
@login_required
def get_services_post():
	try:
		master_password = request.form.get('master_password')
	except:
		flash('Please check your input')
		return redirect(url_for('auth.get_services'))
	try:
		username = current_user.username
		user = Users.query.filter_by(username=current_user.username).first()
		services =  Services.query.filter_by(user_id=user.id).all()
	except:
		flash('Service is not available, please try again later.')
	try:
		for service in services:
			service.encrypted_pw = decrypt(master_password, b64decode(service.encrypted_pw)).decode('utf-8')
	except:
		flash('Wrong Masterpassword.')
		return redirect(url_for('auth.get_services'))
	return render_template('services_post.html', services=services)

@auth.route('/new_service')
@login_required
def new_service():
	return render_template('new_service.html')

@auth.route('/new_service', methods=['POST'])
@login_required
def new_service_post():
	try:
		username = current_user.username
		service_name = request.form.get('service_name')
		service_username = request.form.get('username')
		password = request.form.get('password')
		password_check = request.form.get('password_check')
		service_password = request.form.get('service_password')
	except:
		flash('Check your Input.')
		return redirect(url_for('auth.new_service'))
	#try:
	if(password != password_check):
		flash("Passwords doesn't match")
		return redirect(url_for('auth.new_service'))

	try:
		user = Users.query.filter_by(username=current_user.username).first()
		encrypted_password = b64encode(encrypt(password, service_password)).decode('utf-8')
		new_service = Services(user_id=user.id, service_name=service_name, encrypted_pw=encrypted_password, username=service_username)
		db.session.add(new_service)
		db.session.commit()
		flash('Service Password was successfully added.')
		return redirect(url_for('auth.get_services'))
	except:
		flash('Service not available. Try again later')
		return redirect(url_for('main.profile'))
	
@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
	try:
		username = request.form.get('username')
		password = request.form.get('password')
		remember = True if request.form.get('remember') else False
		date_today = datetime.now()
		user = Users.query.filter_by(username=username).first()
			
	except:
		flash('Please check your Input.')
		return redirect(url_for('auth.login'))
	
	if user:
		check_pw = user.verify_password(password=password)
		if check_pw:
			if(check_password_criteria(password) == False):
				flash("Password doesn't match the Password criteria anymore. You are required to change your Password before you can login again.", 'error')
				return redirect(url_for('auth.change_password'))
			elif(user.get_expire_date() < date_today):
				flash("Password has expired. You are required to change your Password before you can login again.")
				return redirect(url_for('auth.change_password'))
			else:
				login_user(user, remember=remember)
				return redirect(url_for('main.profile'))
		else:
			flash('Wrong password')
			return redirect(url_for('auth.login'))
	else:
		flash("Username doesn't exists create Account")
		return redirect(url_for('auth.signup'))

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup',methods=['POST'])
def signup_post():
	try:
		username = request.form.get('username')
		password = request.form.get('password')
		password_check = request.form.get('password_check')
		pw_expire_date = datetime.now() + relativedelta(months=+3)
	except:
		flash('Check your Input.')
		return redirect(url_for('auth.login'))
	try:
		if(password != password_check):
			flash("Passwords doesn't match")
			return redirect(url_for('auth.signup'))
		user = Users.query.filter_by(username=username).first()
		if user:
			flash('Username already exists')
			return redirect(url_for('auth.login'))
		elif(check_password_criteria(password) == False):
			flash(return_password_criteria(), 'error')
			return redirect(url_for('auth.signup'))
		elif(check_hibp(password) == True):
			flash("Password was already found in a breach please create a secure passowrd", 'error')
			return redirect(url_for('auth.signup'))
		else:
			new_user = Users(username=username,password=password, pw_expire_date=pw_expire_date)
			db.session.add(new_user)
			db.session.commit()
			flash('Account creation successful')
			return redirect(url_for('auth.login'))
	except:
		flash('Servie not reachable. Try again later.')
		return redirect(url_for('auth.signup'))

@auth.route('/logout')
@login_required
def logout():
	"""
	Handle requests to the /logout route
	Log an user out through the logout link
	"""
	logout_user()
	flash('You have successfuly been logged out.')
	return redirect(url_for('auth.login'))
