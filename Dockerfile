FROM python:3.10

# `DJANGO_ENV` arg is used to make prod / dev builds:
ARG DJANGO_ENV \
  # Needed for fixing permissions of files created by Docker:
  UID=1000 \
  GID=1000

ENV DEBUG=true \
  APP_PATH='/usr/src/blanball' \
  # python:
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PYTHONDONTWRITEBYTECODE=1 \
  # pip:
  PIP_NO_CACHE_DIR=1 \
  PIP_DISABLE_PIP_VERSION_CHECK=1 \
  PIP_ROOT_USER_ACTION=ignore \
  PIP_DEFAULT_TIMEOUT=100 \
  #poetry 
  POETRY_VERSION=1.2.0 \
  POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry' \
  POETRY_HOME='/usr/local'

WORKDIR $APP_PATH

COPY ./poetry.lock ./pyproject.toml $APP_PATH/

COPY ./compose/local/  $APP_PATH/project/

RUN if [ "$DEBUG" = 'true' ]; then apt-get update && apt-get upgrade -y \
  && apt-get install --no-install-recommends -y \
  && groupadd -g "${GID}" -r web \
  && useradd -d $APP_PATH -g web -l -r -u "${UID}" web \
  && chown web:web -R $APP_PATH; fi

RUN pip install --upgrade pip\
  &&pip install poetry=="$POETRY_VERSION" 

ENV PATH "/root/.poetry/bin:/opt/venv/bin:${PATH}"

# Cleaning cache:
RUN apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && apt-get clean -y && rm -rf /var/lib/apt/lists/* \
    && poetry version 
    #Install deps:
RUN target="$POETRY_CACHE_DIR" \
    &&poetry run pip install -U pip \
    &&poetry install \
      $(if [ "$DEBUG" = 'true' ]; then echo '--no-root --only main'; fi) \
      --no-interaction --no-ansi

COPY . $APP_PATH
