<?php
require_once 'vendor/autoload.php'; // composer autoloader

$username = preg_replace('/[^\w]+/','',$_POST["username"]);
$password = preg_replace('/[^\w]+/','',$_POST["password"]);
try {
    $student = PowerAPI\PowerAPI::authenticate("http://powerschool.mapleleaf.cn", $username,$password);
} catch (PowerAPI\Exceptions\Authentication $e) {
    file_put_contents("error.log.py", date('Y-m-d H:i:s') . ' ' .  $e->getMessage() . "\n",FILE_APPEND);
    die('Something went wrong! '.$e->getMessage());
}
file_put_contents("usage.log.py", '2.0 ' . date('Y-m-d H:i:s') . ' ' .  $username . "\n",FILE_APPEND);

echo json_encode($student);
