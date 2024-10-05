#!/bin/sh

head -c 32 /dev/urandom | base64 > token.txt
