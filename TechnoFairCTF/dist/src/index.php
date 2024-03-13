<?php

include "user.php";

if (!isset($_COOKIE["user"])) {
    setcookie("user", serialize(new User("guest")));
}

?>

<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login</title>
    <link rel="stylesheet" href="css/bootstrap.min.css">
</head>

<body>
    <div class="min-vh-100 d-flex justify-content-center align-items-center">
        <form method="POST" action="login.php" class="container bg-dark text-white p-4 rounded" style="width: 400px">
            <div class="mb-3">
                <h1 class="text-center">Login</h1>
            </div>
            <div class="mb-3">
                <label for="username" class="form-label">Username</label>
                <input type="text" name="username" class="form-control" id="username" autocomplete="off">
            </div>
            <div class="mb-3">
                <label for="password" class="form-label">Password</label>
                <input type="password" name="password" class="form-control" id="password" autocomplete="off">
            </div>
            <button type="submit" name="submit" class="btn btn-primary">Login</button>
        </form>
    </div>

    <script src="js/bootstrap.bundle.min.js"></script>
</body>

</html>