SHELL = /bin/sh

DOCKER ?= docker
GIT ?= git
MKDIR ?= mkdir -p
RM = rm -rf

PORT ?= 3000

# Include the private.mk file (if it exists) to setup private parameters
-include .private.mk

include parameters.mk

# Spawn temporary dev files
$(workdir)/.homedir:
$(workdir)/.venv:
	$(MKDIR) \
		$(workdir)/.homedir \
		$(workdir)/.venv

# Build the dev Docker image
.PHONY: image/dev
image/dev: Dockerfile
	$(DOCKER) build \
		$(DOCKER_BUILD_ARGS) \
		--rm \
		--target=dev \
		--tag=$(DOCKER_IMAGE_NAME):dev \
		$(srcdir)

.PHONY: image
image: Dockerfile
	$(DOCKER) build \
		$(DOCKER_BUILD_ARGS) \
		--rm \
		--tag=$(DOCKER_IMAGE_NAME) \
		$(srcdir)

# Spawn a Bash shell
.PHONY: bash
bash: $(srcdir) $(workdir)/.homedir $(workdir)/.venv
	@$(DOCKER) run \
		$(DOCKER_ARGS) \
		--net=host \
		--name "${PROJECT_NAME}-dev" \
		--rm -it \
		--entrypoint=bash \
		$(DOCKER_IMAGE_NAME):dev

# Spawn server
.PHONY: server
server:
	$(DOCKER) run \
		$(DOCKER_BASE_ARGS) \
		-p $(DOCKER_HOST_ADDRESS):${PORT}:${PORT}/tcp \
		--name "${PROJECT_NAME}-server" \
		--rm -it \
		$(DOCKER_IMAGE_NAME) \
		--reload --host 0.0.0.0 --port ${PORT} --log-level debug \

# Clear local cache and venv directories
.PHONY: clean
clean: $(workdir)
	$(RM) \
		$(workdir)/.venv
