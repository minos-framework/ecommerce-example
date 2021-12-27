build:
	docker compose build --progress plain

up: build
	echo "Starting containers..."
	docker compose up --detach

down:
	echo "Stopping containers..."
	docker compose down --remove-orphans

logs:
	echo "Showing logs..."
	docker compose logs --follow

export-logs:
	echo "Showing logs..."
	docker compose logs --no-color > logs.txt

integration-tests:
	echo "Running Integration Tests..."
	docker compose run tavern