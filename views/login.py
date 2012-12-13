from flask import Blueprint, request, render_template, g, url_for, flash, redirect
from alcoholicism import db, loginmanager
from alcoholicism.models.user import User
from alcoholicism.forms.login import LoginForm
from flask.ext.login import login_required, login_user, logout_user, current_user

blueprint = Blueprint('login', __name__, template_folder='templates')
@blueprint.route("/login", methods=["GET", "POST"])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user:
			if user.checkPassword(form.password.data):
				remember = form.remember
				if login_user(user, remember = remember):
					flash("Logged in successfully")
					return redirect(request.args.get('next') or url_for('index.index'))
				else:
					flash("Failed to login")
			else:
				flash("Invalid password")
		else:
			flash("Invalid username")
	return render_template('login.html', form=form)

@blueprint.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('index.index'))