# SchoolPower-Backend
SchoolPower的后端，被SchoolPower-Android和SchoolPower-iOS所依赖。

The backend of SchoolPower, which is depended by SchoolPower-Android and SchoolPower-iOS.

**我知道这个README很乱，如果有人真的想要配置的话，欢迎 [联系我](mailto:harryyunull@gmail.com)**

Welcome to [contact me](mailto:harryyunull@gmail.com) if you really want to use this!

2.0版本API使用了修改版本的[powerapi/PowerAPI-php](https://github.com/powerapi/PowerAPI-php)

**2.0版本在2.0目录内，加快获取速度和增加可获取内容，规范化结构化返回内容，优化文件大小**

配置：

```sql
CREATE TABLE `schoolpower`.`apns` ( `id` INT NOT NULL AUTO_INCREMENT , `token` TEXT NOT NULL , `username` TEXT NOT NULL , `password` TEXT NOT NULL , PRIMARY KEY (`id`)) ENGINE = InnoDB;
```

```bash
easy_install apns2
```

## TODO (懒得做的)

- [ ] 2.0的文档和使用方式

- [ ] 扩展名规范化

- [ ] 整理文件

- [ ] 依赖规范化

**以下是1.0版本的配置方法，现已失效**

## 如何使用 Usages

### 配置 Configuration

修改``config.py``, 将HOST的值改为您学校的PowerSchool网址，通常类似于http://example.com/guardian/。

修改``update.json``, 将url的值修改为APK的下载地址。

您还需要修改Android/iOS配置文件里对应的常量改为您服务器的api网址。

Edit ``config.py``, change the value of HOST to the URL of your school's PowerSchool platform. For example, http://example.com/guardian/ .

Edit ``update.json``, change the value of url to the url of your apk file.

You also need to change the constants in Android/iOS project to the corresponding urls.

### 部署 Deployment

### 直接部署 Deploy Directly

将所有文件放到服务器的网站文件夹下(如``/var/www/html``)，然后修改apache2的配置文件(``apache2.conf``)，添加以下代码以禁用.py文件下载。

```ap
<Files ~ "\.py$">
   Order allow,deny
   Deny from all
</Files>
```

Put all files into your website directory(like ``/var/www/html``), and edit your configuration of apache2 (``apache2.conf``) to disable download of .py files.

### Docker

尚未完成，欢迎PR完善。

In progress. PR is welcomed.

## 常见问题 Common Questions

1. 无法使用/报错 Crashes.

   此程序仅对特定学校进行了适配，不保证具有普适性，不同学校之间可能具有微小的差异，请自行进行修改。

   如果您相信该问题是普遍问题，您可以发布一个issue或PR。

   The program only adapts to specific schools, and may not work for some schools because of minor difference between different schools. You may change it by yourself. If you believe it's a general problem, please open an issue or PR.

2. 速度慢 Slow speed.

   该程序的获取速度受限于您学校PowerSchool平台的速度，请将此程序运行在一个可以快速访问到您学校PowerSchool服务器的地区。

   The speed of the program limits to your school's PowerSchool platform. Please deploy the program in a region that have fast access to your school's server.



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
