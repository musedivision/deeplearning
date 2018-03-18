NO_PROJECT_NAME=local
NO_TAG_NAME=DO_NOT_DEPLOY
NO_REPO_NAME=LOCALDEV
COMPOSE_PROJECT_NAME := $(if $(COMPOSE_PROJECT_NAME),$(COMPOSE_PROJECT_NAME),$(NO_PROJECT_NAME))
TAG := $(if $(TAG),$(TAG),$(NO_TAG_NAME))
ECR_REPO_URL := $(if $(ECR_REPO_URL),$(ECR_REPO_URL),$(NO_REPO_NAME))

export PROJECT_NAME := 		:= ${COMPOSE_PROJECT_NAME}
export CONTAINER_PATH       := $(abspath $(lastword $(MAKEFILE_LIST)))
export CONTAINER_REL_PATH   := $(notdir $(patsubst %/,%,$(dir $(CONTAINER_PATH))))
export CONTAINER_NAME       := ${CONTAINER_REL_PATH}

ENV:=dev
IMAGE_NAME=${COMPOSE_PROJECT_NAME}_${CONTAINER_NAME}

.ONESHELL:
.PHONY: test

all:
	  #do config here


clean:
	docker rm -f ${CONTAINER_NAME} || true
	docker rmi -f $$(docker images --filter='reference=${CONTAINER_NAME}' -a -q) || true
	docker rmi -f $$(docker images --filter='reference=${DOCKER_REPO}/${CONTAINER_NAME}' -a -q) || true

build:
	docker build . -t ${IMAGE_NAME}:latest

deploy:
	docker tag ${IMAGE_NAME}:latest ${DOCKER_REPO}/${IMAGE_NAME}
	docker push ${DOCKER_REPO}/${IMAGE_NAME}

# provide the ENV=live to compile the live docker compose branch
compile:
	@cat docker-compose.${ENV}.yml | sed 's/CONTAINER_NAME/${CONTAINER_NAME}/g' | sed 's/CONTAINER_REL_PATH/${CONTAINER_REL_PATH}/g'


# IMPORTANT NOTE:
#
#   IF YOU MUST CHANGE THIS FILE DO SO BELOW THIS LINE AND COMMENT OUT ( DO NOT REMOVE ) ABOVE AND DUPLICATE BELOW
#   WITH YOUR CHANGES.

refresh:
	docker exec ${CONTAINER_NAME} pm2 restart 0 &