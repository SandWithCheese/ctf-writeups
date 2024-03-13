<?php

class Record
{
    private $host;
    private $user;
    private $pass;
    private $db;
    private $tb;
    private $conn;

    public function __construct(string $host, string $user, string $pass, string $db, string $tb)
    {
        $this->host = $host;
        $this->user = $user;
        $this->pass = $pass;
        $this->db = $db;
        $this->tb = $tb;
        $this->conn = new mysqli($this->host, $this->user, $this->pass, $this->db);
    }

    public function getAllRecords()
    {
        $stmt = $this->conn->prepare("SELECT * FROM {$this->tb}");
        $stmt->execute();
        $rows = $stmt->get_result()->fetch_all(MYSQLI_ASSOC);

        return $rows;
    }

    public function __destruct() {
        $this->conn->close();
    }

    public function __wakeup() {
        $this->conn = new mysqli($this->host, $this->user, $this->pass, $this->db);
    }
}

?>