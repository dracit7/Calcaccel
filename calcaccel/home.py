from flask import Blueprint
from flask import render_template
from flask import request
from flask import session

from calcaccel.db import query, execute
from calcaccel.auth import login_required

bp = Blueprint("home", __name__, url_prefix="/home")


@bp.route("/<user>/mistakes")
@login_required
def index(user):
    """Index page of survival mode."""

    mistakes = {}
    mistakes["content"] = []
    records = query("SELECT * FROM mistake WHERE id = ?",
                    (session["user_id"], ), fetchone=False)
    for record in records:
        mistakes["content"] += record["content"]
        mistakes["times"] += record["error_times"]
    return render_template("home/mistakes.html", mistakes=mistakes)
