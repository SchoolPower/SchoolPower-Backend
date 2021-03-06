<?php
ini_set("default_socket_timeout", 15);
require_once 'vendor/autoload.php';
require_once 'config.php';

use Monolog\Logger;
use Monolog\Handler\StreamHandler;
use Monolog\Formatter\JsonFormatter;

$log = new Logger('get_data.php');

$formatter = new JsonFormatter();

$stream = new StreamHandler(__DIR__ . '/application-json.log', Logger::DEBUG);
$stream->setFormatter($formatter);

$log->pushHandler($stream);

header('Content-type: application/json');
header('Access-Control-Allow-Origin: *');

if (!isset($_POST["username"]) || !isset($_POST["password"]))
    exit('{"err":"100","description":"No username or password is given.","instance":"' . getenv('NAME') . '"}');

$username = $_POST["username"]; //preg_replace('/[^\w]+/','', $_POST["username"]);
$password = $_POST["password"]; //preg_replace('/[^\w]+/','', $_POST["password"]);

if ($username == "test") {
    exit(file_get_contents('https://files.schoolpower.tech/test/test.json'));
}
if ($username == "test2") {
    exit(file_get_contents('https://files.schoolpower.tech/test/test2.json'));
}

$HOST_NAME = getenv('NAME') . ".api.v2";

$context = array(
    "username" => $username,
    "host" => $HOST_NAME,
    "os" => $_POST['os'],
    "version" => $_POST['version'],
    "action" => $_POST['action']
);

$log->info('Request received', $context);

$connection = new \Domnikl\Statsd\Connection\UdpSocket(getenv('GRAPHITE_HOST'), getenv('GRAPHITE_PORT'));
$statsd = new \Domnikl\Statsd\Client($connection, $HOST_NAME);
$statsd->setNamespace($HOST_NAME);
$statsd->increment("total_call");

try {
    $statsd->startTiming("fetch_data_time");
    $student = PowerAPI\PowerAPI::authenticate(POWERSCHOOL_URL, $username, $password);
    $statsd->endTiming("fetch_data_time");
} catch (PowerAPI\Exceptions\Authentication $e) {
    $statsd->endTiming("fetch_data_time");
    $statsd->increment("failed_call");
    $log->error('Exception ' . $e->getMessage(), $context);
    if ($e->getMessage() == "Invalid Username or password")
        exit('{"err":"200","description":"' . addslashes($e->getMessage()) . '","reserved":"Something went wrong! Invalid Username or password"}');
    else if ($e->getMessage() == "ERROR_PASSWORD_ADMIN_RESET")
        exit('{"err":"202","description":"ERROR_PASSWORD_ADMIN_RESET",alert:"You password is reset by admin. Please contact your school.","reserved":""}');
    else
        exit('{"err":"201","description":"' . addslashes($e->getMessage()) . '","reserved":""}');
}
$studentData = $student->jsonSerialize();

// Get avatar from database; comment them out if you don't need it
require_once '../common/db.php';

$stmt = $mysqli->prepare("SELECT avatar FROM users WHERE username = ?");
$stmt->bind_param("s", strtolower($username));
$stmt->execute();
$res = $stmt->get_result();

if ($res->num_rows != 0) {
    $data = $res->fetch_all();
    $studentData["additional"] = array("avatar" => $data[0][0]);
} else {
    $studentData["additional"] = array("avatar" => "");
}

// Add some stats data
$statsd->set('user_usage', $username);
$statsd->increment('version.' . $_POST['os'] . '.' . str_replace(".", "_", $_POST['version']));
$statsd->increment('action.' . $_POST['action']);
$statsd->increment('os.' . $_POST['os']);
$statsd->increment("successful_call");

echo json_encode($studentData);
