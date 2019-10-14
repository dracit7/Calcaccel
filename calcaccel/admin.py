import functools

from flask import Blueprint
from flask import session

bp = Blueprint("admin", __name__, url_prefix="/admin")


def admin_required(view):
  """Only admin user could visit sites with @admin_required."""

  @functools.wraps(view)
  def wrapped_view(**kwargs):

    # Admin user's user_id is always 1, that's defined by db_init().
    # If current user's id is not 1, he is not admin surely.
    if session.get("user_id") is not 1:
      return "" # Show nothing to non-admin users

    return view(**kwargs)

  return wrapped_view
