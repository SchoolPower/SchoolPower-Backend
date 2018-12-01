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
ENV SQL_HOST ""
ENV SQL_USERNAME ""
ENV SQL_PASSWORD ""

# Enable compression & Disable warnings
RUN echo "zlib.output_compression = 1" > /usr/local/etc/php/php.ini &&\
    echo "display_errors=Off" >> /usr/local/etc/php/php.ini
    
# Copy application
COPY src /var/www/html/api/2.0/
COPY common /var/www/html/api/common/
COPY notifications /var/www/html/api/notifications/
COPY dist/latest.php /var/www/html/dist/latest.php
RUN echo "<?php header('Content-type: application/json'); echo file_get_contents('https://files.schoolpower.tech/update.json');" > /var/www/html/api/update.json.php
RUN sed -i "s/127\.0\.0\.1/${SQL_HOST}/g" /var/www/html/api/common/db.php
RUN sed -i "s/\"SQL_USERNAME\"\, \"root\"/\"SQL_USERNAME\", \"${SQL_USERNAME}\"/g" /var/www/html/api/common/db.php
RUN sed -i "s/\"SQL_PASSWORD\"\, \"\"/\"SQL_PASSWORD\", \"${SQL_PASSWORD}\"/g" /var/www/html/api/common/db.php
RUN sed -i "s/SERVERNAME/${NAME}/g" /var/www/html/api/2.0/get_data.php
RUN sed -i "s/localhost/${GRAPHITE_HOST}/g" /var/www/html/api/2.0/get_data.php

EXPOSE 9000