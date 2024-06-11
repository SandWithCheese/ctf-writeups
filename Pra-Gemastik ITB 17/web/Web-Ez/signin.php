<?php
session_start();

// Function to validate user credentials
function validate_user($username, $password, $role, $users) {
    foreach ($users as $user) {
        if ($user['username'] === $username && $user['password'] === $password) {
            return true;
        }
    }
    return false;
}

// Check if the form is submitted
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Path to the text file
    $file_path = 'data-folder/data';

    // Read the file content into a string
    $file_content = file_get_contents($file_path);


    // initialize users
    $users = [];

    // Check if file content is successfully read
    if ($file_content !== false) {
        // Split the content by lines
        $lines = explode(PHP_EOL, $file_content);
        
        // Iterate through each line
        foreach ($lines as $line) {
            // Skip empty lines
            if (trim($line) == '') {
                continue;
            }

            // Split the line by the delimiter "|"
            $parts = explode('|', $line);
            
            // Check if the expected number of parts is obtained
            // Assign parts to variables
            $name = $parts[0];
            $password = $parts[1];
            $role = $parts[2];
            
            // Output the parsed values
            $users[] = [
                'username' => $name,
                'password' => $password,
                'role' => $role
            ];
        }
    } else {
        echo "Failed to read the file.";
    }

    // Retrieve username and password from POST request
    $username = $_POST["username"];
    $password = $_POST["password"];
    
    // Validate user credentials
    if (validate_user($username, $password, $role, $users)) {
        // Start a session and set a session variable
        $_SESSION['username'] = $username;
        $_SESSION['role'] = $role;
        $_SESSION['last_activity'] = time(); // Set the time of the last activity
        // Redirect to the home page
        if($role == "user"){
            header("Location: home.php");
        } else if($role == "admin"){
            header("Location: upload-index.php");
        } else {
            header("Location: index.php");
        }
        exit();
    } else {
        echo "Invalid username or password.";
    }
} else {
    // Redirect to login form if accessed directly
    header("Location: index.php");
    exit();
}
?>