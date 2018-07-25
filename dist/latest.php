<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>SchoolPower</title>
    <meta name="viewport" content="width=device-width,initial-scale=1.0, minimum-scale=1.0, maximum-scale=1.0, user-scalable=no"/>
    <style>a{color:#039be5;text-decoration:none;}body{background:#09314b;padding:10%;text-align:justifyfont-size:1.2rem;font-weight:100;font-family:'Open Sans', sans-serif;color:#FFF;}img{max-width:100%;}</style>
  </head>
  <body>
<?php
$ua = strtolower($_SERVER['HTTP_USER_AGENT']);
if(preg_match('/micromessenger/i', $ua)){ // 微信内置浏览器
?>
    <p>请右上角选择使用浏览器打开</p>
    <p>或使用除了 QQ 和微信以外的软件（如浏览器）扫描二维码 :)</p>
    <img src="https://i.loli.net/2018/05/10/5af43c240a541.jpg" alt="wechat.jpg" title="wechat.jpg" />
    <p>不在使用微信？点击<a href="https://files.schoolpower.tech/dist/latest.apk">这里</a>直接下载</p>
<?php
}else if(preg_match('/mqqbrowser/i', $ua)){ // QQ 浏览器
?>
    <p>请点击<strong>灰色的普通下载</strong>或<strong>直接下载</strong>按钮</p>
    <p>或使用除了 QQ 和微信以外的软件（如浏览器）扫描二维码 :)</p>
    <img src="https://i.loli.net/2018/05/10/5af43c23a3159.jpg" alt="qq.jpg" title="qq.jpg" />
    <meta http-equiv="refresh" content="0;URL=https://files.schoolpower.tech/dist/latest.apk">
    <p>不在使用 QQ 内置浏览器？点击<a href="https://files.schoolpower.tech/dist/latest.apk">这里</a>直接下载</p>
<?php
}else{
    header("Location: https://files.schoolpower.tech/dist/latest.apk");
}
?>
  </body>
</html>
