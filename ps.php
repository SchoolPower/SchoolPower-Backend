<?php
    header('Content-type: application/json');
    if(!isset($_POST["username"])){
        exit("It is working...");
    }
    
    $username = escapeshellarg(preg_replace('/[^\w]+/','',$_POST["username"]));
    $password = escapeshellarg(preg_replace('/[^\w]+/','',$_POST["password"]));
    file_put_contents("usage.log.py", date('Y-m-d H:i:s') . ' ' .  $username . "\n",FILE_APPEND);
    if(strtoupper($username)=="'18012643JBL'" && $password=="'optgewaz1997'"){
        echo file_get_contents("test_data.json");
        return;
    }
    if(isset($_POST["filter"])){
        $filter=escapeshellarg(preg_replace('/[^0-9A-Z\,]+/','',$_POST["filter"]));
        system("python3 psmain.py $username $password $filter");
    }else{
        system("python3 psmain.py $username $password");
    }
?>
