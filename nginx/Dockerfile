FROM nginx:latest
RUN ls -l 
COPY ./nginx/nginx.conf /etc/nginx/nginx.conf
COPY ./nginx/my_nginx.conf /etc/nginx/sites-available/

RUN mkdir -p /etc/nginx/sites-enabled/\
    && ln -s /etc/nginx/sites-available/my_nginx.conf /etc/nginx/sites-enabled/\
    && rm /etc/nginx/conf.d/default.conf

CMD ["nginx", "-g", "daemon off;"]