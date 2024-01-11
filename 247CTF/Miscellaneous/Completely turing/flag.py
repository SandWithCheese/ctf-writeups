import subprocess
from string import ascii_uppercase

for i in ascii_uppercase:
    for j in ascii_uppercase:
        print(repr("printf '" + i + "\n" + j + "\n' | beef completely_turing"))
