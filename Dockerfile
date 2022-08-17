FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/blanball

COPY . /usr/src/blanball

RUN /usr/local/bin/python -m pip install --upgrade pip

RUN pip install -r  req.txt

EXPOSE 8000
