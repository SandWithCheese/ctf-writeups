<?php
session_start();

if (!isset($_SESSION['admin']) || $_SESSION['admin'] != 1) {
	header("Location: admin_login.php");
	exit;
}

// Sanitize the 'q' parameter to prevent XSS or injection attacks
$q = isset($_GET['q']) ? htmlspecialchars($_GET['q']) : '';

?>
<!DOCTYPE html>
<html lang="en">

<head>
	<title>Admin Page</title>
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
			color: #81d4fa;
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
			background-color: rgba(30, 30, 30, 0.9);
			border-radius: 8px;
			box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
		}

		.container h3 {
			color: #81d4fa;
			margin-bottom: 1rem;
		}

		.container p {
			color: #e0e0e0;
		}

		.logout {
			text-align: center;
			margin-top: 1rem;
		}

		.logout a {
			color: #ff5252;
			text-decoration: none;
			font-weight: bold;
		}

		.logout a:hover {
			color: #ff1744;
		}

		footer {
			text-align: center;
			padding: 1rem;
			background-color: #1e1e1e;
			color: #9e9e9e;
			margin-top: 2rem;
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
	</style>
</head>

<body>
	<header>
		<h1>Admin Panel</h1>
		<nav>
			<a href="index.php">Home</a>
		</nav>
	</header>

	<div class="container">
		<form action="admin.php" method="get">
			<input type="text" name="q" placeholder="Search posts..." value="<?php echo $q; ?>">
			<input type="submit" value="Search">
		</form>
		<?php if (!empty($q)) : ?>
			<h3>Search Results for "<?php echo $q; ?>"</h3>
			<p>Coming soon...</p>
		<?php else : ?>
			<h3>Welcome to the Admin Panel</h3>
			<p>Use the search box to find and edit posts.</p>
		<?php endif; ?>
		<div class="logout">
			<a href="admin_logout.php">Logout</a>
		</div>
	</div>
	<br><br><br><br>
	<br>
	<br>
	<br>
	<br>
	<br>
	<br>
	<br>
	<footer>
		<p>&copy; 2024 Indonesia Furs Community. All rights reserved.</p>
	</footer>
</body>

</html>