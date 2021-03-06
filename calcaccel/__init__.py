import os

from flask import Flask
from flask import render_template

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__, instance_relative_config=True)
  app.config.from_mapping(
      SECRET_KEY='dev',
      DATABASE=os.path.join(app.instance_path, 'calcaccel.sqlite'),
  )

  if test_config is not None:
    # load the test config if passed in
    app.config.from_mapping(test_config)

  # ensure the instance folder exists
  try:
    os.makedirs(app.instance_path)
  except OSError:
    pass

  # welcome page
  @app.route('/')
  def index():
    return render_template("index.html")

  # register the database commands
  from calcaccel import db

  db.init_app(app)

  # apply the blueprints to the app
  from calcaccel import auth
  from calcaccel import survival
  from calcaccel import dual
  from calcaccel import admin
  from calcaccel import home

  app.register_blueprint(auth.bp)
  app.register_blueprint(survival.bp)
  app.register_blueprint(dual.bp)
  app.register_blueprint(home.bp)
  app.register_blueprint(admin.bp)

  return app
