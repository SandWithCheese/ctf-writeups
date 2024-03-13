<?php

class Query
{
    private $store;

    public function __construct($store)
    {
        $this->store = $store;
    }

    public function getAllQuery()
    {
        return $this->store->getAllRecords();
    }

    public function __debugInfo()
    {
        return $this->getAllQuery();
    }
}

?>