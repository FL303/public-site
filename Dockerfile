FROM hugomods/hugo:exts-0.136.4 AS build

ARG env=staging

COPY ./ /site
WORKDIR /site
RUN hugo --environment $env

#Copy static files to Nginx
FROM nginx:1.25.4-alpine3.18
COPY --from=build /site/public /usr/share/nginx/html
COPY default.conf /etc/nginx/conf.d/default.conf

WORKDIR /usr/share/nginx/html