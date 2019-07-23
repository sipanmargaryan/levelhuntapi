RUN=docker-compose run --rm partial

all:
	docker-compose build

extract:
	docker-compose run --rm packages cp -r  /usr/local/lib/python3.6/dist-packages /host

run:
	docker-compose run --service-ports --rm partial

run-all:
	docker-compose up project

shell:
	$(RUN) /bin/bash

migrate:
	$(RUN) python3 manage.py migrate

test:
	$(RUN) pytest -x -vvv --pdb

report:
	$(RUN) pytest --cov=apps/ -x --pdb

report-html:
	$(RUN) pytest --cov-report html --cov=apps/ -x --pdb

sort:
	$(RUN) isort --recursive apps project

check-sort:
	$(RUN) isort --recursive --diff apps project

stop:
	docker-compose down