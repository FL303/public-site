FROM klakegg/hugo:0.101.0-ext-alpine as build

ARG env=staging

COPY ./ /site
WORKDIR /site
RUN hugo --environment $env

#Copy static files to Nginx
FROM nginx:1.25.3-alpine3.18
COPY --from=build /site/public /usr/share/nginx/html
COPY default.conf /etc/nginx/conf.d/default.conf

WORKDIR /usr/share/nginx/html