from flask.ext.wtf import Form, SelectField, Required, SubmitField, EqualTo, Email, Length, HiddenField, TextField, TextAreaField
from alcoholicism.models.user import Role, User

class CreateTopicForm(Form):
	title = TextField('Topic Title')
	message = TextAreaField('Message')
	tags = TextField('Tags', default="General")
	submit = SubmitField('Create Topic')

class PostForm(Form):
	message = TextAreaField('Message')
	submit = SubmitField('Submit')
