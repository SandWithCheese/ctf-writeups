<?php

$conn = mysqli_connect('127.0.0.1', 'username', 'password', 'secret');

$sql = "CREATE TABLE IF NOT EXISTS `user` (
    `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
    `username` varchar(255) DEFAULT NULL,
    `password` varchar(255) DEFAULT NULL,
    `email` varchar(255) DEFAULT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;";

$conn->query($sql);
$checklength = "SELECT COUNT(*) FROM user";
$result = $conn->query($checklength);
$length = $result->fetch_row()[0];

if ($length == 0) {
    $sql = "INSERT INTO user (username, password, email) VALUES ('adminSolid', 'sUp3rs3cr3tBR0WnoneC4nthack', 'admin@localhost')";
    $conn->query($sql);
}

$sql = "CREATE TABLE IF NOT EXISTS `post` (
    `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
    `judul` varchar(255) DEFAULT NULL,
    `konten` text,
    `tanggal` datetime DEFAULT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;";

$conn->query($sql);
$checklength = "SELECT COUNT(*) FROM post";
$result = $conn->query($checklength);
$length = $result->fetch_row()[0];

if ($length == 0) {
    $sql = "INSERT INTO post (judul, konten, tanggal) 
    VALUES 
    ('CTF TECHCOMFEST 2024', 'Techcomfest adalah salah satu wujud misi dan peran aktif UKM Polytechnic Computer Club dalam mengikuti perkembangan teknologi dalam bidang IT. Dengan diadakannya kegiatan Techcomfest, diharapkan siswa/i SMA/SMK sederajat dan Mahasiswa/i dapat menyalurkan inovasi dan kreativitas mereka khususnya dalam bidang teknologi dan informasi.\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', NOW()),
    ('CTF SLASHROOT 2024', 'Slashroot CTF 8.0 adalah kompetisi Cyber Security tingkat nasional yang diselenggarakan oleh Unit Kegiatan Mahasiswa Kelompok Studi Linux ITB STIKOM Bali. Kami hadir guna meningkatkan edukasi mengenai keamanan siber di Indonesia. Kompetisi akan dilaksanakan menggunakan format perlombaan Capture The Flag dengan kategori soal jeopardy. Setiap tim dengan jumlah maksimal 3 orang akan menyelesaikan berbagai tantangan untuk memperoleh poin tertinggi.\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', NOW()),
    ('CTF DTS TSA', 'Program Talent Scouting Academy (TSA) adalah rangkaian program pengembangan kompetensi bidang teknologi informasi dan komunikasi (TIK) bagi mahasiswa aktif yang sejalan dengan Program \"Merdeka Belajar Kampus Merdeka\" Kementerian Pendidikan, Kebudayaan, Riset, dan Teknologi. TSA memberikan kesempatan bagi para mahasiswa untuk belajar di luar kampus melalui pelatihan yang diselenggarakan secara daring/luring yang meliputi pelatihan technical skills yang berorientasi pada project. Tidak hanya pelatihan, TSA juga menawarkan kesempatan uji kompetensi/sertifikasi global bagi mahasiswa yang memenuhi kriteria tertentu. \n\n\n\n\n\n\n\n\n\n', NOW()),
    ('Filosofi Bendera', 'Benderanya adalah simbol kekuatan dan kebijaksanaan dari komunitas ini. Bendera ini melambangkan sesuatu yang lebih dari sekedar simbol. Di baliknya terdapat nilai-nilai yang sangat penting untuk dipahami oleh setiap orang yang terlibat dalam sistem ini. Hanya admin yang dapat mengakses informasi lebih dalam tentang bendera ini, karena peran admin sangat vital dalam menjaga integritas dan keamanan dari sistem yang ada. Jangan coba-coba untuk memanipulasi atau mencoba mengambil alih bendera ini, karena konsekuensinya bisa sangat berbahaya.\n\n\n\n\n\n\n\n\n\n', NOW());";
    $conn->query($sql);
}
