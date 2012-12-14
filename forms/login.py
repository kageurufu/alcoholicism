from flask.ext.wtf import Form, TextField, Required, BooleanField, PasswordField, SubmitField, EqualTo, Email, Length

class LoginForm(Form):
	username = TextField("Username")
	password = PasswordField("Password")
	remember = BooleanField("Remember Me")
	submit = SubmitField("Login")

class RegisterForm(Form):
	username = TextField("Username", 
		[Required(), 
			Length(3, 24, "Your username must be between 3 and 24 characters")])
	password = PasswordField("Password", 
		[Required(), 
			EqualTo('confirm', "Your password did not match"),
			Length(8, message="Your password must be at least 8 characters")])
	confirm = PasswordField("Confirm Password", 
		[Required()])
	email = TextField("Email Address", 
		[Required(), 
			Email('Please enter a valid email address')])
	firstname = TextField("First Name", 
		[Required()])
	lastname = TextField("Last Name", 
		[Required()])
	submit = SubmitField("Register")