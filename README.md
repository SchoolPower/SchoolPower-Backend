# SchoolPower-Backend
SchoolPower的后端，被SchoolPower-Android和SchoolPower-iOS所依赖。

The backend of SchoolPower, which is depended by SchoolPower-Android and SchoolPower-iOS.

使用了修改版本的[powerapi/PowerAPI-php](https://github.com/powerapi/PowerAPI-php)。

# 安装 Installation

### 1. Setting up environment variables

Copy `.env.template` to `.env` and change accordingly.

### 2. Fetching dependencies

Run `composer install` under '2.0' folder to download dependencies.

### 3. Start up containers

To do this, you will need `docker` and `docker-compose` installed.

```bash
docker-compose up mysql # Database (MySQL) Docker (Only need one instance)
docker-compose up pma # Visit your phpmyadmin and run the below sql to configure the database.
docker-compose up graphite # Graphite (Only need one instance; Unneeded if you don't want statistics)
docker-compose up grafana # Grafana (Dashboard; Only need one instance; Unneeded if you don't want statistics)
docker-compose up backend # SchoolPower (Finally! You can run multiple instances of this)
```

### 4. Configure database

```sql
CREATE TABLE `schoolpower`.`apns` ( `id` INT NOT NULL AUTO_INCREMENT , `token` TEXT NOT NULL , `username` TEXT NOT NULL , `password` TEXT NOT NULL , PRIMARY KEY (`id`)) ENGINE = InnoDB;
CREATE TABLE `schoolpower`.`users` ( `id` INT NOT NULL AUTO_INCREMENT , `username` TEXT NOT NULL , `avatar` TEXT NOT NULL , `remove_code` TEXT NOT NULL , `grade` MEDIUMTEXT NOT NULL , PRIMARY KEY (`id`), UNIQUE `username` (`username`(16))) ENGINE = InnoDB;
```
Also, create a readonly account for grafana's use if needed.

```bash
docker-compose down pma # Remember to stop the container after you have everything configured.
```

### 5. Configure nginx

Install nginx on your host, and configure accordingly.
Below is a working example:
```
server {
    listen 80;
    server_name your.hostname.com;
    error_log  /var/log/nginx/error.log;
    access_log /var/log/nginx/access.log;

    location / {
        root /var/www/html/;
        fastcgi_pass backend:9000;
        fastcgi_index index.php;
        include fastcgi_params;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        fastcgi_param PATH_INFO $fastcgi_path_info;
    }
}
```

Be sure to use HTTPS for increased security!

### 6. Configure APN Push

```bash
apt install python3 python3-pip
python3 -m pip install apns2 pymysql
```

Put your APN private pem to `notifications/apns.pem`.

Create `notifications/config.py` with the following content,
```
SQL_SERVER_ADDRESS = "YOU_SQL_SERVER_ADDRESS"
SQL_SERVER_USER = "schoolpower"
SQL_SERVER_PASSWORD = "YOU_SQL_SERVER_PASSWORD"
SQL_SERVER_DATABASE = "schoolpower"
```

Lastly, configure the crontab by
```bash
echo "0 6-23  * * *   root    cd /root/SchoolPower-Backend/notifications && python3 apns_provider.py" >> /etc/crontab 
```
This will push notifications every hour from 6 a.m. to 23 p.m..

### 7. Configure collectd (not necessary if you don't need it)

```bash
sudo apt-get install collectd-core
sudo apt-get install --no-install-recommends collectd
vim /etc/collectd/collectd.conf # change the config accordingly.
service collectd restart
```

Example of a working `write_graphite` configuration:
```
<Plugin write_graphite>
        <Node "collectd">
                Host "graphite"
                Port "2003"
                Protocol "tcp"
                LogSendErrors true
                Prefix "collectd."
                StoreRates true
                AlwaysAppendDS false
                EscapeCharacter "_"
        </Node>
</Plugin>
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
    Copyright 2018 SchoolPower Studio

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at
    
        http://www.apache.org/licenses/LICENSE-2.0
    
    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
