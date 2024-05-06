from flask import Flask
from flask import request
from flask import redirect
from flask import render_template
from flask import send_from_directory

from werkzeug.utils import secure_filename

import os
import time
import datetime

import secrets

SV_URL = "http://192.168.10.107:8000/filer/"

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

@app.route("/", methods=["GET"])
def index():
	return render_template('index.html')

@app.route("/create", methods=["GET", "POST"])
def create_url():
	if request.method == "POST":
		url = SV_URL
		gen_hash = secrets.token_hex(12)

		os.makedirs("./lib/{}".format(gen_hash), exist_ok=True)
		print("[@] Generate Hash : {}".format(gen_hash))

		return render_template('create.html', url="{}{}".format(url, gen_hash))
	else:
		return redirect("/")

@app.route("/filer/<string:path_hash>", methods=["GET", "POST"])
def folder(path_hash):
	if os.path.exists("./lib/{}".format(path_hash)):
		if request.method == "POST":
			if request.files.getlist('upfiles')[0].filename:
				upload_files = request.files.getlist('upfiles')
				for file in upload_files:
					file.save("./lib/{}/".format(path_hash) + secure_filename(file.filename))
			return redirect("/filer/{}".format(path_hash))
		else:
			sort_mtime("./lib/{}".format(path_hash))
			return render_template("filer.html", filelist=sort_mtime("./lib/{}".format(path_hash)), phash=path_hash)
	else:
		return redirect("/")

@app.route("/filer/<string:path_hash>/<string:filename>", methods=["GET"])
def get_file(path_hash, filename):
	if os.path.isfile("./lib/{}/{}".format(path_hash, filename)):
		return send_from_directory('./lib/{}'.format(path_hash), filename, as_attachment=True)
	else:
		return redirect("/filer/{}".format(path_hash))
		
@app.route("/filer/<string:path_hash>/del/<string:filename>", methods=["GET"])
def del_file(path_hash, filename):
	if os.path.isfile("./lib/{}/{}".format(path_hash, filename)):
		os.remove("./lib/{}/{}".format(path_hash, filename))
	return redirect("/filer/{}".format(path_hash))
		
def sort_mtime(rootdir):
	xs = []
	flist = []
	for root, dir, files in os.walk(rootdir):
		for f in files:
			path = os.path.join(root, f)
			xs.append((os.path.getmtime(path), path))
	for mtime, path in sorted(xs):
		name = os.path.basename(path)
		t = datetime.datetime.fromtimestamp(mtime)
		flist.append([name, t])
	return flist


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8000)