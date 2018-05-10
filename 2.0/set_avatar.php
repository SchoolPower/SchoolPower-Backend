<?php
    require_once '../common/db.php';
    require_once 'vendor/autoload.php';
    require_once 'config.php';
    
    header('Content-type: application/json');
    
    if(!isset($_POST["username"])||!isset($_POST["password"])||!isset($_POST["new_avatar"])||!isset($_POST["remove_code"])){
        exit('{"success":"false", "error": "invalid request; check your parameters"}');
    }
    
    $username = strtolower(preg_replace('/[^\w]+/','',$_POST["username"]));
    $password = preg_replace('/[^\w]+/','',$_POST["password"]);
    $avatar = $_POST["new_avatar"];
    $remove_code = $_POST["remove_code"];
    
    try {
        $student = PowerAPI\PowerAPI::authenticate(POWERSCHOOL_URL, $username, $password, false);
    } catch (PowerAPI\Exceptions\Authentication $e) {
        exit('{"success":"false", "error": "'.$e->getMessage().'"}');
    }
    
    $stmt = $mysqli->prepare("INSERT INTO users (username, avatar, remove_code) VALUES (?, ?, ?) ON DUPLICATE KEY UPDATE avatar=?, remove_code=CONCAT(remove_code,' ',?);");
    $stmt->bind_param("sssss", $username, $avatar, $remove_code, $avatar, $remove_code);

    if($stmt->execute())
        exit('{"success":"true"}');
    else
        exit('{"success":"false", "error": "'.$stmt->error.'"}');
    