#!/bin/bash

cd $(dirname "${BASH_SOURCE[0]}")/src
./create_token.sh
fastapi run chall.py
