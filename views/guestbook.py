from flask import Blueprint, render_template, g, request, redirect, url_for
from alcoholicism import db
from alcoholicism.models.post import Post

blueprint = Blueprint('guestbook', __name__, template_folder='templates')

@blueprint.route('/guestbook', methods=['GET', 'POST'])
def guestbook():
	if request.method == 'POST':
		if 'name' in request.form and 'message' in request.form:
			post = Post(request.form['name'], request.form['message'])
			db.session.add(post)
			db.session.commit()
			return redirect(url_for('guestbook.guestbook'))

	posts = Post.query.all()
	return render_template('guestbook.html', posts = posts)