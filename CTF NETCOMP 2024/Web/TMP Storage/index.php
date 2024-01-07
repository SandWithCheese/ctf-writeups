<?php

require_once 'conn.php';

if (isset($_POST['submit'])){
    $name = mysqli_real_escape_string($conn, $_POST['name']);
    $mail = mysqli_real_escape_string($conn, $_POST['mail']);
    $desc = mysqli_real_escape_string($conn, $_POST['desc']);
    $imgs = basename($_FILES["image"]["name"]);
    $extn = explode('.', $imgs);
    $extn = end($extn);

    $tmp_dir = "tmp/";
    $target_dir = "uploads/";
    $fnames = time() . '-' . sha1($imgs);
    $target_file = $tmp_dir . $fnames . '.' . $extn;

    $check = getimagesize($_FILES["image"]["tmp_name"]);
    if($check !== false) {
        $uploadOk = 1;
    } else {
        $uploadOk = 0;
    }

    if (file_exists($target_file)) {
        $uploadOk = 0;
    }

    if ($_FILES["image"]["size"] > 500000) {
        $uploadOk = 0;
    }

    if(strtolower($extn) == "php") {
        $uploadOk = 0;
    }

    if ($uploadOk == 1) {
        move_uploaded_file($_FILES["image"]["tmp_name"], $target_file);
        sleep(1);

        $link = $target_dir . $fnames . ".jpg";
        copy($target_file, $link);
        unlink($target_file);

        $sql = "INSERT INTO tmpstorage (name, mail, dcrp, link) VALUES ('$name', '$mail', '$desc', '$link')";
        $conn->query($sql);
    }
}

$conn->close();

?>

<!DOCTYPE html>
<html lang="en">
<head>
  <title>TMP Storage</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.3/jquery.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script>
</head>
<body>

<div class="container">
  <center style="margin-top: 10%;">
    <h2>TMP Storage</h2>
  </center>

  <form action="<?php echo $_SERVER["PHP_SELF"];?>" method="post" enctype="multipart/form-data">
    <div class="form-group">
      <label for="name">Name</label>
      <input type="text" class="form-control" id="name" placeholder="Name" name="name">
    </div>
    <div class="form-group">
      <label for="mail">Mail</label>
      <input type="email" class="form-control" id="mail" placeholder="Mail" name="mail">
    </div>
    <div class="form-group">
      <label for="desc">Desc</label>
      <textarea class="form-control" id="desc" name="desc" rows="3"></textarea>
    </div>
    <div class="form-group">
      <label for="image">Image</label>
      <input type="file" name="image" class="form-control-file" id="image">
    </div>
    <button type="submit" name="submit" class="btn btn-default">Upload!</button>
  </form>
</div>

</body>
</html>
