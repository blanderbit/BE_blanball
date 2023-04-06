FROM nginx:latest

RUN apt-get update && apt-get install -y gettext-base

COPY ./nginx/nginx.conf /etc/nginx/nginx.conf
COPY ./nginx/nginx_proxy.conf /etc/nginx/conf.d/default.conf
COPY ./scripts/proxy_entrypoint.sh /usr/local/bin/proxy_entrypoint.sh

RUN chmod +x /usr/local/bin/proxy_entrypoint.sh

CMD ["/usr/local/bin/proxy_entrypoint.sh"]