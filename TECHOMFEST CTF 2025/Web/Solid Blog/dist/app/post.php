<?php

session_start();
include 'koneksi.php';

$id = $_GET['id'];
$q = mysqli_query($conn, "SELECT * FROM post WHERE id = {$id}") or die(mysqli_error($conn));
$post = mysqli_fetch_array($q);

?>
<!DOCTYPE html>
<html lang="en">

<head>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<title>Solid Blog Post</title>
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

		.post {
			background-color: #1e1e1e;
			padding: 1.5rem;
			border-radius: 8px;
			box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
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
			margin-bottom: 1rem;
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
			<h2><?php echo htmlspecialchars($post['judul']); ?></h2>
			<small>Posted on <?php echo htmlspecialchars($post['tanggal']); ?></small>
			<p><?php echo nl2br($post['konten']); ?></p>
		</div>
	</div>

	<footer>
		<p>&copy; 2024 Indonesia Furs Community. All rights reserved.</p>
	</footer>
</body>

</html>