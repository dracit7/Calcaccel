from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import session

from calcaccel.db import query, execute
from calcaccel.auth import login_required
from calcaccel.config import conf

bp = Blueprint("shop", __name__, url_prefix="/shop")


@bp.route("/", methods=["GET", "POST"])
@login_required
def handler():
    id = session["user_id"]
    talent = query("SELECT * FROM talents WHERE id = ?",
                   (id,), fetchone=True)
    error = None

    if talent is None:
        error = "No such user"
        flash(error, "error")

    if request.method == "GET":
        if error is None:
            return talent

    if request.method == "POST":
        if error is None:
            execute("UPDATE talents SET (prevent_death, blessed) = (?, ?) WHERE id = ?",
                    (request.form["prevent_death"], request.form["blessed"], id))
            return "Success"
