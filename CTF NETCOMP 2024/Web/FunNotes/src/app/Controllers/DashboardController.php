<?php

namespace App\Controllers;

use App\Controller;
use App\Models\Notes;

class DashboardController extends Controller {
    public function __construct(){
        if (!isset($_SESSION["login"])){
            $this->redirect("/login");
            exit;
        }
    }
    public function index()
    {
        $notes = new Notes();
        $this->render("dashboard", ["notes" => $notes->get()]);
    }

    public function create_notes()
    {
        $title = $_POST["title"];
        $text = $_POST["text"];
        $owner = $_SESSION["username"];

        if ($_SESSION["role"] === "mod"){
            $note = new Notes();
            $note->save($title, $text, $owner);
        }

        $this->redirect("/dashboard");
    }

    public function delete_notes()
    {
        $notes = new Notes();
        $notes->delete($_GET["title"], $_SESSION["username"]);

        $this->redirect("/dashboard");
    }

    public function export_notes()
    {
        $notes = new Notes();
        $filepath = $notes->export($_SESSION["username"]);

        if (file_exists($filepath)){
            $output = file_get_contents($filepath);

            header('Content-Description: File Transfer');
            header('Content-Type: application/octet-stream');
            header('Content-Disposition: attachment; filename=output.json');
            header('Expires: 0');
            header('Cache-Control: must-revalidate');
            header('Pragma: public');
            header('Content-Length: ' . strlen($output));

            echo $output;
        }

        $this->redirect("/dashboard");
    }
}
