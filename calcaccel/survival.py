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

from calcaccel.db import get_db
from calcaccel.auth import login_required

bp = Blueprint("survival", __name__, url_prefix="/survival")

@bp.route("/")
@login_required
def index():
  """Index page of survival mode."""
  return render_template("survival/index.html")

@bp.route("/scoreboard")
@login_required
def scoreboard():
  """Scoreboard page of survival mode."""
  db = get_db()

  you = db.execute(
    "SELECT * FROM user"
    " WHERE id = ?",
    (session["user_id"],)
  ).fetchone()

  users = db.execute(
    "SELECT username, maxgrade FROM user"
    " WHERE identity = ?"
    " ORDER BY maxgrade DESC",
    ("child",)
  ).fetchall()

  return render_template("survival/scoreboard.html", users=users, you=you)

@bp.route("/play")
@login_required
def play():
  """Play page"""
  return render_template("survival/play.html")


@bp.route("/score", methods=["POST"])
@login_required
def score():
  """Send score back to backend"""
  db = get_db()

  score = request.form["score"]
  user_id = session["user_id"]

  maxgrade = db.execute(
    "SELECT maxgrade FROM user WHERE id = ?",
    (user_id)
  ).fetchone()

  if maxgrade < score:
    db.execute("UPDATE user SET maxgrade = ? WHERE username = ?",
      (score, user_id))
    db.commit()
