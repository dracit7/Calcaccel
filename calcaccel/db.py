import sqlite3

import click
from flask import current_app
from flask import g
from flask.cli import with_appcontext

import argparse


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


def list_db():
    try:
        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT * FROM user")
        for row in c:
            print(row)
        return True
    except:
        return False


def del_db(username):
    try:
        conn = get_db()
        c = conn.cursor()
        c.execute("DELETE FROM user WHERE id = ?", username)
        conn.commit()
        return True
    except:
        return False


def query(query, args=(), fetchone=False):
    try:
        cur = get_db().execute(query, args)
        rv = cur.fetchall()
        cur.close()
        return (rv[0] if rv else None) if fetchone else rv
    except:
        return None


def execute(query, args=()):
    try:
        db = get_db()
        db.cursor().execute(query, args)
        db.commit()
        return True
    except:
        return False


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Utils for processing database.')
    parser.add_argument('--list', action='store_true',
                        help='list all the item in the database')
    parser.add_argument('--delete', action='store', dest='id', type=int,
                        help='delete an item by its id')
    args = parser.parse_args()
    if args.list:
        list_db()
    if args.id != None:
        del_db(args.id)
