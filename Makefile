APP_NAME="neuromorphic-sprint-three"
IMAGE_NAME="eduardomatoss/neuromorphic-sprint-three"
VERSION="latest"
UNAME_S := $(shell uname -s)
ifeq ($(UNAME_S),Linux)
    DOCKER_USER=$(shell id -u $(USER)):$(shell id -g $(USER))
endif
ifeq ($(UNAME_S),Darwin)
    DOCKER_USER=
endif

local/install: generate-default-env-file
	pipenv install --dev --skip-lock

local/lint:
	black --check app/
	flake8 app/

local/lint/fix:
	black app/

local/check-packages:
	pipenv check --system -e PIPENV_PYUP_API_KEY=""

local/bandit:
	bandit -r . app *.py

local/shell:
	pipenv shell

local/test:
	ENV_FOR_DYNACONF=test python -m pytest -s -c tests/pytest.ini \
	--pyargs ./tests -v --junitxml=results.xml \
	--cov-fail-under 50 --cov-report xml \
	--cov-report term \
	--cov-report html --cov ./app

local/run:
	python run.py


docker/build: generate-default-env-file
	CURRENT_UID=${DOCKER_USER} docker-compose build ${APP_NAME}

docker/up:
	CURRENT_UID=${DOCKER_USER} docker-compose up -d

docker/postgres/up:
	CURRENT_UID=${DOCKER_USER} docker-compose up -d postgres-db

docker/down:
	CURRENT_UID=${DOCKER_USER} docker-compose down --remove-orphans

docker/lint:
	CURRENT_UID=${DOCKER_USER} docker-compose run ${APP_NAME} black --check app/
	CURRENT_UID=${DOCKER_USER} docker-compose run ${APP_NAME} flake8 app/

docker/lint/fix:
	docker-compose run ${APP_NAME} run black app/

docker/check-packages:
	CURRENT_UID=${DOCKER_USER} docker-compose run -e PIPENV_PYUP_API_KEY="" ${APP_NAME} pipenv check --system

docker/bandit:
	CURRENT_UID=${DOCKER_USER} docker-compose run ${APP_NAME} bandit -r . app *.py

docker/verify:
	make docker/lint
	make docker/bandit

docker/test:
	CURRENT_UID=${DOCKER_USER} docker-compose run -e ENV_FOR_DYNACONF=test ${APP_NAME} \
	python -m pytest -s -c tests/pytest.ini \
	--pyargs ./tests -v  \
	--cov-fail-under 50 --cov-report xml \
	--cov-report term \
	--cov-report html --cov ./app

docker/run:
	CURRENT_UID=${DOCKER_USER} docker-compose run --service-port ${APP_NAME} python run.py

docker/migrations/generate:
	CURRENT_UID=${DOCKER_USER} docker-compose run ${APP_NAME} alembic revision --autogenerate

docker/migrations/upgrade:
	CURRENT_UID=${DOCKER_USER} docker-compose run ${APP_NAME} alembic upgrade head

image/build:
	docker build . --target production -t ${IMAGE_NAME}:${VERSION}

image/push:
	docker push ${IMAGE_NAME}:${VERSION}

generate-default-env-file:
	@if [ ! -f .env ]; then cp env.template .env; fi;
