#!/bin/bash
set -e

envsubst < /etc/nginx/nginx.conf.template > /etc/nginx/nginx.conf
envsubst < /etc/nginx/conf.d/default.conf.template > /etc/nginx/conf.d/default.conf

nginx -g 'daemon off;'