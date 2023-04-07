FROM nginx:latest
COPY ./nginx/test/nginx.conf /etc/nginx/nginx.conf
COPY ./nginx/test/nginx_proxy.conf /etc/nginx/conf.d/default.conf

CMD ["nginx", "-g", "daemon off;"]