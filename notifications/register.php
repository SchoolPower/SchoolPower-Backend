<?php
    if(!isset($_POST["device_token"])){
        header('HTTP/1.1 400 Bad Request');
        exit();
    }

    function safe_argument($mysqli, $str) {
        return $mysqli->real_escape_string(preg_replace('/[^\w]+/','', $str));
    }
    
    include("../common/db.php")
    
    $token = safe_argument($mysqli, $_POST["device_token"]);

    if ($result = $mysqli->query("SELECT * FROM apns WHERE token = '$token'", MYSQLI_USE_RESULT)) {
        $new_device = $result->fetch_array() == null;
        $result->close();
        
        if($new_device){
            $mysqli->query("INSERT INTO apns(token) VALUES ('$token')");
        }
    }
