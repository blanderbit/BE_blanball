#!/bin/bash
set -e

envsubst < /etc/nginx/nginx.conf > /etc/nginx/nginx.conf
envsubst < /etc/nginx/nginx_proxy.conf > /etc/nginx/conf.d/default.conf

nginx -g 'daemon off;'