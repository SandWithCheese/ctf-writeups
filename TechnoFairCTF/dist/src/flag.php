<?php

if (!isset($_COOKIE["user"])) {
    header("Location: index.php");
    exit();
}

include "filereader.php";
include "query.php";
include "record.php";
include "user.php";

$user = unserialize($_COOKIE["user"]);

if (!($user instanceof User)) {
    var_dump($user);
    exit();
}

if ($user->getType() !== "admin") {
    header("Location: index.php");
    exit();
}

?>

<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flag</title>
    <link rel="stylesheet" href="css/bootstrap.min.css">
</head>

<body>
    <div class="min-vh-100 d-flex justify-content-center align-items-center">
        <h1>FLAG : REDACTED</h1>
    </div>

    <script src="js/bootstrap.bundle.min.js"></script>
</body>

</html>