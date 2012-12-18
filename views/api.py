from flask import Blueprint, request
from alcoholicism import db
from alcoholicism.models.forum import Tag
from alcoholicism.models.user import Role, User
from json import dumps
blueprint = Blueprint('api', __name__)

@blueprint.route('/api/tags')
def tags():
	tags = []
	if 'term' in request.args:
		alltags = Tag.query.filter(Tag.tag.startswith(request.args['term'])).all()
	else:
		alltags = Tag.query.all()
	for tag in alltags:
		tags.append(str(tag))
	return dumps(tags)

@blueprint.route('/api/roles')
def roles():
	roles = {}
	for role in Role.query.all():
		roles[int(role.rank)] = role.title
	return dumps(roles)