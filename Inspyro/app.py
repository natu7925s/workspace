from flask import Flask
from flask import redirect
from flask import request
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc

from markupsafe import Markup


import secrets
import datetime

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inspyro.db'

db = SQLAlchemy(app)
dt_jst = datetime.timezone(datetime.timedelta(hours=9), 'JST')

class Idea(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	name = db.Column(db.String(128), nullable=False)
	created_date = db.Column(db.String(32), nullable=False)

class Tweet(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	idea_key = db.Column(db.Integer, nullable=False)
	post_time = db.Column(db.String(32), nullable=False)
	tweet = db.Column(db.String(256), nullable=False)

@app.route("/del/<int:id>", methods=["POST"])
def idea_del(id):
	idea = Idea.query.get(id)
	db.session.delete(idea)
	tweets = Tweet.query.filter(Tweet.idea_key == id)
	for tw in tweets:
		db.session.delete(tw)
	db.session.commit()
	return redirect("/list")

@app.route("/list", methods=["GET", "POST"])
def idea_list():
	if request.method == "POST":
		name = request.form.get("ideaname")
		dt_now = datetime.datetime.now(dt_jst).strftime('%Y-%m-%d %H:%M:%S')
		if name != "":	
			idea = Idea(
				name=name,
				created_date=dt_now
			)
			db.session.add(idea)
			db.session.commit()
		return redirect("/list")
	
	else:
		ideas = Idea.query.all()
		return render_template("list.html", ideas=ideas)

@app.route("/<int:id>", methods=["GET", "POST"])
def main(id):
	if request.method == "POST":
		tweet_a = request.form.get("tweet")
		dt_now = datetime.datetime.now(dt_jst).strftime('%Y-%m-%d %H:%M:%S')
		if tweet_a != "":
			tweet = Tweet(
				idea_key=id,
				post_time=dt_now,
				tweet=Markup(tweet_a.replace('\r', '<br>'))
			)
			db.session.add(tweet)
			db.session.commit()

	ideas = Idea.query.all()
	tweets = Tweet.query.filter(Tweet.idea_key == id).order_by(desc(Tweet.post_time))
	print(tweets)
	return render_template("main.html", ideas=ideas, tweets=tweets)

@app.route("/", methods=["GET", "POST"])
def index():
	ideas = Idea.query.all()
	return render_template("index.html", ideas=ideas)

if __name__ == "__main__":
	app.run(debug=True, host='0.0.0.0', port=32500)
