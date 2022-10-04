sudo apt install nginx

cp nginx.conf /etc/nginx/nginx.conf
cp my_nginx.conf /etc/nginx/sites-available/

mkdir -p /etc/nginx/sites-enabled/
ln -s /etc/nginx/sites-available/my_nginx.conf /etc/nginx/sites-enabled/
rm /etc/nginx/conf.d/default.conf

nginx -g 'daemon off;'