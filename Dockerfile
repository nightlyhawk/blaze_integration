FROM nginx:1.25

RUN rm /etc/nginx/conf.d/default.conf
COPY default.conf /etc/nginx/conf.d
COPY dhparam /etc/nginx/dhparam
COPY certbot/conf /etc/nginx/ssl
COPY certbot/data /usr/share/nginx/html/letsencrypt
