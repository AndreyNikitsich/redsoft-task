.PHONY: clean, up, down, stop, env

env:
	@cp .env.example .env

stop:
	- docker compose stop

down:
	- docker compose down

clean:
	- docker compose down -v || true
	- docker ps -q | xargs -r docker stop || true
	- docker ps -a -q | xargs -r docker rm || true
	- docker volume ls -q | xargs -r docker volume rm || true

up: env
	@docker compose up --build
