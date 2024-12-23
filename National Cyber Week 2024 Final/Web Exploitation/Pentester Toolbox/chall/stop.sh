#!/bin/bash

docker_compose_path="$(pwd)/chall/docker-compose.yml"
PORT=$1 docker-compose -p $2 -f "${docker_compose_path}" down