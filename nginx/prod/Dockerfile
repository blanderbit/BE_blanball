FROM nginx:latest
COPY ./nginx/prod/nginx.conf /etc/nginx/nginx.conf
COPY ./nginx/prod/nginx_proxy.conf /etc/nginx/conf.d/default.conf

CMD ["nginx", "-g", "daemon off;"]