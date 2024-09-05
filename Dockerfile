FROM tiangolo/uwsgi-nginx-flask:latest

ENV STATIC_URL /static

ENV STATIC_PATH /var/www/app/static

COPY ./requirements.txt /var/www/requirements.txt

COPY . /var/www/app

RUN pip install -r /var/www/requirements.txt