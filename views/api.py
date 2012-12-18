from flask import Blueprint, request
from alcoholicism import db
from alcoholicism.models.forum import Tag
from alcoholicism.models.user import Role, User
from json import dumps
blueprint = Blueprint('api', __name__)

@blueprint.route('/api/tags')
def tags():
	tags = []
	for tag in Tag.query.all():
		tags.append(str(tag))
	return dumps(tags)

@blueprint.route('/api/roles')
def roles():
	roles = {}
	for role in Role.query.all():
		roles[int(role.rank)] = role.title
	return dumps(roles)