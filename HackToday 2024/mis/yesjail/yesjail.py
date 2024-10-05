#!/usr/bin/env python3

import tempfile
import string
import os

jail = []
jail.append(input())
while jail[-1] != 'EOF':
    jail.append(input())
jail = '\n'.join(jail[:-1])

if '__' in jail or any([c for c in jail if c in string.whitespace.replace('\n', '')+'(){}']) or not all(ord(c) >= 0 and ord(c) <= 255 for c in jail):
    print('yes?')
    exit()

tempfile.tempdir = '/tmp'
with tempfile.TemporaryDirectory() as workdir:
    os.chdir(workdir)
    with open('yes.py', 'w+') as file:
        file.write(jail)
    os.system('python3 yes.py')
