from flask import Flask, render_template
from flask import g

app = Flask(__name__)

from app.company1 import bp as bp1
from app.company2 import bp as bp2

companies = [
	["Company 1", bp1, "/company1"],
	["Company 2", bp2, "/company2"],
]

for title, bp, url in companies:
	app.register_blueprint(bp, url_prefix=url)

@app.route("/")
def index():
	r = ""
	for title, bp, url in companies:
		r += f'<a href="{url}">{title}</a><br>'
	return render_template("index.tpl", companies=r)
