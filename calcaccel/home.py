from flask import Blueprint
from flask import render_template
from flask import request
from flask import session

from calcaccel.db import query, execute
from calcaccel.auth import login_required

bp = Blueprint("home", __name__, url_prefix="/home")


@bp.route("/mistakes", methods=("GET", "POST"))
@login_required
def mistakes():
    """Index page of survival mode."""
    if request.method == "GET":
        mistakes = query("SELECT * FROM mistake WHERE user_id = ?",
            (session["user_id"], ), fetchone=False)
        return render_template("home/mistakes.html", mistakes=mistakes)

    if request.method == "POST":
        mistake = request.form["mistake"]
        history = query(
            "SELECT * FROM mistake WHERE content = ?", 
            (mistake, ), 
            fetchone=True
        )
        if history == None:
            execute(
                "INSERT INTO mistake (user_id, error_times, content) VALUES (?, ?, ?)",
                (session["user_id"], 1, mistake)
            )
        else:
            execute(
                "UPDATE mistake SET error_times = ? WHERE id = ?",
                (history['error_times']+1, history["id"])
            )
        return ""