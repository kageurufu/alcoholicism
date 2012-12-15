from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.bcrypt import Bcrypt

app = Flask(__name__)
app.config.from_pyfile('settings.cfg')

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

loginmanager = LoginManager()
loginmanager.setup_app(app)

from alcoholicism.views import index, login, user, admin

app.register_blueprint(index.blueprint)
app.register_blueprint(login.blueprint)
app.register_blueprint(user.blueprint)
app.register_blueprint(admin.blueprint)

from alcoholicism.models.user import User

@loginmanager.user_loader
def load_user(userid):
	return User.query.filter_by(id=userid).first()

loginmanager.login_view = 'login.login'

db.create_all()