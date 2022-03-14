<?php

define('DB_SERVER', 'localhost');
define('DB_USERNAME', 'root');
define('DB_PASSWORD', '!@#qweasd123');
define('DB_NAME', 'webDB');

$sqllink = mysqli_connect(DB_SERVER, DB_USERNAME, DB_PASSWORD, DB_NAME);

if ($sqllink === false) {
    die("ERROR: Could not connect. " . mysqli_connect_error());
} else {
    echo "connection established";
}

?>