<?php
function decrypt_flag($encrypted_list, $referrer_list, $date_list)
{
    // Assert length of all arrays are equal
    assert(count($encrypted_list) == count($referrer_list) && count($referrer_list) == count($date_list));

    // Loop through all the arrays
    for ($i = 0; $i < count($encrypted_list); $i++) {
        // Base64 decode the encrypted content
        $ciphertext = base64_decode($encrypted_list[$i]);

        // Create the key from referrer
        $key = md5($referrer_list[$i]);

        // Create IV from date (padded to 16 bytes)
        $iv = str_pad(date("dHis", strtotime($date_list[$i])), 16, date("dHis", strtotime($date_list[$i])));

        // Decrypt using AES-256-CBC
        $decrypted = openssl_decrypt(
            $ciphertext,
            'AES-256-CBC',
            $key,
            OPENSSL_RAW_DATA,
            $iv
        );

        echo $decrypted . "\n";
    }
}

// Example values
$encrypted_list = [
    "3D22URHPkA0BYR43/Jo6BQ==",
    "Bh+U0QUaLYeazZDHVnpFsg==",
    "5nn4BDKuBO/ODKsBJ+6hRA==",
    "Xt9XLFCAkOmsAxNubv7gpQ==",
    "ea7jYh1u/iI0Tlxou/OMeg==",
    "VbSkzpn9AMyG1Bzm3tDW6A==",
    "4Av0gD5AbKbvmjBdvDgyLg==",
    "jVxjiQMGFMIp6ruPqrJxkA==",
    "5i9PQg/ZvsHuIhslQ48vUw==",
    "lEPvrV0xIdIsvfvqEPsjZA==",
    "I8HNOZxsLvX1xsQDjSOgNw==",
    "Oi9vxmwo3HGHqi3zLHhm+g==",
    "s6P9GXrCelfCbjygTsatTQ==",
    "T/AoJBEwr087Lvmy5PioRg==",
    "cc5S6dH5NEToNGxS7hGUCQ==",
    "JlZkIH/bSnMonmHMFf90Bw==",
    "KehZHTmB8+1s3xpJHElH8Q==",
    "ibQPuRVKm7ihCJuDOxmQ3w==",
    "k5DydUeAUFer3qTqdWrSgQ==",
    "p8wU6TWTXa34a3NQjwBhFQ==",
    "aF+HJh6U9hMTdpmt+UVIYA==",
    "8VjSHL/pWdqUm4Lfhn5ibA==",
    "R4Wed8h6NOMXNNASu3eZvg==",
    "9LKQw9RC33MhO8Jp34vv+g==",
    "f5srn9TMn29dUgNlnregow==",
    "RSIwneVkxeZ8iLWOmCXvtg==",
    "b4BgIKgzqsTNFAWCAjS04w==",
    "XGqPT6SJyIgsRi31CDP1xA==",
    "HnBPslnFSBNuZupHP/ZY5Q==",
    "ArOSGpScSDllnFei0lBpsg==",
    "NFMdEEQ4srGqpExOiB4Nxg==",
    "AGYusNShQNzt/iCR3OsJQA==",
    "xCf8uNmverM9gflYQ2W3fA==",
    "bZddubf6z2tqfTC8UeWpiw==",
    "la2sRRqrDx5rn1fNv0KjIw==",
    "jt8NyDfSQ0wU3+wcr63z4Q==",
    "LqtRzclFkmrHXmFXoWrGFA==",
    "nJjJpmBa+6p7S9+tzxOtkA==",
    "DLXzvOZyB6kntA4Qv+rWsg==",
    "E2ACT1lPh/VTnKLqBnCWNA==",
    "AIBJ040oEXjxUgxfMkrptQ==",
    "0fdnVoVzf4wXz6H25hfZRA==",
    "P0ZTxbK2LnnzNlD+OCOa2w==",
    "4obqFOSR2bP5cPOL/ddmGA==",
    "83u7/AoY/lHhEp6byEeLbQ==",
    "6rIMCvtIOg61WdXpG2YdRA==",
    "0pkW/OXFGAah92/H+Br8sw==",
    "BGKVh0HluTfqpcYEjEd/Zw==",
    "ehMkG+fynDJdadCcaHyVBQ==",
    "bj+l+01GKWCmNxm397Y2kA==",
    "sNQTymgoTIPvfsgqPTOkrg==",
    "+2Rk6rbBhD7wzZ22a7Nq0Q==",
    "vHg5eR0W2wYruRF1rmLJWQ==",
    "laAMKwx9ApeT6s/5awebfA==",
    "CbexFlNXakTyRdf0aCwQzw==",
    "cgLpHhVp1F5ECSudL7RwXA==",
    "GHiCPQ+ywkJAwa5JY167vw==",
    "n03MLW6N3gHfTqbDdlRruw==",
    "Dy7M/DrrpLOKR+Y1K5c20Q==",
    "UzTOhqKIN5TgcqTSbRUeow==",
    "3zAQpc6Dm5D6Te45g/jaWg==",
    "FaUqe8Yfe6Jvm3u4uY8X4w==",
    "WMkNEyKtAfFSxRNxixVwTA==",
    "KlsOcCY1g/FIA7oCne2oYw==",
    "2Yp8PyLgRxs/VdqjZob6Eg==",
    "BchdCQtqqfwLClEx+rvP5A==",
    "ong4+eQvVw6CTVpjsefXTg==",
    "2GOp3hhhBXcFxq+3QEgmTw==",
    "3/QnhPGOFdkvv08SjwcglQ==",
    "knTyRWF9OHCMbHylh3LnEg==",
    "ZLS8n3w6GFhfuSIs66/CxA==",
    "fZ3sdVNmA8NcDW1asTNJPQ==",
    "k2M8rzEZneDwed/zVtUDgQ==",
    "tXvKIvSWcpsJHioBbgHsbA==",
    "92/hdFTo7o02GYvWIbM2qw==",
    "zwa+Z0fs/fPDbeXxe8KLfQ==",
    "xp4lZ62VzGOTlTUakEwdOw==",
    "SF7Y+W75v+Jy+x0InxFF0w==",
    "mtJdwyRTXiQdr34m2u8fnw==",
    "oYyrJY5eVd9FiR/I3vGc7g==",
    "1UBtZvXk070VrSuKRuYWLQ==",
    "AIpXdem+B01tYFrrX/elYA==",
    "VAzjTIdVZCAbCLuaBiv2Cg==",
    "gtHIPDZKYI9w08GjLgyE7A==",
    "lUmvA1qDoaWw1ialtrf6LQ==",
    "AWZboBVTgx4EJKXtKY8D8Q==",
    "5wNxn+g0JW7vWy08TEKE9w==",
    "KBtiIPnuOFmxovXLPl2n7Q==",
    "K0xlOP5mltCKeiqDB95cHQ==",
    "oC+W6n6KVRrdfglikXzjYQ==",
    "+uTCEc5pWkLaOqzzEdouMQ==",
    "jnIveA+CezliwvwNf6KWvQ==",
    "lPk+/1u2TJ/TZjTv29MKng==",
    "z4KkNHtdk/+Eub1ADbU0aw==",
    "16tTHJX/mJ4cC8Pj0bz1ww==",
    "AHYiaLCdSA2cLsjhcJ/CrA==",
    "ZFN0lzRK2Ww16dzD1GvMVQ==",
    "V59kM8EiakohJIqnn2ScmQ==",
    "HSnXTj3pNwLV4xzvG7rksA==",
];
$referrer_list = [
    "https://www.bing.com/",
    "https://duckduckgo.com/",
    "https://yahoo.com/",
    "https://www.bing.com/",
    "https://www.google.com/",
    "https://example.com/",
    "https://www.google.com/",
    "https://www.google.com/",
    "https://duckduckgo.com/",
    "https://duckduckgo.com/",
    "https://duckduckgo.com/",
    "https://example.com/",
    "https://duckduckgo.com/",
    "https://example.com/",
    "https://www.bing.com/",
    "https://example.com/",
    "https://duckduckgo.com/",
    "https://www.google.com/",
    "https://www.google.com/",
    "https://example.com/",
    "https://example.com/",
    "https://www.google.com/",
    "https://yahoo.com/",
    "https://example.com/",
    "https://duckduckgo.com/",
    "https://www.google.com/",
    "https://duckduckgo.com/",
    "https://example.com/",
    "https://duckduckgo.com/",
    "https://www.bing.com/",
    "https://yahoo.com/",
    "https://yahoo.com/",
    "https://www.bing.com/",
    "https://www.google.com/",
    "https://www.bing.com/",
    "https://example.com/",
    "https://yahoo.com/",
    "https://example.com/",
    "https://www.bing.com/",
    "https://yahoo.com/",
    "https://www.bing.com/",
    "https://example.com/",
    "https://www.bing.com/",
    "https://www.bing.com/",
    "https://example.com/",
    "https://duckduckgo.com/",
    "https://example.com/",
    "https://www.bing.com/",
    "https://www.google.com/",
    "https://yahoo.com/",
    "https://www.bing.com/",
    "https://duckduckgo.com/",
    "https://yahoo.com/",
    "https://www.google.com/",
    "https://duckduckgo.com/",
    "https://yahoo.com/",
    "https://duckduckgo.com/",
    "https://www.google.com/",
    "https://yahoo.com/",
    "https://example.com/",
    "https://yahoo.com/",
    "https://yahoo.com/",
    "https://www.google.com/",
    "https://yahoo.com/",
    "https://www.bing.com/",
    "https://duckduckgo.com/",
    "https://duckduckgo.com/",
    "https://example.com/",
    "https://yahoo.com/",
    "https://duckduckgo.com/",
    "https://yahoo.com/",
    "https://www.google.com/",
    "https://duckduckgo.com/",
    "https://www.google.com/",
    "https://example.com/",
    "https://duckduckgo.com/",
    "https://www.google.com/",
    "https://yahoo.com/",
    "https://duckduckgo.com/",
    "https://www.bing.com/",
    "https://www.bing.com/",
    "https://yahoo.com/",
    "https://www.google.com/",
    "https://example.com/",
    "https://www.bing.com/",
    "https://www.bing.com/",
    "https://www.google.com/",
    "https://example.com/",
    "https://yahoo.com/",
    "https://example.com/",
    "https://www.bing.com/",
    "https://www.google.com/",
    "https://yahoo.com/",
    "https://yahoo.com/",
    "https://www.google.com/",
    "https://example.com/",
    "https://www.google.com/",
    "https://example.com/",
    "https://www.google.com/",
];

