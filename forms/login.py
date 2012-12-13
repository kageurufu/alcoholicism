from flask.ext.wtf import Form, TextField, Required, BooleanField, PasswordField, SubmitField

class LoginForm(Form):
	username = TextField("Username")
	password = PasswordField("Password")
	remember = BooleanField("Remember Me")
	submit = SubmitField("Login")