from alcoholicism import db
from datetime import datetime
from alcoholicism import bcrypt

class User(db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(24), unique=True)
	email = db.Column(db.String(120), unique=True)
	passHash = db.Column(db.String(60))
	firstname = db.Column(db.String(30))
	lastname = db.Column(db.String(30))
	status = db.Column(db.Enum('accepted','denied','pending','banned'))
	created = db.Column(db.DateTime)
	last_access = db.Column(db.DateTime)
	last_login = db.Column(db.DateTime)
	role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
	role = db.relationship('Role', lazy="joined")
	posts = db.Column(db.Integer)

	def __init__(self, username, password, email, firstname, lastname):
		self.status = 'pending'
		self.created = datetime.utcnow()
		self.username = username
		self.email = email
		self.firstname = firstname
		self.lastname = lastname
		self.passHash = self.hashPassword(password)
		self.posts = 0
		self.role_id = 4 #Follower, for now... better way to do this?

	def __repr__(self):
		return '<User: %s>' % self.username

	def __str__(self):
		return '%s %s %s' % (self.role, self.firstname, self.lastname)
		
	def setPassword(self, password):
		self.passHash = self.hashPassword(password)

	def hashPassword(self, password):
		return bcrypt.generate_password_hash(password)

	def checkPassword(self, password):
		if not self.passHash:
			return False
		return bcrypt.check_password_hash(self.passHash, password)

	def __cmp__(self, other):
		if self.role.rank > other.role.rank:	return 1
		if self.role.rank < other.role.rank:	return -1
		return 0

	#Helper functions for flask-login
	def get_id(self):
		return self.id

	def is_active(self):
		return self.status == 'accepted'

	def is_anonymous(self):
		return False

	def is_authenticated(self):
		return True
		

class Role(db.Model):
	__tablename__ = 'roles'
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(40), unique=True)
	rank = db.Column(db.Integer, unique=True)
	def __init__(self, title, rank):
		#title should be the actual title for the role, rank is somewhat... arbitrary
		self.title = title
		self.rank = rank

	def __repr__(self):
		return '<Role: %s>' % self.title
	
	def __str__(self):
		return self.title

	def __cmp__(self, other):
		if self.rank > other.rank:	return 1
		if self.rank < other.rank:	return -1
		return 0