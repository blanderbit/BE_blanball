FROM nginx:latest

RUN apt-get update && apt-get install -y gettext-base

COPY ./nginx/nginx.conf.template /etc/nginx/nginx.conf.template
COPY ./nginx/nginx_proxy.conf.template /etc/nginx/conf.d/default.conf.template
COPY ./entrypoint.sh /usr/local/bin/entrypoint.sh

RUN chmod +x /usr/local/bin/entrypoint.sh

CMD ["/usr/local/bin/entrypoint.sh"]