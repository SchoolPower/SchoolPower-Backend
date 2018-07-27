<?php
require_once 'vendor/autoload.php';
require_once 'config.php';

header('Content-type: application/json');

if(!isset($_POST["username"])||!isset($_POST["password"]))
    exit('{"err":"100","description":"No username or password is given."}');

$username = preg_replace('/[^\w]+/','',$_POST["username"]);
$password = preg_replace('/[^\w]+/','',$_POST["password"]);

$connection = new \Domnikl\Statsd\Connection\UdpSocket('localhost', 8125);
$statsd = new \Domnikl\Statsd\Client($connection, "SERVERNAME.api.v2");
$statsd->setNamespace("SERVERNAME.api.v2");
$statsd->increment("total_call");

try {
    $statsd->startTiming("fetch_data_time");
    $student = PowerAPI\PowerAPI::authenticate(POWERSCHOOL_URL, $username, $password);
    $statsd->endTiming("fetch_data_time");
} catch (PowerAPI\Exceptions\Authentication $e) {
    $statsd->endTiming("fetch_data_time");
    $statsd->increment("failed_call");
    exit('{"err":"200","description":"'.addslashes($e->getMessage()).'","reserved":"Something went wrong! Invalid Username or password"}')
}

// Get avatar from database; comment them out if you don't need it
require_once '../common/db.php';

$stmt = $mysqli->prepare("SELECT avatar FROM users WHERE username = ?");
$stmt->bind_param("s", strtolower($username));
$stmt->execute();
$res = $stmt->get_result();

$studentData = $student->jsonSerialize();
if($res->num_rows!=0){
    $data = $res->fetch_all();
    $studentData["additional"] = Array("avatar" => $data[0][0]);
}else{
    $studentData["additional"] = Array("avatar" => "");
}

// Add some stats data
$statsd->set('user_usage', $username);
$statsd->increment('version.' . str_replace(".","_",$_POST['version']));
$statsd->increment('action.' . $_POST['action']);
$statsd->increment('os.' . $_POST['os']);
$statsd->increment("successful_call");

echo json_encode($studentData);
