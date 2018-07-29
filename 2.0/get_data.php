<?php
require_once 'vendor/autoload.php';
require_once 'config.php';

header('Content-type: application/json');

if(!isset($_POST["username"])||!isset($_POST["password"]))
    exit('{"err":"100","description":"No username or password is given."}');

$username = preg_replace('/[^\w]+/','',$_POST["username"]);
$password = preg_replace('/[^\w]+/','',$_POST["password"]);

if($username == "test2"){
    exit('{"information":{"currentGPA":null,"currentTerm":"T1","firstName":"Firstname","gender":"M","dob":"","id":"1","lastName":"LastName","middleName":"MiddleName","photoDate":"2017-10-01T16:00:00.000Z"},"sections":[],"attendances":[]}');
}
if($username == "test"){
    exit('{"information":{"currentGPA":null,"currentMealBalance":"0.0","currentTerm":"T1","dcid":"10000","dob":"2001-06-01T16:00:00.000Z","ethnicity":null,"firstName":"Liu","gender":"M","gradeLevel":"11","guardianAccessDisabled":"false","id":"10000","lastName":"Wu","middleName":"John","photoDate":"2017-10-25T16:16:39.469Z","startingMealBalance":"0.0"},"sections":[{"assignments":[{"category":"Quizzes","description":"Significant digits, scientific notation and v/t graphs","name":"Quiz 1 Chapter 1","percent":"97.83","score":"' . rand(0, 46) . '","letterGrade":"A","pointsPossible":"46.0","date":"2017-09-10T16:00:00.000Z","weight":"0.22","includeInFinalGrade":"1","terms":["S1","T1","Y1"]}],"expression":"1(A-E)","startDate":"2017-09-05T16:00:00.000Z","endDate":"2018-01-21T16:00:00.000Z","finalGrades":{"X1":{"percent":"0.0","letter":"--","comment":null,"eval":"--","startDate":1515945600,"endDate":1515945600},"T2":{"percent":"94.0","letter":"A","comment":"Student shows exceptional potential in Science. Excellent progress. ","eval":"M","startDate":1510502400,"endDate":1510502400},"T1":{"percent":"89.0","letter":"A","comment":"Student shows exceptional potential in Science. Student shows excellent participation and displays a great attitude every class. ","eval":"M","startDate":1504195200,"endDate":1504195200},"S1":{"percent":"93.0","letter":"A","comment":null,"eval":"M","startDate":1504195200,"endDate":1504195200}},"name":"Physics 11","roomName":"203","teacher":{"firstName":"John","lastName":"Doe","email":"fake_email@email.com","schoolPhone":null}}],"attendances":[{"code":"E","description":"Excused Absence","date":"2017-10-16T16:00:00.000Z","period":"3(B,D)","name":"Chinese Social Studies ' . rand(1, 12) . '"},{"code":"I","description":"Illness","date":"2017-12-10T16:00:00.000Z","period":"1(A-E)","name":"Physics 11"}]}');
}

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
    exit('{"err":"200","description":"'.addslashes($e->getMessage()).'","reserved":"Something went wrong! Invalid Username or password"}');
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
