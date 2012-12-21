from flask import Blueprint, request, render_template, g, url_for, flash, redirect
from alcoholicism import db, loginmanager, mail
from alcoholicism.models.user import User, Role
from alcoholicism.forms.login import LoginForm, RegisterForm
from flask.ext.login import login_required, login_user, logout_user, current_user
from flask.ext.mail import Message
from datetime import datetime

blueprint = Blueprint('login', __name__, template_folder='templates')

@blueprint.route("/login", methods=["GET", "POST"])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user:
			if user.checkPassword(form.password.data):
				remember = form.remember
				if not user.is_active():
					flash("Your account is currently %s" % user.status)
					return render_template('login/login.html', form = form)
				if login_user(user, remember = remember):
					user.last_login = datetime.utcnow()
					db.session.commit()
					flash("Logged in successfully", 'success')
					return redirect(request.args.get('next') or url_for('index.index'))
				else:
					flash("Failed to login", 'error')
			else:
				flash("Invalid password", 'error')
		else:
			flash("Invalid username", 'error')
	return render_template('login/login.html', form=form)

@blueprint.route('/register', methods=['GET', 'POST'])
def register():
	form = RegisterForm()
	if form.validate_on_submit():
		if User.query.filter_by(username = form.username.data).count():
			flash("Username is already in use", 'error')
			return render_template('login/register.html', form = form)
		if User.query.filter_by(email = form.email.data).count():
			flash("The email is already in use", 'error')
			return render_template('login/register.html', form = form)
		role = Role.query.filter_by(title='Follower').first()
		new_user = User(form.username.data,
			form.password.data,
			form.email.data,
			form.firstname.data,
			form.lastname.data)
		db.session.add(new_user)
		db.session.commit()
		login_user(new_user)
		notify_admin_message = Message("New User Created: %s" % new_user.username,
			recipients=["kage.urufu@gmail.com"])
		notify_user_message = Message("Your account has been created", 
			recipients = [new_user.email])
		notify_admin_message.html = render_template('email/notify_admin_new_user.html', user=new_user)
		notify_user_message.html = render_template('email/notify_new_user.html', user=new_user)
		mail.send(notify_admin_message)
		mail.send(notify_user_message)
		flash("User was created, admin approval is necessary before login is allowed!", 'success')
		return redirect(url_for('index.index'))
	return render_template('login/register.html', form = form)

@blueprint.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('index.index'))