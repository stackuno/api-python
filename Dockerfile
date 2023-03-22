ARG BASE_IMAGE=python:3.10.10-slim-buster

FROM ${BASE_IMAGE} AS dev

# Install system dependencies
ARG SYSTEM_PACKAGES=""
RUN set -x; apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    ca-certificates \
    curl \
    ${SYSTEM_PACKAGES} \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry to $POETRY_HOME and allow all users to execute Poetry binaries
# https://python-poetry.org/docs/#introduction
ENV POETRY_HOME=/opt/poetry
ARG POETRY_VERSION=1.4.0
RUN set -x; \
    python -m venv ${POETRY_HOME} && \
    ${POETRY_HOME}/bin/pip install poetry==${POETRY_VERSION} && \
    ${POETRY_HOME}/bin/poetry --version && \
    chmod -R a+rwx ${POETRY_HOME}

ENV PATH="/opt/poetry/bin:$PATH"


FROM ${BASE_IMAGE} AS build

# Define environment vars for venv and initialize a venv
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN set -x; python -m venv $VIRTUAL_ENV

ARG PIP_ORIGIN=https://pypi.org/simple
ARG PIP_VERSION=23.0.1
RUN set -x; pip install \
  --index-url ${PIP_ORIGIN} \
  --upgrade pip==${PIP_VERSION}

COPY . /opt/${PROJECT}
WORKDIR /opt/${PROJECT}

# Copy Poetry from dev stage
COPY --from=dev /opt/poetry /opt/poetry
ENV PATH="/opt/poetry/bin:$PATH"

# Install Python packages without dev dependencies
ARG PACKAGE_INSTALLER="poetry install --no-dev"
RUN set -x; ${PACKAGE_INSTALLER}


FROM ${BASE_IMAGE}

# Provision a non-root user
ARG GID=20000
ARG UID=20000
ARG GECOS=",,,,"
RUN set -x; \
  addgroup \
    --gid ${GID} \
    appgroup \
  && \
  adduser \
    --no-create-home \
    --uid ${UID} \
    --gecos ${GECOS} \
    --gid ${GID} \
    --disabled-password \
    --disabled-login \
    appuser \
  && \
  > /var/log/faillog && > /var/log/lastlog
USER ${UID}:${GID}

# Copy venv from build image
COPY --chown=${UID}:${GID} --from=build /opt/venv /opt/venv

# Configure venv paths
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

ARG PROJECT=app
ENV PROJECT $PROJECT
WORKDIR /opt/${PROJECT}

COPY --chown=${UID}:${GID} . /opt/${PROJECT}

ARG PORTS=8000
EXPOSE ${PORTS}

ENTRYPOINT ["uvicorn", "app:api"]
CMD ["--host", "0.0.0.0"]
