#!/usr/bin/python3
# 
# Simple MazeWar Program
# Author: Franklin Reynolds
# Date: Feb 19, 2007
#

from flask import Flask
from flask import jsonify

import random
import thing as THING

app = Flask(__name__)

MSRV = None

class mazesvr:

    import maze
    m = maze.Maze()
    thing = []
    LASTPLAYER = 0
    NumOfPlayers = 7

    def __init__(self):
        random.seed()
        for i in range(1, self.NumOfPlayers):
            self.thing.append( THING.Thing(1, 1, self.m.PLAYER, "Player 1", "", 1) )
            self.m.halls[1][1] = 1
        self.LASTPLAYER = self.NumOfPlayers

        self.thing.append(THING.Thing(1, 5, self.m.GREMLIN, "Gremlin 1", "", 1))
        self.m.halls[1][5] = 8;
        self.thing.append( THING.Thing(7, 3, self.m.GREMLIN, "Gremlin 2", "", 2))
        self.m.halls[7][5] = 9;
        self.thing.append(THING.Thing(13, 13, self.m.GREMLIN, "Gremlin 3", "", 3))
        self.m.halls[13][13] = 10;
        self.thing.append(THING.Thing(13, 5, self.m.GREMLIN, "Gremlin 4", "", 4 ))
        self.m.halls[13][5] = 11;
        self.thing.append(THING.Thing(5, 13, self.m.GREMLIN, "Gremlin 5", "", 1))
        self.m.halls[5][13] = 12;
        self.thing.append(THING.Thing(3, 11, self.m.GREMLIN, "Gremlin 6", "", 2))
        self.m.halls[3][11] = 13;
        self.thing.append(THING.Thing(11, 9, self.m.GREMLIN, "Gremlin 7", "", 3))
        self.m.halls[11][9] = 14;
        self.thing.append(THING.Thing(9, 1, self.m.GREMLIN, "Gremlin 8", "", 4 ))
        self.m.halls[9][1] = 15;
        print("mazesvr view of maze")
        self.m.display()
        return

    def poll( self, player ):
        x = self.thing[player].x
        y = self.thing[player].y
        type = self.thing[player].type
        return x,y,type

    def display(self):
        self.m.display()
        return
    
    def info( self, player ):
        print("player: " + str(player) + ", direction: " + str(self.thing[player].direction) + ", x, y"+ str(self.thing[player].x) + ", " + str(self.thing[player].y))
        return (player, self.thing[player].direction, self.thing[player].x, self.thing[player].y)
    
    def left( self, player ):
        self.thing[player].direction -= 1
        if self.thing[player].direction == 0 :
            self.thing[player].direction = 4

    def right( self, player ):
        self.thing[player].direction += 1
        if self.thing[player].direction == 5 :
            self.thing[player].direction = 1

    def forward( self, player ):
        if self.thing[player].direction == 1:
            if self.m.halls[self.thing[player].x][self.thing[player].y + 1] == 0 :
                self.m.halls[self.thing[player].x][self.thing[player].y + 1] = player 
                self.m.halls[self.thing[player].x][self.thing[player].y] = 0 
                self.thing[player].y += 1
        if self.thing[player].direction == 2:
            if self.m.halls[self.thing[player].x +1][self.thing[player].y] == 0 :
                self.m.halls[self.thing[player].x + 1][self.thing[player].y] = player 
                self.m.halls[self.thing[player].x][self.thing[player].y] = 0 
                self.thing[player].x += 1
        if self.thing[player].direction == 3:
            if self.m.halls[self.thing[player].x][self.thing[player].y - 1] == 0 :
                self.m.halls[self.thing[player].x][self.thing[player].y - 1] = player 
                self.m.halls[self.thing[player].x][self.thing[player].y] = 0 
                self.thing[player].y -= 1
        if self.thing[player].direction == 4:
            if self.m.halls[self.thing[player].x - 1][self.thing[player].y] == 0 :
                self.m.halls[self.thing[player].x - 1][self.thing[player].y] = player 
                self.m.halls[self.thing[player].x][self.thing[player].y] = 0 
                self.thing[player].x -= 1

    def back( self, player ):
        if self.thing[player].direction == 3:
            if self.m.halls[self.thing[player].x][self.thing[player].y + 1] == 0 :
                self.m.halls[self.thing[player].x][self.thing[player].y + 1] = player 
                self.m.halls[self.thing[player].x][self.thing[player].y] = 0 
                self.thing[player].y += 1
        if self.thing[player].direction == 4:
            if self.m.halls[self.thing[player].x +1][self.thing[player].y] == 0 :
                self.m.halls[self.thing[player].x + 1][self.thing[player].y] = player 
                self.m.halls[self.thing[player].x][self.thing[player].y] = 0 
                self.thing[player].x += 1
        if self.thing[player].direction == 1:
            if self.m.halls[self.thing[player].x][self.thing[player].y - 1] == 0 :
                self.m.halls[self.thing[player].x][self.thing[player].y - 1] = player 
                self.m.halls[self.thing[player].x][self.thing[player].y] = 0 
                self.thing[player].y -= 1
        if self.thing[player].direction == 2:
            if self.m.halls[self.thing[player].x - 1][self.thing[player].y] == 0 :
                self.m.halls[self.thing[player].x - 1][self.thing[player].y] = player 
                self.m.halls[self.thing[player].x][self.thing[player].y] = 0 
                self.thing[player].x -= 1

    def view( self, player ):
        direc = self.thing[player].direction
        x = self.thing[player].x
        y = self.thing[player].y
        view = []
        cellnum = 0
        # -1 == ROCK
        DONE = False
        while not DONE:
            # append LEFT, CENTER, RIGHT
            cellnum += 1
            if self.m.halls[x][y] == -1:
                DONE = True
            if direc == 1:
                view.append((str(cellnum),(self.m.halls[x-1][y],self.m.halls[x][y],self.m.halls[x+1][y])))
                y += 1
            elif direc == 2:
                view.append((str(cellnum),(self.m.halls[x][y+1],self.m.halls[x][y],self.m.halls[x][y-1])))
                x += 1
            elif direc == 3:
                view.append((str(cellnum),(self.m.halls[x+1][y],self.m.halls[x][y],self.m.halls[x-1][y])))
                y -= 1
            elif direc == 4:
                view.append((str(cellnum),(self.m.halls[x][y-1],self.m.halls[x][y],self.m.halls[x][y+1])))
                x -= 1
            print("view")
            print(view)

        return view
    
                
