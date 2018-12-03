<?php
    // CREATE TABLE `schoolpower`.`apns` ( `id` INT NOT NULL AUTO_INCREMENT , `token` TEXT NOT NULL , PRIMARY KEY (`id`)) ENGINE = InnoDB;
    // CREATE TABLE `schoolpower`.`users` ( `id` INT NOT NULL AUTO_INCREMENT , `username` TEXT NOT NULL , `avatar` TEXT NOT NULL , `remove_code` TEXT NOT NULL , `grade` MEDIUMTEXT NOT NULL , PRIMARY KEY (`id`), UNIQUE `username` (`username`(16))) ENGINE = InnoDB;
    define("SQL_HOST", getenv("SQL_HOST"));
    define("SQL_USERNAME", getenv("SQL_USERNAME"));
    define("SQL_PASSWORD", getenv("SQL_PASSWORD"));
    define("SQL_DATABASE", "schoolpower");

    // connect to the database
    $mysqli = new mysqli(SQL_HOST, SQL_USERNAME, SQL_PASSWORD, SQL_DATABASE);

    if ($mysqli->connect_errno) {
        header('HTTP/1.1 500 Internal Server Error');
        exit("Failed to connect to MySQL: (" . $mysqli->connect_errno . ") " . $mysqli->connect_error);
    }
