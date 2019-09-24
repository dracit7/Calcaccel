
run:
	@export FLASK_APP=calcaccel &&	export FLASK_ENV=development &&	flask run

db:
	@export FLASK_APP=calcaccel &&	export FLASK_ENV=development &&	flask init-db
