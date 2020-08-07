#!/usr/bin/python
# 
# Simple MazeWar Program
# Author: Franklin Reynolds
# Date: Feb 19, 2007
#

class Thing:
    x = 0          # x,y current location of thing in maze
    y = 0
    direction = 0  # direction thing is pointing
    score = 0      # how many points thing has accumulated
    hits = 0       # how many times thing has be hit
    state = 0      # current "state": active==1, dead==0
    type = 2       # type of thing: player == 1, gremlin == 2
    name = ''      # this is provided by the client
    team = ''      # this is provided by the client
    id = 0         # this is provided to the client 

    def __init__(self, in_x, in_y, in_type, in_name, in_team, in_direction):
        self.x = in_x
        self.y = in_y
        self.type = in_type
        self.name = in_name
        self.team = in_team
        self.state = 1
        self.direction = in_direction

    def display(self):
        print("player name: ", self.name, " team: ", self.team)
        print(" x: ", self.x, " y: ", self.y, " direction: ", self.direction)
        print("id: ", self.id, " score: ", self.score, " hits: ", self.hits)
        print(" type: ", self.type, " state: ", self.state)
