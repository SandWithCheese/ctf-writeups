<?php

session_start();
include 'koneksi.php';
$posts = mysqli_query($conn, "SELECT * FROM post");

?>
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Solid Blog</title>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Roboto', sans-serif;
            margin: 0;
            padding: 0;
            background-image: url('https://images3.alphacoders.com/120/thumb-1920-1205960.jpg');
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            color: #e0e0e0;
            line-height: 1.6;
        }

        header {
            background-color: #1e1e1e;
            padding: 1rem 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
        }

        header h1 {
            margin: 0;
            font-size: 1.5rem;
        }

        nav a {
            color: #81d4fa;
            text-decoration: none;
            margin: 0 1rem;
            font-weight: 700;
        }

        nav a:hover {
            color: #29b6f6;
        }

        .container {
            max-width: 800px;
            margin: 2rem auto;
            padding: 1rem;
        }

        form {
            margin-bottom: 2rem;
            display: flex;
            justify-content: space-between;
            gap: 1rem;
        }

        input[type="text"] {
            flex: 1;
            padding: 0.5rem;
            border: 1px solid #424242;
            border-radius: 5px;
            background-color: #212121;
            color: #e0e0e0;
        }

        input[type="submit"] {
            padding: 0.5rem 1rem;
            border: none;
            border-radius: 5px;
            background-color: #29b6f6;
            color: #fff;
            font-weight: 700;
            cursor: pointer;
        }

        input[type="submit"]:hover {
            background-color: #039be5;
        }

        .post {
            background-color: #1e1e1e;
            margin-bottom: 1.5rem;
            padding: 1rem;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
            opacity: 0.9;
        }

        .post h2 {
            margin: 0 0 0.5rem;
            color: #81d4fa;
        }

        .post h2:hover {
            text-decoration: underline;
        }

        .post small {
            display: block;
            margin-bottom: 0.5rem;
            color: #9e9e9e;
        }

        footer {
            text-align: center;
            padding: 1rem;
            background-color: #1e1e1e;
            margin-top: 2rem;
        }

        footer p {
            margin: 0;
            color: #9e9e9e;
        }
    </style>
</head>

<body>
    <header>
        <h1>Solid Blog</h1>
        <nav>
            <?php if (isset($_SESSION['admin']) && $_SESSION['admin'] == 1): ?>
                <a href="admin.php">Admin</a>
            <?php endif; ?>
            <a href="index.php">Home</a>
            <a href="about.php">About</a>
            <a href="admin_login.php">Login</a>
        </nav>
    </header>

    <div class="container">
        <div class="post">
            <center>
                <h1>Indonesia Furs Community</h1>
                <p> Welcome to the Indonesia Furs Community. We are a community of furries from all over Indonesia. We are a community that is open to everyone, regardless of their fur type.</p>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                    <p> Founder : <br> <b>Daffainfo</b> </p>
                    <p> Cofounder : <br> <b>Dimas Maulana</b> </p>
                </div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                    <img src="https://t3.ftcdn.net/jpg/07/17/33/40/360_F_717334058_zZu41aMmrR0CvBxI3WLbWRjrqFyLAdW1.jpg"
                        alt="Founder Image"
                        style="width: 100%; aspect-ratio: 1/1; border-radius: 8px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2); object-fit: cover;">
                    <img src="https://img.freepik.com/premium-photo/cute-cartoon-cat-winter-clothes_922357-41956.jpg"
                        alt="Cofounder Image"
                        style="width: 100%; aspect-ratio: 1/1; border-radius: 8px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2); object-fit: cover;">
                </div>
                <p> Other Members : <br> <b>azuketto</b> <br> <b>marc</b> <br> <b>rui</b> <br> <b>53buahapel</b> <br> <b>and many others</b> </p>

            </center>
        </div>
    </div>

    <footer>
        <p>&copy; 2024 Indonesia Furs Community. All rights reserved.</p>
    </footer>
</body>

</html>