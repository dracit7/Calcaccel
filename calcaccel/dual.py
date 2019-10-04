import functools

from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from calcaccel.db import query, get_db
from calcaccel.auth import login_required

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
      session["peer_username"] = peer["username"]
      session["your_username"] = you["username"]
      gameid = you["username"] + "&" + peer["username"]
      return redirect("/dual/play/" + gameid + "?player=1")

  return render_template("dual/index.html")


@bp.route("/play/<gameid>", methods=["POST", "GET"])
@login_required
def play(gameid):
  """Play page"""
  return render_template("dual/play.html", gameid=gameid)
