from flask import Blueprint, redirect, render_template, abort, url_for
from flask.ext.login import current_user
from alcoholicism import db
from alcoholicism.models.user import User, Notification
from alcoholicism.models.forum import Tag, Topic, Post, PostLike
from alcoholicism.forms.forum import PostForm, CreateTopicForm
from datetime import datetime

blueprint = Blueprint('forum', __name__, template_folder = 'templates')

@blueprint.route('/forum')
@blueprint.route('/forum/tag/<tag>')
@blueprint.route('/forum/page/<page>')
@blueprint.route('/forum/tag/<tag>/page/<page>')
def index(tag = None, page=1):
	page = int(page)
	if tag:
		#tag = Tag.query.filter_by(tag = tag).first()
		filter_tag = Tag.query.filter_by(tag = tag).first()
		query = Topic.query.filter(
			Topic.tags.any(
				Tag.id.in_([filter_tag.id])
				)
			).order_by('lastTime desc')
	else:
		query = Topic.query.order_by('lastTime desc')
		tag = None
	pages = query.count() / 20 
	if pages == 0: pages = 1
	topics = query.limit(20).offset((page - 1) * 20).all()
	return render_template('forum/index.html', topics = topics, pagetag = tag, page = page, pages = pages)

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
		notification = Notification(topic.author,
									"%s has replied to your post" % current_user,
									url_for('forum.topic', topicid=topic.id))
		db.session.add(newPost)
		db.session.add(notification)
		db.session.commit()
		return redirect(url_for('forum.topic', topicid = topicid))	
	return render_template('forum/topic.html', topic = topic, form = form)

@blueprint.route('/forum/like/<topicid>/<postid>')
def like(topicid = None, postid = None):
	if not postid or not topicid:
		return redirect(url_for('forum.topic', topicid=topicid))
	post = Post.query.filter_by(id = postid).first()
	if not post:
		return redirect(url_for('forum.topic', topicid=topicid))
	isLiked = PostLike.query.filter_by(user_id = current_user.id, post_id = postid)
	if isLiked.count():
		db.session.delete(isLiked.first())
		db.session.commit()
	else: 
		like = PostLike(current_user, post)
		notification = Notification(post.author,
									"%s has liked your post" % current_user,
									url_for('forum.topic', topicid=post.topic.id))
		db.session.add(like)
		db.session.add(notification)
		db.session.commit()
	return redirect(url_for('forum.topic', topicid=topicid))
