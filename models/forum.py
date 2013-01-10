from alcoholicism import db
from datetime import datetime
#from alcoholicism.db import db.Model, db.Column, db.Integer, db.String, db.Enum, db.DateTime, db.relationship, db.ForeignKey, db.Text

class Topic(db.Model):
	__tablename__ = 'forum_topics'
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(500))
	author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	author = db.relationship('User', lazy="joined")
	time = db.Column(db.DateTime)
	lastTime = db.Column(db.DateTime)
	sticky = db.Column(db.Boolean)
	locked = db.Column(db.Boolean)
	posts = db.relationship("Post", backref="forum_topics")
	tags = db.relationship("Tag",
		secondary=db.Table('topic_tags',
			db.Column('topic_id', db.Integer, db.ForeignKey('forum_topics.id')),
			db.Column('tags.id', db.Integer, db.ForeignKey('tags.id'))
		)
	)
	def __init__(self, title, author, tags=[]):
		self.author = author
		self.lastAuthor = author
		self.title = title
		self.time = datetime.utcnow()
		self.lastTime = datetime.utcnow()
		self.sticky = False
		self.locked = False
		for tag in tags:
			self.tags.append(tag)

	def __repr__(self):
		return '<Topic: %s>' % self.title
	def __str__(self):
		return '%s' % self.title

class Post(db.Model):
	__tablename__ = 'forum_posts'
	id = db.Column(db.Integer, primary_key=True)
	author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	author = db.relationship('User', lazy="joined")
	message = db.Column(db.Text)
	time = db.Column(db.DateTime)
	topic_id = db.Column(db.Integer, db.ForeignKey('forum_topics.id'))
	topic = db.relationship('Topic')
	likes = db.relationship("PostLike", backref="forum_likes")
	def __init__(self, topic, author, message):
		self.author = author
		self.message = message
		self.topic = topic
		self.time = datetime.utcnow()

	def __repr__(self):
		return '<Post: Topic #%s - #%s>' % (self.topic_id, self.id)
	def __str__(self):
		return "%s" % self.message

class Tag(db.Model):
	__tablename__ = 'tags'
	id = db.Column(db.Integer, primary_key=True)
	tag = db.Column(db.String(40), unique=True)
	def __init__(self, tag):
		self.tag = tag
	def __repr__(self):
		return '<Tag: %s>' % self.tag
	def __str__(self):
		return '%s' % self.tag

class PostLike(db.Model):
	__tablename__ = 'forum_likes'
	id = db.Column(db.Integer, primary_key=True)
	post_id = db.Column(db.Integer, db.ForeignKey('forum_posts.id'))
	post = db.relationship('Post')
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	user = db.relationship('User')

	def __init__(self, user, post):
		self.post = post
		self.user = user

	def __repr__(self):
		return "<Like: %s by %s>" % (self.post, self.user)