

.PHONY: install
install:
	poetry install

.PHONY: run
run:
	poetry run python -m djinn.manage runserver

.PHONY: migrations
migrations:
	poetry run python -m djinn.manage makemigrations

.PHONY: migrate
migrate:
	poetry run python -m djinn.manage migrate

.PHONY: superuser
superuser:
	poetry run python -m djinn.manage createsuperuser

.PHONY: generate
generate:
	python djinn/code_generator/cli.py generate 

.PHONY: check
check:
	poetry run ruff check .

.PHONY: format
format:
	poetry run ruff format .

.PHONY: fix
fix:
	poetry run ruff check --fix .

.PHONY: update
update: install migrate ;
	