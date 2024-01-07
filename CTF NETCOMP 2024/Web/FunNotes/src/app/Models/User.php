<?php

namespace App\Models;

class User
{
    public $username;
    public $password;

    public function __construct($username, $password)
    {
        $this->username = $username;
        $this->password = $password;
    }

    public function save(){
        $fh = fopen("/var/www/html/user.txt", "a");
        fwrite($fh, "$this->username:$this->password:user\n");
        fclose($fh);
    }

    public function get(){
        $fh = fopen("/var/www/html/user.txt", "r");
        while(!feof($fh)) {
            $cred = fgets($fh);
            if (strpos($cred, "$this->username:$this->password") > -1){
                return explode(":", $cred);
            }
        }   
        return false;
    }
}
