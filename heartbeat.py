#!/usr/bin/python
# 
# Simple MazeWar Program
# Author: Franklin Reynolds
# Date: Feb 19, 2007
#

import requests
import time

def forward():
    #r = requests.post('http://localhost:5000/forward', data = {'key': 'value'})
    r = requests.post('http://localhost:5000/heartbeat')
    print(r.text)

def main():
    forward()

if __name__ == "__main__":
    main()
