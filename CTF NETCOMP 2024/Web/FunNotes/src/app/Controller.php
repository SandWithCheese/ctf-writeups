<?php

namespace App;

class Controller
{
    protected function render($view, $data = [])
    {
        extract($data);

        include "Views/$view.php";
    }

    protected function redirect($url)
    {
        header("Location: $url");
        exit;
    }
}
