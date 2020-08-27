.PHONY: help
help: ## Shows this help command
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

unittest: ## Runs unit tests
	mv ./mounts/database/newsbot.db ./mounts/database/newsbot.db.1
	alembic upgrade head
	pytest
	rm ./mounts/database/newsbot.db
	mv ./mounts/database/newsbot.db.1 ./mounts/database/newsbot.db

build: ## Build docker image
	docker build -t newsbot .

demo: ## Runs the application
	docker-compose up

freeze: ## Exports all installed python packages to the requirements.txt
	pip3 freeze > requirements.txt