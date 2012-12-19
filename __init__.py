from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.bcrypt import Bcrypt
from flask.ext.markdown import Markdown
from datetime import datetime

app = Flask(__name__)
app.config.from_pyfile('settings.cfg')

Markdown(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

loginmanager = LoginManager()
loginmanager.setup_app(app)

from alcoholicism import filters
from alcoholicism.views import index, login, user, admin, forum, api

app.register_blueprint(index.blueprint)
app.register_blueprint(login.blueprint)
app.register_blueprint(user.blueprint)
app.register_blueprint(admin.blueprint)
app.register_blueprint(forum.blueprint)
app.register_blueprint(api.blueprint)

from alcoholicism.models.user import User

@loginmanager.user_loader
def load_user(userid):
	user = User.query.filter_by(id=userid).first()
	user.last_access = datetime.utcnow()
	db.session.commit()
	return user

loginmanager.login_view = 'login.login'

db.create_all()