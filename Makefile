
run:
	@export FLASK_APP=calcaccel &&	export FLASK_ENV=development &&	flask run

db:
	@export FLASK_APP=calcaccel &&	export FLASK_ENV=development &&	flask init-db

format:
	@autopep8 --indent-size 2 -i calcaccel/*.py