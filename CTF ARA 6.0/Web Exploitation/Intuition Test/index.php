<?php

error_reporting(0);

class IntuitionTest
{
    public $name;
    public $expected_R;
    public $expected_G;
    public $expected_B;
    public $input_R;
    public $input_G;
    public $input_B;
}

$flag = 'ARA6{fake_flag_bro}';
$message = '';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $name = htmlspecialchars($_POST['name']);
    $input_R = (int) $_POST['input_R'];
    $input_G = (int) $_POST['input_G'];
    $input_B = (int) $_POST['input_B'];

    $obj = new IntuitionTest();
    $obj->name = $name;
    $obj->expected_R = rand(0, 255);
    $obj->expected_G = rand(0, 255);
    $obj->expected_B = rand(0, 255);
    $obj->input_R = $input_R;
    $obj->input_G = $input_G;
    $obj->input_B = $input_B;

    $serialized_obj = base64_encode(serialize($obj));

    if ($obj->expected_R === $obj->input_R && $obj->expected_G === $obj->input_G && $obj->expected_B === $obj->input_B) {
        $message = "You guessed it right, $name! <br><br><br> $flag";
    } else {
        header("Location: index.php?i={$serialized_obj}");
        exit();
    }
} elseif (isset($_GET['i'])) {
    $decoded_input = base64_decode($_GET['i']);
    $obj = unserialize($decoded_input);
    if ($obj instanceof IntuitionTest) {
        $name = $obj->name;
        $obj->expected_R = rand(0, 255);
        $obj->expected_G = rand(0, 255);
        $obj->expected_B = rand(0, 255);

        if ($obj->expected_R === $obj->input_R && $obj->expected_G === $obj->input_G && $obj->expected_B === $obj->input_B) {
            $message = "You guessed it right, $name! <br><br><br> $flag";
        } else {
            $message = "This time your intuition’s wrong...but you’ll figure it out!";
        }
    } else {
        $message = "That’s not quite what we expected.";
    }
}
?>

<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Intuition Test</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            background: url('https://bolprod.com/wp-content/uploads/2022/04/CITY_1_Rocket_Animation.gif') no-repeat center center fixed;
            background-size: cover;
            height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            font-family: 'Press Start 2P', cursive;
            color: white;
            text-align: center;
        }

        .container {
            background: rgba(0, 0, 0, 0.8);
            padding: 20px;
            padding-left: 60px;
            padding-right: 60px;
            border-radius: 10px;
            min-width: 480px;
            width: 36vw;
            border: 8px solid white;
            box-shadow: 4px 4px 0px rgb(197, 16, 82), -4px -4px 0px rgb(73, 110, 255);
        }

        h2 {
            font-size: 20px;
            margin-bottom: 15px;
            text-shadow: 3px 3px 0px black;
        }

        p {
            font-size: 14px;
            margin-bottom: 10px;
        }


        .pixel-flag {
            width: 100px;
            height: auto;
            image-rendering: pixelated;
            filter: grayscale(100%) brightness(3);
            margin-bottom: 15px;
        }

        label {
            display: block;
            margin: 10px 0 5px;
        }

        .slider-container {
            display: flex;
            align-items: center;
            gap: 10px;
        }

        input[type="range"] {
            flex: 1;
            appearance: none;
            height: 10px;
            background: #ccc;
            outline: none;
            border-radius: 5px;
        }

        input[type="range"]::-webkit-slider-thumb {
            appearance: none;
            width: 20px;
            height: 20px;
            background: white;
            border: 3px solid black;
            cursor: pointer;
        }

        input[type="text"] {
            width: 60%;
            padding: 8px;
            border-radius: 5px;
            border: 2px solid white;
            background: black;
            color: white;
            text-align: center;
            font-family: 'Press Start 2P', cursive;
            font-size: 10px;
            margin-bottom: 10px;
        }

        .color-preview {
            margin-top: 10px;
            width: 100%;
            height: 30px;
            border: 3px solid white;
            border-radius: 5px;
            background: rgb(0, 0, 0);
        }

        input[type="submit"] {
            background: #ff005d;
            color: white;
            padding: 10px;
            border: 4px solid white;
            cursor: pointer;
            font-size: 14px;
            margin-top: 15px;
            text-transform: uppercase;
            font-family: 'Press Start 2P', cursive;
            box-shadow: 3px 3px 0px black;
        }

        input[type="submit"]:hover {
            background: rgb(87, 116, 230);
        }
    </style>
</head>

<body>
    <div class="container">
        <img class="pixel-flag"
            src="https://preview.redd.it/37hq4lxo6xf81.gif?width=640&crop=smart&auto=webp&s=6056fab781ba0239d0cff727d59b47e7e94ae88c"
            alt="Pixel Flag">

        <h2>Intuition Test</h2>
        <p>Guess this flag’s color!</p>
        <br>
        <form method="POST">
            <label for="name" style="font-size: 14px">Your Name:</label>
            <input type="text" name="name" required>
            <br>
            <label for="input_R" style="color:rgb(238, 76, 76)">R</label>
            <div class="slider-container">
                <input type="range" name="input_R" id="input_R" min="0" max="255" value="0" oninput="updateColor()">
                <span id="R_value">0</span>
            </div>
            <label for="input_G" style="color:rgb(25, 196, 122)">G</label>
            <div class="slider-container">
                <input type="range" name="input_G" id="input_G" min="0" max="255" value="0" oninput="updateColor()">
                <span id="G_value">0</span>
            </div>
            <label for="input_B" style="color:rgb(67, 107, 218)">B</label>
            <div class="slider-container">
                <input type="range" name="input_B" id="input_B" min="0" max="255" value="0" oninput="updateColor()">
                <span id="B_value">0</span>
            </div>
            <br>
            <p style="font-size: 12px">Color Preview</p>
            <div class="color-preview" id="colorPreview"></div>
            <br>
            <input type="submit" value="Guess">
        </form>
        <br>
        <p><?php echo $message; ?></p>
    </div>

    <script>
        function updateColor() {
            let r = document.getElementById('input_R').value;
            let g = document.getElementById('input_G').value;
            let b = document.getElementById('input_B').value;

            document.getElementById('R_value').innerText = r;
            document.getElementById('G_value').innerText = g;
            document.getElementById('B_value').innerText = b;

            document.getElementById('colorPreview').style.backgroundColor = `rgb(${r}, ${g}, ${b})`;
        }
    </script>
</body>

</html>