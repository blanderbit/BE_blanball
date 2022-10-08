FROM nginx:latest
# RUN ls -l 
COPY ./nginx/nginx.conf /etc/nginx/nginx.conf
# COPY ./nginx/my_nginx.conf /etc/nginx/sites-available/
COPY ./nginx/nginx_proxy.conf /etc/nginx/conf.d/default.conf

# RUN mkdir -p /etc/nginx/sites-enabled/\
#     && ln -s /etc/nginx/sites-available/my_nginx.conf /etc/nginx/sites-enabled/\
#     && rm /etc/nginx/conf.d/default.conf

CMD ["nginx", "-g", "daemon off;"]