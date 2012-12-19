from flask.ext.wtf import Form, SelectField, Required, SubmitField, EqualTo, Email, Length, HiddenField
from alcoholicism.models.user import Role

class AcceptForm(Form):
	role = SelectField('Role', choices = [])
	accept = SubmitField('Approve')
	userid = HiddenField('UserID')

	def getChoices(self):
		roles = Role.query.order_by('rank asc').all()
		self.role.choices = []
		for role in roles:
			self.role.choices.append((u'%s' % role.id, role.title))

class UserForm(Form):
	role = SelectField('Role', choices=[])
	submit = SubmitField('Edit')
	status = SelectField('Status', choices=[('accepted','accepted'), ('pending','pending'), ('banned','banned'), ('denied','denied')])
	userid = HiddenField('UserID')

	def getChoices(self):
		roles = Role.query.order_by('rank asc').all()
		self.role.choices = []
		for role in roles:
			self.role.choices.append((u'%s' % role.id, role.title))
