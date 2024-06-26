

.PHONY: install
install:
	poetry install

.PHONY: run
run:
	poetry run python -m {{cookiecutter.package_name}}.manage runserver

.PHONY: migrations
migrations:
	poetry run python -m {{cookiecutter.package_name}}.manage makemigrations

.PHONY: migrate
migrate:
	poetry run python -m {{cookiecutter.package_name}}.manage migrate

.PHONY: superuser
superuser:
	poetry run python -m {{cookiecutter.package_name}}.manage createsuperuser

.PHONY: install-pre-commit
install-pre-commit:
	poetry run pre-commit uninstall; poetry run pre-commit install

.PHONY: lint
lint:
	poetry run pre-commit run --all-files


.PHONY: generate
generate:
	python {{cookiecutter.package_name}}/code_generator/cli.py generate 

.PHONY: check
check:
	poetry run ruff check .

.PHONY: format
format:
	poetry run ruff format .

.PHONY: fix
fix:
	poetry run ruff check --fix .

.PHONY: run-dependencies
run-dependencies:
	test -f .env || touch .env
	docker-compose -f docker-compose.dev.yml up --force-recreate db redis

.PHONY: test
test:
	poetry run pytest -v -rs -n auto --show-capture=all

.PHONY: update
update: install migrate ;
	

.PHONY: git-noverify
git-noverify:
	git add .
	git commit --no-verify -m "cookiecutter"
	git push 