@app.route('/')
def hw():
    global MSRV
    
    return 'Hello World'

@app.route('/start')
def start():
    global MSRV
    return "start"

@app.route('/info', methods=["POST"])
def info():
    global MSRV
    v = MSRV.info(1)
    return jsonify(v)

@app.route('/display', methods=["POST"])
def display():
    global MSRV
    v = MSRV.display()
    return "ok"

@app.route('/left', methods=["GET","POST"])
def left():
    global MSRV
    MSRV.left(1)
    v = MSRV.view(1)
    print("jsonify test")
    print(v)
    print("j: " + str(jsonify(v)))
    return jsonify(v)

@app.route('/right', methods = ['GET', 'POST'])
def right():
    global MSRV
    MSRV.right(1)
    v = MSRV.view(1)
    return jsonify(v)

@app.route('/forward', methods=["GET","POST"])
def forward():
    global MSRV
    MSRV.forward(1)
    v = MSRV.view(1)
    return jsonify(v)

@app.route('/back', methods=['POST'])
def back():
    global MSRV
    MSRV.back(1)
    v = MSRV.view(1)
    return jsonify(v)

@app.route('/status')
def status():
    global MSRV
    return "status"

@app.route('/shoot')
def shoot():
    global MSRV
    return "shoot"

def main(argv=None):
    import sys
    import getopt
    global MSRV

    if argv is None:
        argv = sys.argv
    print("mazesrv:just testing")
    MSRV = mazesvr()
    MSRV.m.display()
    app.run(debug=True, host='0.0.0.0')

if __name__ == "__main__":
    main()
