#!/bin/bash
docker build -t web_asdf .
docker run --name=web_asdf --rm -p5000:5000 -it web_asdf