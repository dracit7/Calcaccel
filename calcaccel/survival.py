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
  db = get_db()

  you = db.execute(
    "SELECT * FROM user"
    " WHERE username = ?",
    (session["user_id"],)
  ).fetchone()

  users = db.execute(
    "SELECT username, maxgrade FROM user"
    " WHERE identity = ?"
    " ORDER BY maxgrade DESC",
    ("child",)
  ).fetchall()

  return render_template("survival/index.html", users=users, you=you)

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

  # TODO: 在这里插入将用户的成绩记录到数据库中的代码