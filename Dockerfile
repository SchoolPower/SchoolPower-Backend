# Arguments:
# NAME: name of the container
# DOMAIN: domain of the container
# GRAPHITE_HOST: the ip of the graphite server
# SQL_HOST: the ip of the mysql server
# SQL_USERNAME: the username of the mysql server
# SQL_PASSWORD: the password of the mysql server
# Volumes:
# /etc/letsencrypt/live/ : fullchain.pem/privkey.pem

FROM php:7.0-apache
MAINTAINER Harry Yu <harryyunull@gmail.com>

# Install needed softwares
RUN mkdir -p /usr/share/man/man1

RUN echo "deb http://ftp2.cn.debian.org/debian/ stretch main" > /etc/apt/sources.list && \
    echo "deb http://ftp2.cn.debian.org/debian/ stretch-updates main" >> /etc/apt/sources.list && \
    echo "deb http://mirrors.tuna.tsinghua.edu.cn/debian-security/ stretch/updates main" >> /etc/apt/sources.list && \
    apt-get update && apt-get upgrade -y && \
    apt-get install -q -y collectd libxml2-dev software-properties-common && \
    docker-php-ext-install soap && \ 
    docker-php-ext-install mysqli && docker-php-ext-enable mysqli
RUN add-apt-repository ppa:certbot/certbot && \
    apt-get install -q -y python-certbot-apache && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Configuration
ARG NAME
ARG GRAPHITE_HOST
ARG DOMAIN
ARG SQL_HOST
ARG SQL_USERNAME
ARG SQL_PASSWORD
ARG HTTP_ONLY=false

# First copy them all
COPY conf/schoolpower-api-http.conf /etc/apache2/sites-enabled/
COPY conf/schoolpower-api.conf /etc/apache2/sites-enabled/
COPY conf/schoolpower-api-ssl.conf /etc/apache2/sites-enabled/
RUN rm /etc/apache2/sites-enabled/000-default.conf &&\
    sed -i "s/DOMAIN_PLACEHOLDER/${DOMAIN}/g" /etc/apache2/sites-enabled/schoolpower-api.conf &&\
    sed -i "s/DOMAIN_PLACEHOLDER/${DOMAIN}/g" /etc/apache2/sites-enabled/schoolpower-api-ssl.conf &&\
    sed -i "s/DOMAIN_PLACEHOLDER/${DOMAIN}/g" /etc/apache2/sites-enabled/schoolpower-api-http.conf
    
# Then adjust apache configuration according to "HTTP_ONLY"
RUN if [ "${HTTP_ONLY}" = "true" ]; then rm /etc/apache2/sites-enabled/schoolpower-api.conf &&\
    rm /etc/apache2/sites-enabled/schoolpower-api-ssl.conf;\
    else rm /etc/apache2/sites-enabled/schoolpower-api-http.conf; fi
    
RUN echo "ExtendedStatus on" >> /etc/apache2/apache2.conf &&\
    echo "<Location /mod_status>" >> /etc/apache2/apache2.conf &&\
    echo "  SetHandler server-status" >> /etc/apache2/apache2.conf &&\
    echo "  Deny from all" >> /etc/apache2/apache2.conf &&\
    echo "  Allow from localhost ip6-localhost" >> /etc/apache2/apache2.conf &&\
    echo "</Location>" >> /etc/apache2/apache2.conf
RUN echo "zlib.output_compression = 1" > php.ini # Enable compression
RUN a2enmod rewrite
RUN a2enmod ssl
RUN a2enmod http2
RUN a2enmod proxy
RUN a2enmod proxy_http
VOLUME /etc/letsencrypt/live/
RUN cp /usr/lib/python2.7/dist-packages/certbot_apache/options-ssl-apache.conf /etc/letsencrypt/

# Configure collectd
COPY conf/collectd.conf /etc/collectd/collectd.conf
RUN sed -i "s/HOSTNAME_PLACEHOLDER/${NAME}/g" /etc/collectd/collectd.conf
RUN sed -i "s/GRAPHITE_HOST_PLACEHOLDER/${GRAPHITE_HOST}/g" /etc/collectd/collectd.conf

# Copy application
COPY 2.0 /var/www/html/api/2.0/
COPY common /var/www/html/api/common/
COPY notifications /var/www/html/api/notifications/
COPY dist/latest.php /var/www/html/dist/latest.php
RUN echo "<?php echo file_get_contents('https://files.schoolpower.tech/update.json');" > /var/www/html/api/update.json.php
RUN sed -i "s/127\.0\.0\.1/${SQL_HOST}/g" /var/www/html/api/common/db.php
RUN sed -i "s/\"SQL_USERNAME\"\, \"root\"/\"SQL_USERNAME\", \"${SQL_USERNAME}\"/g" /var/www/html/api/common/db.php
RUN sed -i "s/\"SQL_PASSWORD\"\, \"\"/\"SQL_PASSWORD\", \"${SQL_PASSWORD}\"/g" /var/www/html/api/common/db.php
RUN sed -i "s/SERVERNAME/${NAME}/g" /var/www/html/api/2.0/get_data.php
RUN sed -i "s/localhost/${GRAPHITE_HOST}/g" /var/www/html/api/2.0/get_data.php

EXPOSE 80 443
CMD service collectd start && apache2-foreground
