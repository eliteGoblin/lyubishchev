
export WORKON_HOME=$HOME/.virtualenvs
export PROJECT_HOME=$HOME/devel

# Execute the program.
PHONY: run
run:
	docker volume create timescaledb-storage
	docker volume create grafana-storage
	docker-compose up

.PHONY: down
down:
	docker-compose down

SHELL := /bin/bash

.PHONY: ingest-test
ingest-test:
	./lyubishchev/data_ingest/ingest.py --start-date=2021-11-15 --end-date=2021-11-21

PHONY: ingest-days
ingest-days:
	./lyubishchev/data_ingest/ingest.py --offset-days=4

PHONY: ingest-last-fortnight
ingest-last-fortnight:
	./lyubishchev/data_ingest/ingest.py --offset-days=14

.PHONY: clean-db
clean-db:
	docker-compose down
	-rm ./lyubishchev/data_ingest/latest_timestamp.txt
	-docker volume rm timescaledb-storage 
