#!/usr/bin/python
# 
# Simple Heartbeat Program for Mazewar
# Author: Franklin Reynolds
# Date: Aug 11, 2020
# Description: The idea is to ping the Mazewar server so that it
#              can move Gremlins, etc. without player intervention.
#              It also controls the pace at which the Gremlims act.
#
#              python3 heartbeat -r [-1,0,N] -s [1-60 seconds between heartbeats]
#

import requests
import time
import argparse
import sys

def forward():
    #r = requests.post('http://localhost:5000/forward', data = {'key': 'value'})
    r = requests.post('http://localhost:5000/heartbeat')
    print(r.text)

def cliparse(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--repetitions', type=int, default=1, help="N==repeat N times; -1 repeat forever")
    parser.add_argument('-s', '--sleep', type=int, default=1, choices=range(1,60), help="N==number of seconds to sleep between heartbeats")
    return parser.parse_args()
    
def main():
    args = cliparse(sys.argv[1:])
    sleep = args.sleep
    repetitions = args.repetitions
    count = 1

    while True:
        forward()
        time.sleep(sleep)
        if repetitions == -1:
            continue
        count += 1
        if count > repetitions:
            break

if __name__ == "__main__":
    main()
