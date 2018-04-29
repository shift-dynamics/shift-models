#!/usr/bin/env python

from subprocess import call
from os import listdir
from os.path import isfile, join

if __name__ == "__main__":

    json_files = [f for f in listdir('.') if isfile(f) and f.split('.')[-1] == 'json']
    for f in json_files:
        call(["./../../../../build/bin/mbdl_cli", f])
        call(["mv", "dhva.dat", f.split('.')[0] + ".dat"])
