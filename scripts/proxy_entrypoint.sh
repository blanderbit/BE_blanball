#!/bin/bash
set -e

envsubst < /etc/nginx/nginx.conf > /etc/nginx/nginx.conf
envsubst < /etc/nginx/conf.d/default.conf > /etc/nginx/conf.d/default.conf

nginx -g 'daemon off;'