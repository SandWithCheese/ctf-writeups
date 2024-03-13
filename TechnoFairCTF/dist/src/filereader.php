<?php

class FileReader
{
    private $file;
    private $whiteList;


    public function __construct(string $file)
    {
        $this->file = $file;
        $this->whiteList = ["credential.php", "filereader.php", "flag.php", "index.php", "login.php", "query.php", "record.php", "user.php"];
    }

    public function __debugInfo()
    {
        if (!in_array($this->file, $this->whiteList)) {
            return ["file" => "Nice Try"];
        }

        return ["file" => file_get_contents($this->file)];
    }
}

?>