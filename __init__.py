from flask import Flask, request_started, request
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager, current_user
from flask.ext.bcrypt import Bcrypt
from flask.ext.markdown import Markdown
from flask.ext.mail import Mail
from datetime import datetime
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config.from_pyfile('settings.cfg')

Markdown(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
mail = Mail(app)
loginmanager = LoginManager()
loginmanager.setup_app(app)
toolbar = DebugToolbarExtension(app)

from alcoholicism import filters
from alcoholicism.views import index, login, user, admin, forum, api

app.register_blueprint(index.blueprint)
app.register_blueprint(login.blueprint)
app.register_blueprint(user.blueprint)
app.register_blueprint(admin.blueprint)
app.register_blueprint(forum.blueprint)
app.register_blueprint(api.blueprint)

from alcoholicism.models.user import User, Notification

@loginmanager.user_loader
def load_user(userid):
	user = User.query.filter_by(id=userid).first()
	user.last_access = datetime.utcnow()
	return user


@app.before_request
def checkNotifications():
	if request.args.get('notification'):
		notification = Notification.query.filter_by(id=request.args.get('notification')).first()
		if notification:
			if notification.user.id == current_user.id:
				notification.viewed = True
				current_user.notifications.remove(notification)

@app.after_request
def saveSession(request):
	db.session.commit()
	return request

loginmanager.login_view = 'login.login'

db.create_all()