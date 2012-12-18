from flask.ext.wtf import Form, SelectField, Required, SubmitField, EqualTo, Email, Length, HiddenField, TextField, TextAreaField
from alcoholicism.models.user import Role, User

class CreateTopicForm(Form):
	title = TextField('Topic Title', [Required()])
	message = TextAreaField('Message', [Required()])
	tags = TextField('Tags', [Required()], default="General")
	submit = SubmitField('Create Topic')

class PostForm(Form):
	message = TextAreaField('Message', [Required()])
	submit = SubmitField('Submit', [Required()])
