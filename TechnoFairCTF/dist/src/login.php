<?php

if (isset($_POST["submit"]) && isset($_POST["username"]) && isset($_POST["password"])) {
    include "credential.php";
    include "user.php";

    $conn = new mysqli($mysql_host, $mysql_user, $mysql_pass, $mysql_db);

    $username = mysqli_real_escape_string($conn, $_POST["username"]);
    $password = mysqli_real_escape_string($conn, $_POST["password"]);

    $stmt = $conn->prepare("SELECT * FROM users WHERE username = ?");
    $stmt->bind_param("s", $username);
    $stmt->execute();
    $result = $stmt->get_result();

    if ($result->num_rows === 1) {
        $row = $result->fetch_assoc();
        $storedPassword = $row["password"];

        if (password_verify($password, $storedPassword)) {
            setcookie("user", serialize(new User("admin")));
            header("Location: flag.php");
            exit();
        }
    }
}

header("Location: index.php");
exit();

?>