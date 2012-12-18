from flask import Blueprint, render_template, redirect, abort, request, flash, url_for
from flask.ext.login import current_user, login_required
from alcoholicism.models.user import User, Role
from alcoholicism.forms.admin import AcceptForm, UserForm
from alcoholicism import db

from pprint import pprint

blueprint = Blueprint('admin', __name__, template_folder='templates')

@blueprint.route('/admin', methods=['POST', 'GET'])
@login_required
def index():
	if current_user.role.rank < 1000:
		return abort(403)
	roles = Role.query.all()
	return render_template('admin/index.html', roles=roles,)

@blueprint.route('/admin/approve', methods=['POST', 'GET'])
@login_required
def approve():
	if current_user.role.rank < 1000:
		return abort(403)
	form = AcceptForm()
	form.getChoices()
	if form.validate_on_submit():
		role = Role.query.filter_by(id = form.role.data).first()
		user = User.query.filter_by(id = form.userid.data).first()
		if not user:
			return abort(403)
		user.role = role
		user.status = 'approved'
		db.session.commit()
		return redirect(url_for('admin.approve'))
	pending_users = User.query.filter_by(status='pending').all()
	return render_template('admin/approve.html', form=form, pending_users=pending_users)

@blueprint.route('/admin/users', methods=['GET', 'POST'])
@login_required
def users(userid = None):
	if current_user.role.rank < 1000:
		return abort(403)
	form = UserForm()
	form.getChoices()
	if form.validate_on_submit():
		role = Role.query.filter_by(id = form.role.data).first()
		user = User.query.filter_by(id = form.userid.data).first()
		if not user:
			return abort(403)
		user.role = role
		user.status = form.status.data
		db.session.commit()
		return redirect(url_for('admin.users'))
	users = User.query.all()
	return render_template('admin/users.html', form=form, users=users)
