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

bp = Blueprint("admin", __name__, url_prefix="/admin")

def admin_required(view):
  """Only admin user could visit sites with @admin_required."""

  @functools.wraps(view)
  def wrapped_view(**kwargs):
    if session.get("user_id") is not 1:
      return ""

    return view(**kwargs)

  return wrapped_view