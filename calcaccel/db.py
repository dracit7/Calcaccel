import sqlite3

import click
from flask import current_app
from flask import g
from flask import request
from flask.cli import with_appcontext
from werkzeug.security import generate_password_hash

from calcaccel.admin import bp
from calcaccel.admin import admin_required


def get_db():
  """Connect to the application's configured database. The connection
  is unique for each request and will be reused if this is called
  again.
  """
  if "db" not in g:
    g.db = sqlite3.connect(
        current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
    )
    g.db.row_factory = sqlite3.Row

  return g.db


def close_db(e=None):
  """If this request connected to the database, close the
  connection.
  """
  db = g.pop("db", None)

  if db is not None:
    db.close()


def init_db():
  """Clear existing data and create new tables."""
  db = get_db()

  with current_app.open_resource("schema.sql") as f:
    db.executescript(f.read().decode("utf8"))

  db.execute(
      "INSERT INTO user (username, password, identity, maxgrade) VALUES (?, ?, ?, ?)",
      ("admin", generate_password_hash("dlcqtql"), "admin", 9999)
  )
  db.commit()


@click.command("init-db")
@with_appcontext
def init_db_command():
  """Clear existing data and create new tables."""
  init_db()
  click.echo("Initialized the database.")


def init_app(app):
  """Register database functions with the Flask app. This is called by
  the application factory.
  """
  app.teardown_appcontext(close_db)
  app.cli.add_command(init_db_command)


@bp.route("/listdb/<table>")
@admin_required
def list_db(table):
  try:
    users = ""
    c = get_db().cursor()
    c.execute("SELECT * FROM "+table)
    for user in c:
      users += str(tuple(user)) + "<br>"
    return users
  except Exception as err:
    return str(err)


@bp.route("/deldb/<table>")
@admin_required
def del_db(table):
  if table == "user":
    try:
      username = request.args["usr"]
      conn = get_db()
      c = conn.cursor()
      c.execute("DELETE FROM user WHERE username = ?", (username,))
      conn.commit()
      return "Deleted %s successfully" % username
    except Exception as err:
      return str(err)
  if table == "runtime_data":
    try:
      username = request.args["usr"]
      conn = get_db()
      c = conn.cursor()
      c.execute("DELETE FROM runtime_data WHERE id = ?", (username,))
      conn.commit()
      return "Deleted %s successfully" % username
    except Exception as err:
      return str(err)

def query(query, args=(), fetchone=False):
  try:
    cur = get_db().execute(query, args)
    if fetchone:
      rv = cur.fetchone()
    else:
      rv = cur.fetchall()
    cur.close()
    return rv
  except Exception as err:
    return str(err)


def execute(query, args=()):
  try:
    db = get_db()
    db.cursor().execute(query, args)
    db.commit()
    return "executed successfully"
  except Exception as err:
    return str(err)
