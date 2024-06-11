
<?php
// signup.php

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Get form data
    $username = $_POST['username'];
    $password = $_POST['password'];

    // Basic form validation
    if (empty($username) || empty($password)) {
        echo "All fields are required.";
        exit;
    }

    // Store user data (here we're storing it in a file, but you should use a database)
    $users_file = 'data-folder/data';
    $users = [];

    if (file_exists($users_file)) {
        // Path to the text file
        $file_path = 'data-folder/data';

        // Read the file content into a string
        $file_content = file_get_contents($file_path);

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
                $pw = $parts[1];
                $role = $parts[2];
                
                // Output the parsed values
                $users[] = [
                    'username' => $name,
                    'password' => $pw,
                    'role' => $role
                ];
            }
        } else {
            echo "Failed to read the file.";
        }
    }

    // Check if username already exists
    foreach ($users as $user) {
        if ($user['username'] === $username) {
            echo "Username already taken.";
            exit;
        }
    }

    // Add new user to users array
    $users[] = [
        'username' => $username,
        'password' => $password,
        'role' => "user"
    ];

    // Save the users array back to the file
    // Open the file for writing
    $file_handle = fopen($file_path, 'w');

    if ($file_handle) {
        // Write the header

        // fwrite($file_handle, "username|password|role\n");
        
        // Write each user's data
        foreach ($users as $user) {
            $line = $user['username'] . '|' . $user['password'] . '|' . $user['role'] . "\n";
            fwrite($file_handle, $line);
        }

        
        // Close the file handle
        fclose($file_handle);
        
        echo "Data has been successfully written to the file.";
    } else {
        echo "Failed to open the file for writing.";
    }

    // Redirect to login page after successful registration
    // header("Location: index.php");
    exit();
} else {
     // Redirect to login form if accessed directly
    //  header("Location: signup.php");
     exit();
}
?>