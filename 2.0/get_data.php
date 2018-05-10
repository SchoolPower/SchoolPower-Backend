<?php
require_once 'vendor/autoload.php';
require_once 'config.php';

if(!isset($_POST["username"]))
    exit("No username is given");

$username = preg_replace('/[^\w]+/','',$_POST["username"]);
$password = preg_replace('/[^\w]+/','',$_POST["password"]);
try {
    $student = PowerAPI\PowerAPI::authenticate(POWERSCHOOL_URL, $username, $password);
} catch (PowerAPI\Exceptions\Authentication $e) {
    file_put_contents("../error.log.py", date('Y-m-d H:i:s') . ' ' .  $e->getMessage() . "\n",FILE_APPEND);
    exit('Something went wrong! '.$e->getMessage());
}
header('Content-type: application/json');
if(!isset($_POST['action'])){
    file_put_contents("../usage.log.py", '2.0 ' . date('Y-m-d H:i:s') . ' ' .  $username .  "\n",FILE_APPEND);
}else{
    file_put_contents("../usage.log.py", "2.0 " . date('Y-m-d H:i:s') . " $username $_POST[version] $_POST[action] $_POST[os]\n",FILE_APPEND);
}

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

echo json_encode($studentData);
