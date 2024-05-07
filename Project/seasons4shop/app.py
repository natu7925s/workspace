from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy

import secrets
import datetime

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///memobuddy.db'

db = SQLAlchemy(app)
dt_jst = datetime.timezone(datetime.timedelta(hours=9), 'JST')



@app.route('/admin', methods=["GET"])
def admin():
	return render_template("admin.html")

@app.route("/", methods=["GET", "POST"])
def index():
	return render_template("index.html")

if __name__ == "__main__":
	app.run(debug=True, host='0.0.0.0', port=32500)

