<?php
require 'vendor/autoload.php';
require 'config.php';

use Dompdf\Dompdf;
use Dompdf\Options;

$errors = [];

if (isset($_POST['data'])) {
  extract($_POST['data']);
  if (!preg_match('/^[A-Za-z0-9 ]+$/', $name)) {
    $errors['name'] = "Invalid name. Only letters, numbers, and spaces allowed.";
  }
  if (!filter_var($photoUrl, FILTER_VALIDATE_URL)) {
    $errors['photoUrl'] = "Invalid photo URL format.";
  }
  if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
    $errors['email'] = "Invalid email format.";
  }
  if (!preg_match('/^[0-9+ ]+$/', $phone)) {
    $errors['phone'] = "Invalid phone number. Only numbers, +, and spaces allowed.";
  }
  if (!preg_match('/^[A-Za-z0-9#&()@ ]+$/', $address)) {
    $errors['address'] = "Invalid address. Only letters, numbers, #, &, (, ), and @ allowed.";
  }
} else {
  $errors['data'] = "No data provided";
}

if (!empty($errors)) {
  foreach ($errors as $field => $error) {
    echo "<p><strong>$field:</strong> $error</p>";
  }
  die();
}

$html = '
<!DOCTYPE html>
<html>
<head>
  <style>
    body {
      font-family: Arial, sans-serif;
      text-align: center;
    }
    .name-card {
      width: 320px;
      height: 180px;
      border: 2px solid #333;
      padding: 15px;
      display: flex;
      align-items: center;
      justify-content: center;
      flex-direction: column;
      border-radius: 10px;
      box-shadow: 2px 2px 10px rgba(0,0,0,0.2);
      font-size: 12px;20009
    }
    .photo {
      width: 60px;
      height: 60px;
      border-radius: 50%;
      object-fit: cover;
      border: 2px solid #000;
    }
    .name {
      font-size: 16px;
      font-weight: bold;
      margin-top: 5px;
    }
    .contact {
      font-size: 10px;
      margin-top: 5px;
      text-align: center;
    }
  </style>
</head>
<body>
  <div class="name-card">
    <img src="'.$photoUrl.'" class="photo" alt="User Photo">
    <div class="name">'.$name.'</div>
    <div class="contact">
      <div>Email: '.$email.'</div>
      <div>Phone: '.$phone.'</div>
      <div>Address: '.$address.'</div>
    </div>
  </div>
</body>
</html>
';

$options = new Options();
foreach ($config as $key => $value) {
  $options->set($key, $value);
}
$dompdf = new Dompdf($options);

$dompdf->loadHtml($html);
$dompdf->setPaper([0, 0, 330, 270], 'portrait');
$dompdf->render();
$dompdf->stream("namecard.pdf", ["Attachment" => false]);
