#!/usr/bin/python
# 
# Simple Heartbeat Program for Mazewar
# Author: Franklin Reynolds
# Date: Aug 11, 2020
# Description: The idea is to ping the Mazewar server so that it
#              can move Gremlins, etc. without player intervention.
#              It also controls the pace at which the Gremlims act.
#
#              python3 heartbeat -r [-1,0,N]
#

import requests
import time
import argparse

def forward():
    #r = requests.post('http://localhost:5000/forward', data = {'key': 'value'})
    r = requests.post('http://localhost:5000/heartbeat')
    print(r.text)

def cliparse(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--repetitions', type=int, default=1, help="N==repeat N times; -1 repeat forever")
    return args
    
def main():
    args = cliparse(sys.argv[1:])
    repetitions = args.repetitions
    count = 0

    while True:
        forward()
        if repetitions == -1:
            continue
        count += 1
        if count < repetitions:
            continue


if __name__ == "__main__":
    main()
