<?php

namespace App\Models;

class Notes {
    public $title;
    public $text;
    public $owner;

    public function get(){
        if (!file_exists("/var/www/html/notes.json")){
            file_put_contents("/var/www/html/notes.json", json_encode([]));
        }

        $current = json_decode(file_get_contents("/var/www/html/notes.json"));
        return $current;
    }
    
    public function save($title, $text, $owner){

        if (!file_exists("/var/www/html/notes.json")){
            file_put_contents("/var/www/html/notes.json", json_encode([["title" => $title, "text" => $text, "owner" => $owner]]));
        }
        
        else {
            $current = json_decode(file_get_contents("/var/www/html/notes.json"));
            array_push($current, ["title" => $title, "text" => $text, "owner" => $owner]);
            file_put_contents("/var/www/html/notes.json", json_encode($current));
        }
    }

    public function delete($title, $owner){
        if (!file_exists("/var/www/html/notes.json")){
            file_put_contents("/var/www/html/notes.json", json_encode([]));
        }

        $current = json_decode(file_get_contents("/var/www/html/notes.json"));
        foreach ($current as $i => $note){
            if ($note->title === $title && $note->owner === $owner){
                array_splice($current, $i, $i);
                break;
            }
        }

        file_put_contents("/var/www/html/notes.json", json_encode($current));
        
    }

    public function export($owner){
        $current = json_decode(file_get_contents("/var/www/html/notes.json"));
        if (!isset($_COOKIE["lastExport"])){
            $token = $this->create_export();
            setcookie("lastExport", json_encode($token), time() + 300, "/");
            $outputNote = [];
            foreach ($current as $index => $note){
                if ($note->owner === $owner){
                    array_push($outputNote, $note);
                    $this->save_progress($outputNote, $index, $token->token, $token->filepath);
                }
            }
        } else {
            $token = $this->get_progress($_COOKIE["lastExport"]);
            $outputNote = $token->notes;

            for ($i = $token->index; $i < count($current); $i++){
                if ($current[$i]->owner === $owner){
                    array_push($outputNote, $current[$i]);
                    $this->save_progress($outputNote, $i, $token->token, $token->filepath);
                }
            }
        }

        file_put_contents("/var/www/html/public/$token->filepath", json_encode($outputNote));
        unset($_COOKIE["lastExport"]);
        return $token->filepath;
    }

    public function get_progress($session){
        $data_session = json_decode($session);

        if (!file_exists("/var/www/html/progress.json")){
            file_put_contents("/var/www/html/progress.json", "[]");
        }

        $current = json_decode(file_get_contents("/var/www/html/progress.json"));
        $found = 0;
        foreach ($current as $i => $progress){
            if ($progress->token === $data_session->token){
                $found = 1;
                break;
            }
        }

        if (!$found){
            $progress = ["token" => $data_session->token, "filepath" => $data_session->filepath, "notes" => [], "index" => 0 ];
            array_push($current, $progress);
        }

        file_put_contents("/var/www/html/progress.json", json_encode($current));

        return $progress;
    }

    public function save_progress($currentNotes, $index, $token, $filepath = ""){
        if (!file_exists("/var/www/html/progress.json")){
            file_put_contents("/var/www/html/progress.json", "[]");
        }
        
        $current = json_decode(file_get_contents("/var/www/html/progress.json"));
        $found = 0;
        foreach ($current as $i => $progress){
            if ($progress->token === $token){
                $current[$i]->notes = $currentNotes;
                $current[$i]->index = $index;
                $found = 1;
                break;
            }
        }

        if (!$found){
            array_push($current, ["token" => $token, "filepath" => $filepath, "notes" => $currentNotes, "index" => $index ]);
        }

        file_put_contents("/var/www/html/progress.json", json_encode($current));
    }

    function randstr($l = 8)
    {
        $characters = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ';
        $randstring = '';
        for ($i = 0; $i < $l; $i++) {
            $randstring .= $characters[rand(0, strlen($characters))];
        }
        return $randstring;
    }

    public function create_export(){
        $fn = $this->randstr();
        $token = $this->randstr();
        return (object)[
            "filepath" => "export/$fn.json",
            "token" => $token,
            "index" => 0,
            "notes" => []
        ];
    }
}