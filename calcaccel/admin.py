import functools

from flask import Blueprint
from flask import session

bp = Blueprint("admin", __name__, url_prefix="/admin")


def admin_required(view):
  """Only admin user could visit sites with @admin_required."""

  @functools.wraps(view)
  def wrapped_view(**kwargs):
    if session.get("user_id") is not 1:
      return ""

    return view(**kwargs)

  return wrapped_view
