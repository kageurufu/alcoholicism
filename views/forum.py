from flask import Blueprint, redirect, render_template, abort, url_for
from flask.ext.login import current_user
from alcoholicism import db
from alcoholicism.models.user import User
from alcoholicism.models.forum import Tag, Topic, Post
from alcoholicism.forms.forum import PostForm, CreateTopicForm
from datetime import datetime

blueprint = Blueprint('forum', __name__, template_folder = 'templates')

@blueprint.route('/forum')
@blueprint.route('/forum/tag/<tag>')
def index(tag = None):
	if tag:
		#tag = Tag.query.filter_by(tag = tag).first()
		filter_tag = Tag.query.filter_by(tag = tag).first()
		topics = Topic.query.filter(
			Topic.tags.any(
				Tag.id.in_([filter_tag.id])
				)
			).order_by('lastTime desc').all()
	else:
		topics = Topic.query.order_by('lastTime desc').all()
	return render_template('forum/index.html', topics = topics)

@blueprint.route('/forum/create', methods=['POST','GET'])
def createTopic():
	form = CreateTopicForm()
	if form.validate_on_submit():
		taglist = form.tags.data.split(',')
		tags = []
		for tag in taglist:
			tag = tag.strip()
			foundtag = Tag.query.filter_by(tag = tag.strip()).first()
			if not foundtag:
				foundtag = Tag(tag)
				db.session.add(foundtag)
			tags.append(foundtag)
		newTopic = Topic(form.title.data, current_user, tags)
		newPost = Post(newTopic, current_user, form.message.data)
		db.session.add(newTopic)
		db.session.add(newPost)
		db.session.commit()
		return redirect(url_for('forum.topic', topicid = newTopic.id))
	scripts = ['forum.js']
	return render_template('forum/create.html', form = form, scripts=scripts)

@blueprint.route('/forum/topic/<topicid>', methods=['GET', 'POST'])
def topic(topicid = None):
	if not topicid:
		return redirect(url_for('forum.index'))
	form = PostForm()
	topic = Topic.query.filter_by(id = topicid).first()
	if form.validate_on_submit():
		newPost = Post(topic, current_user, form.message.data)
		topic.lastTime = datetime.utcnow()
		db.session.add(newPost)
		db.session.commit()
		return redirect(url_for('forum.topic', topicid = topicid))	
	return render_template('forum/topic.html', topic = topic, form = form)
