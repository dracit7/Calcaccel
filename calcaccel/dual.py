from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import session

from calcaccel.db import query, execute
from calcaccel.auth import login_required

import time

bp = Blueprint("dual", __name__, url_prefix="/dual")


@bp.route("/", methods=["POST", "GET"])
@login_required
def index():
	"""Index page of dual mode."""
	you = query(
			"SELECT * FROM user"
			" WHERE id = ?",
			(session["user_id"],),
			fetchone=True
	)

	if request.method == "POST":
		peer = query("SELECT * FROM user WHERE username = ?",
								 (request.form["username"],), fetchone=True)

		error = None

		if peer is None:
			error = "No such user."
			flash(error, "error")

		if peer == you:
			error = "You cannot play with yourself!"
			flash(error, "error")

		if error is None:
			session["peer_id"] = peer["id"]
			execute("INSERT INTO runtime_data (id, score, timeleft, currenttime) VALUES (?, ?, ?, ?)",
							(you["id"], 0, 0, int(time.time())))
			return redirect("/dual/play?peer=%s" % peer["username"])

	return render_template("dual/index.html")


@bp.route("/play", methods=["POST", "GET"])
@login_required
def play():
	"""Play page"""
	return render_template("dual/play.html", peer=request.args["peer"])


@bp.route("/message", methods=["POST", "GET"])
@login_required
def message():
	if request.method == "POST":
		score = request.form["score"]
		timeleft = request.form["timeleft"]
		execute(
			"UPDATE runtime_data SET (score, timeleft, currenttime) = (?, ?, ?) WHERE id = ?",
			(score, timeleft, int(time.time()), session["user_id"])
		)

	if request.method == "GET":
		peer = query(
			"SELECT * FROM runtime_data WHERE id = ?",
			(session["peer_id"],),
			fetchone=True
		)
		if peer == None:
			return ""
		_, score, timeleft, currenttime = peer
		request.form["score"] = score
		if currenttime + 2 < int(time.time()):
			# TODO: config time interval
			request.form["timeleft"] = -1
			execute(
				"DELETE FROM runtime_data WHERE id = ?",
				(session["peer_id"], )
			)
		else:
			request.form["timeleft"] = timeleft
		return request.form
