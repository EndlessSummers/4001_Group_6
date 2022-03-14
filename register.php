<?php
require_once 'config.php';

$username = $password = $repassword = '';
$username_err = $password_err = $confirm_password_err = "";

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    
    // check username
    if (empty(trim($_POST["username"]))) {
        $username_err = "Please enter a username.";
    // } else if (!preg_match('/^[a-zA-Z0-9_]+$/', trim($_POST["username"]))) {
    //     $username_err = "Username can only contain letters, numbers, and underscroes.";
    } else {
        $sqlquery = "SELECT id from users where username = ?";
        if ($stmt = mysqli_prepare($sqllink, $sqlquery)) {
            mysqli_stmt_bind_param($stmt, "s", $param_username);
            $param_username = trim($_POST["username"]);

            if (mysqli_stmt_execute($stmt)) {
                // store result in an internal buffer
                mysqli_stmt_store_result($stmt);

                if (mysqli_stmt_num_rows($stmt) == 1) {
                    $username_err = "This username is already taken.";
                } else {
                    $username = trim($_POST["username"]);
                }
            } else {
                // execute failure
                echo "Something went wrong. Please try again later.";
            }
            mysqli_stmt_close($stmt);
        }
    }

    // check password 
    // NOTE: password validation can happen before submit (i.e. client-end)
    if (empty(trim($_POST["password"]))) {
        $password_err = "Please enter a password.";
    } else if (strlen($_POST["password"]) < 6) {
        $password_err = "Password must have atleast 6 characters.";
    } else {
        $password = trim($_POST["password"]);
    }

    // confirm password
    if(empty(trim($_POST["repassword"]))){
        $confirm_password_err = "Please confirm password.";     
    } else{
        $confirm_password = trim($_POST["repassword"]);
        if(empty($password_err) && ($password != $confirm_password)){
            $confirm_password_err = "Password did not match.";
        }
    }

    if (empty($username_err) && empty($password_err) && empty($confirm_password_err)) {
        $sqlquery = "INSERT INTO users (username, password) VALUES (?, ?)";
        if ($stmt = mysqli_prepare($sqllink, $sqlquery)) {
            mysqli_stmt_bind_param($stmt, "ss", $param_username, $param_password);

            $param_username = $username;
            $param_password = password_hash($password, PASSWORD_DEFAULT);

            if (mysqli_stmt_execute($stmt)) {
                header("HTTP/121.43.57.151");
            } else {
                echo "Something went wrong. Please try again later.";
            }

            mysqli_stmt_close($stmt);
        }
    }

    mysqli_close($sqllink);
}
?>
