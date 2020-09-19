.PHONY: help
help: ## Shows this help command
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

driver:
	curl https://chromedriver.storage.googleapis.com/2.31/chromedriver_linux64.zip -o /usr/local/bin/chromedriver
	chmod +x /usr/local/bin/chromedriver

test: ## Runs unit tests
	#rm ./mounts/database/newsbot.db
	alembic upgrade head
	pytest
	rm ./mounts/database/newsbot.db

refresh: ## Removes temp data for a clean start
	rm ./mounts/database/newsbot.db

rmdatabase:
	rm ./mounts/database/newsbot.db

docker-build: ## Build docker image
	docker build -t newsbot .

demo: ## Runs the application
	docker-compose up

freeze: ## Exports all installed python packages to the requirements.txt
	pip3 freeze > requirements.txt