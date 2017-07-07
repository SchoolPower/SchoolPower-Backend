<?php
    $is_valid_request = isset($_POST["username"])
    if(!$is_valid_request){
        exit("SchoolPower Backend - It is working...");
    }
    
    function filter_argument($src){
        return escapeshellarg(preg_replace('/[^\w]+/','',$src));
    }
    
    header('Content-type: application/json');
    $username = filter_argument($_POST["username"]);
    $password = filter_argument($_POST["password"]);
    
    file_put_contents("usage.log.py", date('Y-m-d H:i:s') . ' ' .  $username . "\n",FILE_APPEND);
    
    if(isset($_POST["filter"])){
        $filter = filter_argument($_POST["filter"]);
        system("python3 psmain.py $username $password $filter");
    }else{
        system("python3 psmain.py $username $password");
    }
?>
