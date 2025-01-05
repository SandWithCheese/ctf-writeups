<?php

session_start();
include 'koneksi.php';

$q = $_GET['q'];
$query = "SELECT * FROM post WHERE judul LIKE '%{$q}%' OR konten LIKE '%{$q}%';";

?>
<!DOCTYPE html>
<html lang="en">

<head>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<title>Search Results - Solid Blog</title>
	<link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap" rel="stylesheet">
	<style>
		body {
			font-family: 'Roboto', sans-serif;
			margin: 0;
			padding: 0;
			background-image: url('https://images3.alphacoders.com/120/thumb-1920-1205960.jpg');
			background-size: cover;
			/* Ensures the image covers the entire body */
			background-position: center;
			/* Centers the image */
			background-repeat: no-repeat;
			/* Prevents tiling */
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

		.search-results {
			background-color: #1e1e1e;
			padding: 1.5rem;
			border-radius: 8px;
			box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
		}

		.search-results h3 {
			margin-bottom: 1rem;
			color: #81d4fa;
		}

		.post {
			margin-bottom: 1.5rem;
		}

		.post h2 {
			margin: 0;
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
		<div class="search-results">
			<h3>Search Results for "<?php echo htmlspecialchars($q); ?>"</h3>
			<p><?php if (mysqli_multi_query($conn, $query)) {
					$results = [];
					do {
						if ($result = mysqli_store_result($conn)) {
							while ($row = mysqli_fetch_array($result)) {
								$results[] = $row;
							}
							mysqli_free_result($result);
						}
					} while (mysqli_next_result($conn));
				} else {
					die("Query failed: " . mysqli_error($conn));
				}
				echo count($results); ?> results found</p>
			<hr>
			<?php foreach ($results as $row): ?>
				<div class="post">
					<a href="post.php?id=<?php echo $row['id']; ?>">
						<h2><?php echo htmlspecialchars($row['judul']); ?></h2>
					</a>
					<small>Posted on <?php echo htmlspecialchars($row['tanggal']); ?></small>
				</div>
				<hr>
			<?php endforeach; ?>
		</div>
	</div>

	<footer>
		<p>&copy; 2024 Indonesia Furs Community. All rights reserved.</p>
	</footer>
</body>

</html>