#!/bin/bash
sudo docker rm -f web_image_vault
sudo docker build -t web_image_vault .
sudo docker run -d --name=web_image_vault --rm -p1337:1337 -it web_image_vault  