SHELL:=/bin/bash

include .env

#
#   CONFIGURABLE VARIABLES
#

#
#	Project name is propagated to the ECS cluster and it is use to ensure we dont accidentally change the wrong live service
#
#
export PROJECT_NAME										:= deep

#
#	allows containers to have make targets locally that are not in this makefile.
#

export CONTAINER_TARGETS_WHITELIST						:= refresh


#
#   AUTOMATED CONSTANTS
#
export DOCKER_COMPOSE_VERSION							:= 2
export TIMESTAMP										:= $(shell date +%s)
export PROJECT_PATH										:= $(abspath $(lastword $(MAKEFILE_LIST)))
export PROJECT_FOLDER									:= $(notdir $(patsubst %/,%,$(dir $(PROJECT_PATH))))
export CONTAINERS										:= $(dir $(wildcard containers/*/))
export COMPOSE_PROJECT_NAME								:= ${PROJECT_NAME}
export WORD_COUNT										:= $(words $(MAKECMDGOALS))
export ALL_ARGS											:= $(wordlist 1, ${WORD_COUNT}, $(MAKECMDGOALS) )
export ARGS_0											:= $(word 1, $(ALL_ARGS))
export ENV												:= dev

export TAG												:= ${shell date | md5 | cut -c27-}
export FASTAI											:= .fastai
export DOCKER_REPO										:= musedivision

.PHONY: $(CONTAINERS) $(CONTAINER_TARGETS_WHITELIST) build clean deploy all
.SILENT: $(CONTAINERS) $(CONTAINER_TARGETS_WHITELIST) all
.ONESHELL:

#
# This is the first and default recipie.  typing make  or make all will run
# it causing you to switch to this aws region and this projects credentials
#
all: /usr/local/bin/docker-compose


$(CONTAINERS):
	@cd $@ && $(MAKE) $(CMD) || true

$(CONTAINER_TARGETS_WHITELIST):
	$(MAKE) $(CONTAINERS) CMD=$(ARGS_0)

deploy:
	@$(MAKE) $(CONTAINERS) CMD=deploy

build: ${FASTAI}
	docker-compose down || true
	@$(MAKE) $(CONTAINERS) CMD=build
	$(MAKE) docker-compose.override.yml
	docker-compose up -d

stop:
	docker-compose down

clean:
	rm -f docker-compose.override.yml
	@$(MAKE) $(CONTAINERS) CMD=clean
	docker rmi $(docker images | grep "^<none>" | awk '{print $3}') || true

nuke:
	rm -rf ./.fastai

${FASTAI}:
	git clone https://github.com/fastai/fastai.git ./.fastai
	cp ./.fastai/environment.yml ./containers/example/src/.

/usr/local/bin/docker-compose:
	sudo curl -L https://github.com/docker/compose/releases/download/1.19.0/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
	sudo chmod +x /usr/local/bin/docker-compose
	docker-compose --version

#
#
#	SPECIAL RECIPIES
#
#

docker-compose.override.yml:
	@touch docker-compose.override.yml
	@echo version: '"$(DOCKER_COMPOSE_VERSION)"' >> docker-compose.override.yml
	@echo services: >> docker-compose.override.yml
	@$(MAKE) $(CONTAINERS) CMD=compile >> docker-compose.override.yml


