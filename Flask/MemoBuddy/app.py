from flask import Flask
from flask import render_template
from flask import request
from flask import redirect

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc

import secrets
import datetime

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///memobuddy.db'

db = SQLAlchemy(app)
dt_jst = datetime.timezone(datetime.timedelta(hours=9), 'JST')

class Memo(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	post_time = db.Column(db.String(32), nullable=False)
	memo = db.Column(db.String(256), nullable=False)

@app.route("/write", methods=["POST"])
def write():
	if request.method == "POST":
		memo_a = request.form.get("memo")
		dt_now = datetime.datetime.now(dt_jst).strftime('%Y-%m-%d %H:%M:%S')
		if memo_a != "":	
			memo = Memo(
				memo=memo_a,
				post_time=dt_now
			)
			db.session.add(memo)
			db.session.commit()
		return redirect("/")

@app.route("/", methods=["GET", "POST"])
def index():
	memos = Memo.query.order_by(desc(Memo.post_time)).all()
	print(memos)
	return render_template("index.html", memos=memos)

if __name__ == "__main__":
	app.run(debug=True, host='0.0.0.0', port=32500)
