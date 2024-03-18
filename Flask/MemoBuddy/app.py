from flask import Flask
from flask import render_template

import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

@app.route("/", methods=["GET", "POST"])
def index():
	return render_template("index.html")

if __name__ == "__main__":
	app.run(debug=True, host='0.0.0.0', port=32500)