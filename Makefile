

.PHONY: install
install:
	poetry install


.PHONY: install-pre-commit
install-pre-commit:
	poetry run pre-commit uninstall; poetry run pre-commit install

.PHONY: git-noverify
git-noverify:
	git add .
	git commit --no-verify -m "cookiecutter"
	git push 
