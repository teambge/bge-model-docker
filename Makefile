.PHONY: login build push run debug clean

REPO ?= teambge
PY_VERSIONS := python3.6 python2.7
SOURCE_DIR := ./dockerfiles
PREFIX := model-
IMAGE_NAME := $(REPO)/$(if $(filter $(ENVIRONMENT),build),$(PREFIX)$(PY_VERSION):latest,$(ENVIRONMENT)-$(PREFIX)$(PY_VERSION):latest)

py_version_check:
ifndef PY_VERSION
	$(error PY_VERSION is undefined)
endif


environment_check:
ifndef ENVIRONMENT
	$(error ENVIRONMENT is undefined)
endif


login:
	@if [ -n "$(DOCKER_USERNAME)" ] && [ -n "$(DOCKER_PASSWORD)" ]; then \
		echo $(DOCKER_PASSWORD) | docker login -u $(DOCKER_USERNAME) --password-stdin; \
	else \
		echo "The arguments DOCKER_USERNAME and DOCKER_PASSWORD is required for docker login."; \
	fi


build: environment_check
	@if [ -n "$(PY_VERSION)" ]; then \
		echo 'docker build -f "$(SOURCE_DIR)/$(PY_VERSION)/$(ENVIRONMENT)/Dockerfile" -t "$(IMAGE_NAME)" . '; \
		docker build -f "$(SOURCE_DIR)/$(PY_VERSION)/$(ENVIRONMENT)/Dockerfile" -t "$(IMAGE_NAME)" . ; \
	else \
		for PY_VERSION in $(PY_VERSIONS); do \
			make build PY_VERSION=$$PY_VERSION ENVIRONMENT=$(ENVIRONMENT) || exit 1; \
		done \
	fi


push: environment_check login
	@if [ -n "$(PY_VERSION)" ]; then \
		echo "docker push $(IMAGE_NAME)"; \
		docker push $(IMAGE_NAME); \
	else \
		for PY_VERSION in $(PY_VERSIONS); do \
			make push PY_VERSION=$$PY_VERSION ENVIRONMENT=$(ENVIRONMENT) || exit 1; \
		done \
	fi


run: py_version_check environment_check
	docker run -it --rm $(IMAGE_NAME) /bin/bash


debug: py_version_check environment_check
	docker create --name=debug -it $(IMAGE_NAME) /bin/bash \
		&& docker start debug \
		&& docker exec -it -u root debug /bin/bash


clean:
	docker image prune
