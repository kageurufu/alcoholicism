from flask import Blueprint, render_template

blueprint = Blueprint('user', __name__, template_folder='templates')

@blueprint.route('/profile', methods=['POST', 'GET'])
@blueprint.route('/profile/<userid>', methods=['POST', 'GET'])
def profile(userid = None):
	return render_template('user/profile.html')