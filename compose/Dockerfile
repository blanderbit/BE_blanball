# syntax=docker/dockerfile:1.4
FROM python:3.10

ENV DJANGO_ENV=${DJANGO_ENV} \
  # python:
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PYTHONDONTWRITEBYTECODE=1 \
  # pip:
  PIP_NO_CACHE_DIR=1 \
  PIP_DISABLE_PIP_VERSION_CHECK=1 \
  PIP_DEFAULT_TIMEOUT=100 \
  #poetry 
  POETRY_VERSION=1.2.0 \
  POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry' \
  POETRY_HOME='/usr/local'


VOLUME /db-data

WORKDIR /usr/src/blanball

COPY . /usr/src/blanball

RUN pip install --upgrade pip\
  &&pip install poetry=="$POETRY_VERSION"

ENV PATH "/root/.poetry/bin:/opt/venv/bin:${PATH}"
# Cleaning cache:
RUN apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && apt-get clean -y && rm -rf /var/lib/apt/lists/* \


# RUN poetry run pip install -U pip \
#     && poetry install

  && echo "$DJANGO_ENV" \
  && poetry version \
  #Install deps:
  &&poetry run pip install -U pip \
  &&poetry install 
