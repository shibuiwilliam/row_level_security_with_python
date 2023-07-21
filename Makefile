DIR := $(shell pwd)
VERSION := $(shell cd ${DIR} && poetry version -s)

DOCKER_REPOSITORY := shibui/row_level_security_with_python
DOCKERFILE := Dockerfile
DOCKER_IMAGE_NAME = $(DOCKER_REPOSITORY):$(VERSION)
DOCKER_COMPOSE := docker-compose.yaml

############ COMMON COMMANDS ############
SRC := $(DIR)/src

.PHONY: spell_check
spell_check:
	codespell --toml pyproject.toml

.PHONY: lint
lint: spell_check
	black --check --diff --line-length 120 $(SRC)

.PHONY: sort
sort:
	isort $(SRC)

.PHONY: fmt
fmt: sort
	black --line-length 120 $(SRC)

.PHONY: req
req:
	poetry export \
		--without-hashes \
		-f requirements.txt \
		--output requirements.txt

.PHONY: req_dev
req_dev:
	poetry export \
		--with dev \
		--without-hashes \
		-f requirements.txt \
		--output requirements_dev.txt

.PHONY: req_all
req_all: req req_dev

.PHONY: install_dep
install_dep:
	pip install -r requirements.txt

.PHONY: install_dep_dev
install_dep_dev:
	pip install -r requirements_dev.txt

.PHONY: install_deps
install_deps: install_dep install_dep_dev

.PHONY: build
build:
	docker build \
		--platform linux/amd64 \
		--build-arg FROM_IMAGE=python:3.11.3-slim \
		-t $(DOCKER_IMAGE_NAME) \
		-f $(DOCKERFILE) \
		.

.PHONY: up
up:
	docker-compose \
		-f $(DOCKER_COMPOSE) \
		up -d

.PHONY: down
down:
	docker-compose \
		-f $(DOCKER_COMPOSE) \
		down
