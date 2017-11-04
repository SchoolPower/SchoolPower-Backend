<?php
    if(!isset($_POST["device_token"])||!isset($_POST["username"])||!isset($_POST["password"])){
        header('HTTP/1.1 400 Bad Request');
        exit();
    }

    function safe_argument($mysqli, $str) {
        return $mysqli->real_escape_string(preg_replace('/[^\w]+/','', $str));
    }

    // CREATE TABLE `schoolpower`.`apns` ( `id` INT NOT NULL AUTO_INCREMENT , `token` TEXT NOT NULL , PRIMARY KEY (`id`)) ENGINE = InnoDB;
    // connect to the database
    $mysqli = new mysqli("127.0.0.1", "root", "", "schoolpower");

    if ($mysqli->connect_errno) {
        header('HTTP/1.1 500 Internal Server Error');
        exit("Failed to connect to MySQL: (" . $mysqli->connect_errno . ") " . $mysqli->connect_error);
    }
    
    $token = safe_argument($mysqli, $_POST["device_token"]);

    if ($result = $mysqli->query("SELECT * FROM apns WHERE token = '$token'", MYSQLI_USE_RESULT)) {
        $new_device = $result->fetch_array() == null;
        $result->close();
        
        if($new_device){
            $mysqli->query("INSERT INTO apns(token) VALUES ('$token')");
        }
    }
?>