$date_list = [
    "2025-01-23 05:27:00",
    "2025-01-23 05:27:04",
    "2025-01-23 05:27:09",
    "2025-01-23 05:27:12",
    "2025-01-23 05:27:18",
    "2025-01-23 05:27:21",
    "2025-01-23 05:27:27",
    "2025-01-23 05:27:28",
    "2025-01-23 05:27:31",
    "2025-01-23 05:27:33",
    "2025-01-23 05:27:38",
    "2025-01-23 05:27:42",
    "2025-01-23 05:27:46",
    "2025-01-23 05:27:48",
    "2025-01-23 05:27:51",
    "2025-01-23 05:27:53",
    "2025-01-23 05:27:54",
    "2025-01-23 05:27:57",
    "2025-01-23 05:27:59",
    "2025-01-23 05:28:03",
    "2025-01-23 05:28:07",
    "2025-01-23 05:28:11",
    "2025-01-23 05:28:14",
    "2025-01-23 05:28:18",
    "2025-01-23 05:28:21",
    "2025-01-23 05:28:24",
    "2025-01-23 05:28:25",
    "2025-01-23 05:28:27",
    "2025-01-23 05:28:28",
    "2025-01-23 05:28:30",
    "2025-01-23 05:28:35",
    "2025-01-23 05:28:37",
    "2025-01-23 05:28:39",
    "2025-01-23 05:28:41",
    "2025-01-23 05:28:42",
    "2025-01-23 05:28:45",
    "2025-01-23 05:28:49",
    "2025-01-23 05:28:50",
    "2025-01-23 05:28:53",
    "2025-01-23 05:28:54",
    "2025-01-23 05:28:57",
    "2025-01-23 05:29:00",
    "2025-01-23 05:29:04",
    "2025-01-23 05:29:06",
    "2025-01-23 05:29:09",
    "2025-01-23 05:29:10",
    "2025-01-23 05:29:14",
    "2025-01-23 05:29:17",
    "2025-01-23 05:29:19",
    "2025-01-23 05:29:21",
    "2025-01-23 05:29:23",
    "2025-01-23 05:29:26",
    "2025-01-23 05:29:28",
    "2025-01-23 05:29:31",
    "2025-01-23 05:29:32",
    "2025-01-23 05:29:34",
    "2025-01-23 05:29:36",
    "2025-01-23 05:29:38",
    "2025-01-23 05:29:39",
    "2025-01-23 05:29:41",
    "2025-01-23 05:29:43",
    "2025-01-23 05:29:46",
    "2025-01-23 05:29:50",
    "2025-01-23 05:29:53",
    "2025-01-23 05:29:55",
    "2025-01-23 05:29:59",
    "2025-01-23 05:30:02",
    "2025-01-23 05:30:03",
    "2025-01-23 05:30:07",
    "2025-01-23 05:30:08",
    "2025-01-23 05:30:12",
    "2025-01-23 05:30:16",
    "2025-01-23 05:30:18",
    "2025-01-23 05:30:21",
    "2025-01-23 05:30:23",
    "2025-01-23 05:30:25",
    "2025-01-23 05:30:28",
    "2025-01-23 05:30:31",
    "2025-01-23 05:30:34",
    "2025-01-23 05:30:37",
    "2025-01-23 05:30:40",
    "2025-01-23 05:30:44",
    "2025-01-23 05:30:50",
    "2025-01-23 05:30:56",
    "2025-01-23 05:31:00",
    "2025-01-23 05:31:03",
    "2025-01-23 05:31:10",
    "2025-01-23 05:31:13",
    "2025-01-23 05:31:16",
    "2025-01-23 05:31:18",
    "2025-01-23 05:31:20",
    "2025-01-23 05:31:24",
    "2025-01-23 05:31:25",
    "2025-01-23 05:31:27",
    "2025-01-23 05:31:31",
    "2025-01-23 05:31:33",
    "2025-01-23 05:31:38",
    "2025-01-23 05:31:42",
    "2025-01-23 05:31:45",
];

decrypt_flag($encrypted_list, $referrer_list, $date_list);
