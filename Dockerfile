# Arguments:
# NAME: name of the container
# DOMAIN: domain of the container
# GRAPHITE_HOST: the ip of the graphite server
# SQL_HOST: the ip of the mysql server
# SQL_USERNAME: the username of the mysql server
# SQL_PASSWORD: the password of the mysql server

FROM php:7.2-fpm-alpine
MAINTAINER Harry Yu <harryyunull@gmail.com>

# Install needed softwares
RUN mkdir -p /usr/share/man/man1

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories &&\
    apk update && apk upgrade && apk add libxml2-dev && \
    docker-php-ext-install soap && \ 
    docker-php-ext-install mysqli && docker-php-ext-enable mysqli

# Configuration
ENV NAME ""
ENV GRAPHITE_HOST ""
ENV GRAPHITE_PORT 8125
ENV SQL_HOST ""
ENV SQL_USERNAME ""
ENV SQL_PASSWORD ""

# Enable compression & Disable warnings & Write errors to docker logs
RUN echo "zlib.output_compression = 1" > /usr/local/etc/php/php.ini &&\
    echo "display_errors=Off" >> /usr/local/etc/php/php.ini &&\
    echo "log_errors = On" >> /usr/local/etc/php/php.ini &&\
    echo "error_log = /dev/stderr" >> /usr/local/etc/php/php.ini

# Copy application
RUN mkdir /etc/conf.d/php.d/

EXPOSE 9000