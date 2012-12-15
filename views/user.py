from flask import Blueprint, render_template

blueprint = Blueprint('user', __name__, template_folder='templates')

@blueprint.route('/profile', methods=['POST', 'GET'])
def profile():
	return render_template('user/profile.html')