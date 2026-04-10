FROM nginx:1.27-alpine

COPY html/ /usr/share/nginx/html/
COPY css/ /usr/share/nginx/html/css/
COPY javascript/ /usr/share/nginx/html/javascript/
COPY favicon.svg /usr/share/nginx/html/favicon.svg
COPY nginx/default.conf /etc/nginx/conf.d/default.conf

RUN rm -f /usr/share/nginx/html/index.html \
    && cp /usr/share/nginx/html/main.html /usr/share/nginx/html/index.html

EXPOSE 80
