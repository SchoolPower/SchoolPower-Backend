<?php
require_once 'vendor/autoload.php';
require_once 'config.php';

if(!isset($_POST["username"]))
    exit("No username is given");

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
    file_put_contents("../error.log.py", date('Y-m-d H:i:s') . ' ' .  $e->getMessage() . "\n",FILE_APPEND);
    exit('Something went wrong! '.$e->getMessage());
    $statsd->increment("failed_call");
}
header('Content-type: application/json');

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

$statsd->set('user_usage', $username);
$statsd->increment('version.' . str_replace(".","_",$_POST['version']));
$statsd->increment('action.' . $_POST['action']);
$statsd->increment('os.' . $_POST['os']);
$statsd->increment("successful_call");

echo json_encode($studentData);
