from alcoholicism import db
from datetime import datetime

class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80))
	message = db.Column(db.Text)
	time = db.Column(db.DateTime)

	def __init__(self, name, message):
		self.name = name
		self.message = message
		self.time = datetime.utcnow()

	def __repr__(self):
		return '<Post %r>' % self.name