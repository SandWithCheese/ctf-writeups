<?php
// home.php
session_start();

// Define timeout duration (e.g., 1800 seconds = 30 minutes)
$timeout_duration = 1800;

// Check if the user is logged in
if (!isset($_SESSION['username'])) {
    // Redirect to the login page if not logged in
    header("Location: index.php");
    exit();
}

// Check if last activity is set and if the session has expired
if (isset($_SESSION['last_activity']) && (time() - $_SESSION['last_activity']) > $timeout_duration) {
    // Last request was more than timeout_duration ago, destroy session and redirect to login
    session_unset();
    session_destroy();
    header("Location: index.php?timeout=1");
    exit();
}

// Update last activity time stamp
$_SESSION['last_activity'] = time();
?>

<!DOCTYPE html>
<html lang="en">
    <head>
        <title><?php echo $_SESSION['username'];?></title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        <link href="https://fonts.googleapis.com/css?family=Lato:300,400,700&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css">
        <link rel="stylesheet" href="css/style.css">
    </head>
    <body>
        <section class="ftco-section">
            <div class="container">
                <div class="row justify-content-center">
                    <div class="col-md-6 text-center mb-5">
                        <h2 class="heading-section">Mount Hua</h2>
                    </div>
                </div>
                <div class="row justify-content-center">
                    <div class="col-md-12 col-lg-10">
                        <div class="wrap d-md-flex">
                            <div class="img" style="background-image: url(images/chung_myung2.jpg);">
                            </div>
                            <div class="login-wrap p-4 p-md-5">
                                <div class="d-flex">
                                    <div class="w-100">
                                        <h3 class="mb-4"><?php echo $_SESSION['role']?> Page</h3>
                                    </div>
                                    <div class="w-100">
                                        <p class="social-media d-flex justify-content-end">
                                            <a href="#" class="social-icon d-flex align-items-center justify-content-center"><span class="fa fa-facebook"></span></a>
                                            <a href="#" class="social-icon d-flex align-items-center justify-content-center"><span class="fa fa-twitter"></span></a>
                                        </p>
                                    </div>
                                </div>
                                <div class="container">
                                    <h2>Hi <?php echo $_SESSION['username']?>!</h2>
                                    <p>The Mount Hua Sect is a long standing rival of the Zhongnan Sect.[1] They were once part of the 10 Great Sects, before their decline following the final battle against Chun Ma.[?]</p>
                                </div>
                                <a href="logout.php">logout</a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
        </section>
        <script src="js/jquery.min.js"></script>
        <script src="js/popper.js"></script>
        <script src="js/bootstrap.min.js"></script>
        <script src="js/main.js"></script>
    </body>
</html>