from flask import Blueprint, render_template, g
from random import choice

blueprint = Blueprint('index', __name__, template_folder='templates')

@blueprint.route('/')
def index():
	quotes = ("Absolution through Absolut&#0153;",
		"A shot for your sins",
		"Bless the Holy Spirits, Jameson, Jerry, and Jack",
		"Here's to Honor. To getting on her, staying on her, and if you can't come in her, come on her",
		"Our Lager,<br />Which art in barrels<br />Hallowed be thy drink.<br />Thy will be drunk,<br />I will be drunk,<br />At home as in the tavern.<br />Give us this day our foamy head<br />and forgive us our spillages<br />as we forgive those that spill against us<br />and lead us not into incarceration.<br />But deliver us from hang-overs,<br />for thine is the beer,<br />The bitter and the lager<br />forever and ever<br />Barmen!")
	return render_template('index/index.html', quote=choice(quotes))
