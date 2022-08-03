FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/blanball

RUN /usr/local/bin/python -m pip install --upgrade pip

COPY req.txt /usr/src/blanball/

RUN pip install -r  req.txt

COPY . /usr/src/blanball

# RUN python /usr/src/blanball/project/manage.py makemigrations
# RUN python /usr/src/blanball/project/manage.py migrate