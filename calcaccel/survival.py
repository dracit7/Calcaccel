from flask import Blueprint
from flask import render_template
from flask import request
from flask import session

from calcaccel.db import query, execute
from calcaccel.auth import login_required

bp = Blueprint("survival", __name__, url_prefix="/survival")


@bp.route("/")
@login_required
def index():
    """Index page of survival mode."""
    return render_template("survival/index.html", mode="survival")


@bp.route("/scoreboard")
@login_required
def scoreboard():
    """Scoreboard page of survival mode."""
    you = query(
        "SELECT * FROM user"
        " WHERE id = ?",
        (session["user_id"],),
        fetchone=True
    )
    users = query(
        "SELECT username, maxgrade FROM user"
        " WHERE identity = ?"
        " ORDER BY maxgrade DESC",
        ("child",),
        fetchone=False
    )
    return render_template("survival/scoreboard.html", users=users, you=you, mode="survival")


@bp.route("/play")
@login_required
def play():
    """Play page"""
    return render_template("survival/play.html", mode="survival")


@bp.route("/score", methods=["POST"])
@login_required
def score():
    """Send score back to backend"""

    score = request.form.get("score", type=int)
    user_id = session["user_id"]

    maxgrade = query(
        "SELECT maxgrade FROM user WHERE id = ?",
        (user_id, ),
        fetchone=True
    )

    if query != None:
        mg, = tuple(maxgrade)
        if mg < score:
            execute(
                "UPDATE user SET maxgrade = ? WHERE id = ?",
                (score, user_id)
            )

    return ""
