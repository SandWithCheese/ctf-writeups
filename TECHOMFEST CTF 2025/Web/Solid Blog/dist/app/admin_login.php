<?php
session_start();
include 'koneksi.php';

if (isset($_POST['submit'])) {
	$username = $_POST['username'];
	$password = $_POST['password'];

	$login = mysqli_query($conn, "SELECT * FROM user WHERE username = '{$username}' AND password = '{$password}'");

	if (mysqli_num_rows($login) == 0) {
		$error_message = "Username atau password salah!";
	} else {
		$_SESSION['admin'] = 1;
		header("Location: admin.php");
		exit;
	}
}
?>
<!DOCTYPE html>
<html lang="en">

<head>
	<title>Admin Login</title>
	<meta http-equiv="content-type" content="text/html;charset=utf-8" />
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
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
			max-width: 400px;
			margin: 2rem auto;
			background-color: rgba(30, 30, 30, 0.9);
			padding: 2rem;
			border-radius: 8px;
			box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
		}

		.container h1 {
			text-align: center;
			margin-bottom: 1.5rem;
			color: #81d4fa;
		}

		form {
			display: flex;
			flex-direction: column;
			gap: 1rem;
		}

		form p {
			margin: 0;
			color: #e0e0e0;
			font-size: 1rem;
			font-weight: bold;
		}

		input[type="text"],
		input[type="password"] {
			padding: 0.75rem;
			border: 1px solid #424242;
			border-radius: 5px;
			background-color: #212121;
			color: #e0e0e0;
			font-size: 1rem;
		}

		input[type="submit"] {
			padding: 0.75rem;
			border: none;
			border-radius: 5px;
			background-color: #29b6f6;
			color: #fff;
			font-weight: 700;
			cursor: pointer;
			font-size: 1rem;
		}

		input[type="submit"]:hover {
			background-color: #039be5;
		}

		.error-message {
			text-align: center;
			color: red;
			font-weight: bold;
			margin-bottom: 1rem;
		}

		footer {
			text-align: center;
			padding: 1rem;
			background-color: #1e1e1e;
			color: #9e9e9e;
			margin-top: 2rem;
			box-shadow: 0 -4px 6px rgba(0, 0, 0, 0.2);
		}
	</style>
</head>

<body>
	<header>
		<h1>Solid Blog</h1>
		<nav>
			<a href="index.php">Home</a>
		</nav>
	</header>

	<div class="container">
		<h1>Admin Login</h1>

		<?php if (isset($error_message)) : ?>
			<div class="error-message"><?php echo $error_message; ?></div>
		<?php endif; ?>

		<form action="" method="post">
			<p>Username:</p>
			<input type="text" name="username" placeholder="Enter your username" required>

			<p>Password:</p>
			<input type="password" name="password" placeholder="Enter your password" required>

			<input type="submit" name="submit" value="Login">
		</form>
	</div>
	<br>
	<br>
	<br>
	<br>
	<footer>
		<p>&copy; 2024 Indonesia Furs Community. All rights reserved.</p>
	</footer>
</body>

</html>