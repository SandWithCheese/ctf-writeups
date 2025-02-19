<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Generate Name Card</title>
  <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
</head>
<body>
  <div class="container mt-5">
    <h2 class="text-center">Generate Name Card</h2>
    <form method="POST" action="card.php" class="mt-4">
      <div class="form-group">
        <label for="name">Name</label>
        <input type="text" class="form-control" id="name" name="data[name]" placeholder="Enter your name" required>
      </div>

      <div class="form-group">
        <label for="photo">Photo (URL)</label>
        <input type="text" class="form-control" id="url" name="data[photoUrl]" placeholder="URL" required>
        </select>
      </div>

      <div class="form-group">
        <label for="email">Email</label>
        <input type="text" class="form-control" id="email" name="data[email]" placeholder="Email" required>
        </select>
      </div>

      <div class="form-group">
        <label for="phone">Phone</label>
        <input type="text" class="form-control" id="phone" name="data[phone]" placeholder="Phone" required>
        </select>
      </div>

      <div class="form-group">
        <label for="address">Address</label>
        <input type="text" class="form-control" id="address" name="data[address]" placeholder="Address" required>
        </select>
      </div>

      <button type="submit" class="btn btn-primary btn-block">Generate Name Card</button>
    </form>
  </div>

  <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.3/dist/umd/popper.min.js"></script>
  <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
</body>
</html>