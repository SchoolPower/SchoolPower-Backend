# SchoolPower-Backend
SchoolPower的后端，被SchoolPower-Android和SchoolPower-iOS所依赖。

The backend of SchoolPower, which is depended by SchoolPower-Android and SchoolPower-iOS.

使用了修改版本的[powerapi/PowerAPI-php](https://github.com/powerapi/PowerAPI-php)。

# 配置 Configuration

```sql
CREATE TABLE `schoolpower`.`apns` ( `id` INT NOT NULL AUTO_INCREMENT , `token` TEXT NOT NULL , `username` TEXT NOT NULL , `password` TEXT NOT NULL , PRIMARY KEY (`id`)) ENGINE = InnoDB;
CREATE TABLE `schoolpower`.`users` ( `id` INT NOT NULL AUTO_INCREMENT , `username` TEXT NOT NULL , `avatar` TEXT NOT NULL , `remove_code` TEXT NOT NULL , `grade` MEDIUMTEXT NOT NULL , PRIMARY KEY (`id`), UNIQUE `username` (`username`(16))) ENGINE = InnoDB;
```

You will also need to run `composer install` under '2.0' folder to download dependencies.

## Docker (Recommended)

**Database (MySQL) Docker (Only need one instance):**
```bash
docker run --name sp-mysql -e MYSQL_ROOT_PASSWORD=secret -e MYSQL_DATABASE=schoolpower -p 3306:3306 -d mysql:5
```

**PhpMyAdmin (Unnecessarily after setup):**
```bash
docker run --name myadmin -d --link sp-mysql:db -p 8123:80 phpmyadmin/phpmyadmin
```
Visit your phpmyadmin and run the above sql to configure the database. Remember to stop the container after you have everything configured.

**Graphite (Only need one instance; Unneeded if you don't want statistics):**

Please refer to [graphite-project/docker-graphite-statsd](https://github.com/graphite-project/docker-graphite-statsd). You need to expose 80, 2003, 8125 ports.

**Grafana (Dashboard; Only need one instance; Unneeded if you don't want statistics):** See [here](http://docs.grafana.org/installation/docker/) for more information.
```bash
docker run \
  -d \
  -p 3000:3000 \
  --name=grafana \
  -e "GF_INSTALL_PLUGINS=grafana-piechart-panel" \
  grafana/grafana
```

**SchoolPower (Finally! You can run multiple instances of this):**

To build (Modify the parameters to fit your situation):
```bash
docker build\
 --build-arg NAME=test\
 --build-arg DOMAIN=api.schoolpower.tech\
 --build-arg GRAPHITE_HOST=172.17.0.2\
 --build-arg SQL_HOST=172.17.0.5\
 --build-arg SQL_USERNAME=schoolpower\
 --build-arg SQL_PASSWORD=secret\
 -t schoolpower .
```
To run:
```
docker run -d -v /root/certs/:/etc/letsencrypt/live/ -p 80:80 -p 443:443 schoolpower
```

## Ubuntu
```bash
# Basic fucntion
apt update && apt install software-properties-common -y
add-apt-repository ppa:certbot/certbot
apt update && apt install git python3-pip apache2 php libapache2-mod-php7.0 php7.0-soap python-certbot-apache -y
git clone https://github.com/SchoolPower/SchoolPower-Backend.git
vim /etc/apache2/ports.conf # change to the correct port
vim /etc/apache2/sites-enabled/000-default.conf
mkdir /var/www/html/api
cp -r SchoolPower-Backend/2.0/ /var/www/html/api
/etc/init.d/apache2 restart
# ... more to be configurated (HTTPS).

# For APN Push
easy_install3 apns2
pip3 install pymysql
# ... more to be configurated (crontab, cert).
```

## 常见问题 Common Questions

1. 无法使用/报错 Crashes.

   此程序仅对特定学校进行了适配，不保证具有普适性，不同学校之间可能具有微小的差异，请自行进行修改。

   如果您相信该问题是普遍问题，您可以发布一个issue或PR。

   The program only adapts to specific schools, and may not work for some schools because of minor difference between different schools. You may change it by yourself. If you believe it's a general problem, please open an issue or PR.

2. 速度慢 Slow speed.

   该程序的获取速度受限于您学校PowerSchool平台的速度，请将此程序运行在一个可以快速访问到您学校PowerSchool服务器的地区。

   The speed of the program limits to your school's PowerSchool platform. Please deploy the program in a region that can access your school's server fastly.



License
-------
    Copyright 2017 SchoolPower Studio

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at
    
        http://www.apache.org/licenses/LICENSE-2.0
    
    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
