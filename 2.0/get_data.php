<?php
require_once 'vendor/autoload.php'; // composer autoloader

try {
    $student = PowerAPI\PowerAPI::authenticate("http://powerschool.mapleleaf.cn", "19050068srt", "200961aaa");
} catch (PowerAPI\Exceptions\Authentication $e) {
    die('Something went wrong! '.$e->getMessage());
}
echo json_encode($student);
