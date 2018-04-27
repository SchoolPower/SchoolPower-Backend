<?php
    // CREATE TABLE `schoolpower`.`apns` ( `id` INT NOT NULL AUTO_INCREMENT , `token` TEXT NOT NULL , PRIMARY KEY (`id`)) ENGINE = InnoDB;
    // CREATE TABLE `schoolpower`.`users` ( `id` INT NOT NULL AUTO_INCREMENT , `username` TEXT NOT NULL , `avatar` TEXT NOT NULL , `remove_code` TEXT NOT NULL , `grade` MEDIUMTEXT NOT NULL , PRIMARY KEY (`id`), UNIQUE `username` (`username`(16))) ENGINE = InnoDB;
    // PRIMARY KEY (`id`)) ENGINE = InnoDB;
    
    // connect to the database
    $mysqli = new mysqli("127.0.0.1", "root", "", "schoolpower");

    if ($mysqli->connect_errno) {
        header('HTTP/1.1 500 Internal Server Error');
        exit("Failed to connect to MySQL: (" . $mysqli->connect_errno . ") " . $mysqli->connect_error);
    }
