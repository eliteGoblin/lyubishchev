# Execute the program.
PHONY: run
run:
	docker volume create timescaledb-storage
	docker volume create grafana-storage
	docker-compose up

PHONY: down
down:
	docker-compose down

.PHONY: clean-db
clean-db:
	# docker-compose down
	# -docker volume rm timescaledb-storage 
	# -rm ./data_ingest/latest_timestamp.txt