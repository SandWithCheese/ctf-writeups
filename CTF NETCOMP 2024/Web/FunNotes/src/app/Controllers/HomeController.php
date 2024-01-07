<?php

namespace App\Controllers;

use App\Controller;
use App\Models\User;

class HomeController extends Controller
{
    public function index()
    {
        if (!isset($_SESSION["login"])){
            $this->redirect("/login");
            exit;
        }

        $this->redirect("/dashboard");
    }

    public function login()
    {
        $this->render("login");
    }

    public function goLogin()
    {
        $new = new User($_POST["username"], $_POST["password"]);
        $user = $new->get();
        if (!$user){
            $this->redirect("/login");
        }

        $_SESSION["username"] = $user[0];
        $_SESSION["role"] = $user[2];
        $_SESSION["login"] = true;

        $this->redirect("/dashboard");
    }

    public function signup()
    {
        $this->render("signup");
    }

    public function goSignup()
    {
        $new = new User($_POST["username"], $_POST["password"]);
        $new->save();
        $this->redirect("/login");
    }

    public function goLogout(){
        session_destroy();
        unset($_SESSION);
        $this->redirect("/login");
    }
}
