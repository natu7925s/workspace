from flask import Flask
from flask import render_template
from flask import redirect

from flask_sqlalchemy import SQLAlchemy

import secrets
import datetime
import random

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bookinger.db'

db = SQLAlchemy(app)
dt_jst = datetime.timezone(datetime.timedelta(hours=9), 'JST')

class Room(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	name = db.Column(db.String(8), nullable=False)

@app.route("/booking/new", methods=["POST"])
def newbook():
	return redirect("/")

@app.route("/booking", methods=["GET"])
def booking():
	rooms = Room.query.all()
	return render_template("booking.html", rooms=rooms)

@app.route("/", methods=["GET", "POST"])
def index():
	rooms = []
	for i in range(1, 10):
		tmp = ["部屋{}".format(i)]
		for j in range(7):

			if random.randint(0, 1) == 1:
				tmp.append("予約")
			else:
				tmp.append("")
		rooms.append(tmp)
	
	return render_template("index.html", rooms=rooms)

if __name__ == "__main__":
	app.run(debug=True, host='0.0.0.0', port=32500)