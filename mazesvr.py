#!/usr/bin/python3
# 
# Simple MazeWar Program: The Server
# Author: Franklin Reynolds
# Date: Aug 10, 2020
#
# Description: Server implemented using Flask. Exports
#              a "rest" interface. Currently uses port 5000
#
#               Python3 mazesrv.py

from flask import Flask
from flask import jsonify

import random
import thing as THING

app = Flask(__name__)

MSRV = None

WALL = -1
EMPTY = 0
PLAYER = 1
GREMLIN = 2
NORTH = 1
EAST = 2
SOUTH = 3
WEST = 4

print("before class")
class mazesvr:

    import maze
    m = maze.Maze()
    thing = []
    LASTPLAYER = 0
    NumOfPlayers = 7

    def __init__(self):
        global NORTH, EAST, SOUTH, WEST

        random.seed()
        
        for i in range(0, self.NumOfPlayers+1):
            self.thing.append( THING.Thing(1, 1, self.m.PLAYER, "Player"+str(i), "", NORTH, i) )
            self.m.halls[1][1] = 1
        self.LASTPLAYER = self.NumOfPlayers
        count = self.NumOfPlayers + 1
        self.thing.append(THING.Thing(1, 5, self.m.GREMLIN, "Gremlin 1", "", NORTH, count))
        self.m.halls[1][5] = count;
        count += 1
        self.thing.append( THING.Thing(7, 5, self.m.GREMLIN, "Gremlin 2", "", EAST, count))
        self.m.halls[7][5] = count;
        count += 1
        self.thing.append(THING.Thing(13, 13, self.m.GREMLIN, "Gremlin 3", "", SOUTH, count))
        self.m.halls[13][13] = count;
        count += 1
        self.thing.append(THING.Thing(13, 5, self.m.GREMLIN, "Gremlin 4", "", WEST, count))
        self.m.halls[13][5] = count;
        count += 1
        self.thing.append(THING.Thing(5, 13, self.m.GREMLIN, "Gremlin 5", "", NORTH, count))
        self.m.halls[5][13] = count;
        count += 1
        self.thing.append(THING.Thing(3, 11, self.m.GREMLIN, "Gremlin 6", "", EAST, count))
        self.m.halls[3][11] = count;
        count += 1
        self.thing.append(THING.Thing(11, 9, self.m.GREMLIN, "Gremlin 7", "", SOUTH, count))
        self.m.halls[11][9] = count;
        count += 1
        self.thing.append(THING.Thing(9, 1, self.m.GREMLIN, "Gremlin 8", "", WEST, count))
        self.m.halls[9][1] = count;
        count += 1
        print("mazesvr view of maze")
        self.m.display()
        return

    def hit_thing(self, id):
        for thg in self.thing:
            if thg.id == id:
                thg.hits += 1
                if thg.hits > thg.MAX_HITS:
                    thg.state = 0                   # killed
                    self.m.halls[thg.x][thg.y] = 0  # remove from maze
                    thg.x = -1
                    thg.y = -1
                    return 1
        return 0
                
    def poll( self, player ):
        x = self.thing[player].x
        y = self.thing[player].y
        type = self.thing[player].type
        return x,y,type

    def display(self):
        self.m.display()
        for i in self.thing:
            print("id: " + str(i.id) + " x,y: " + str(i.x) + ", " + str(i.y) + ", state: " + str(i.state) + ", hits: " + str(i.hits))
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
        global NORTH, EAST, SOUTH, WEST
        if self.thing[player].direction == NORTH:
            if self.m.halls[self.thing[player].x][self.thing[player].y + 1] == 0 :
                self.m.halls[self.thing[player].x][self.thing[player].y + 1] = player 
                self.m.halls[self.thing[player].x][self.thing[player].y] = 0 
                self.thing[player].y += 1
                return
        if self.thing[player].direction == EAST:
            if self.m.halls[self.thing[player].x +1][self.thing[player].y] == 0 :
                self.m.halls[self.thing[player].x + 1][self.thing[player].y] = player 
                self.m.halls[self.thing[player].x][self.thing[player].y] = 0 
                self.thing[player].x += 1
                return
        if self.thing[player].direction == SOUTH:
            if self.m.halls[self.thing[player].x][self.thing[player].y - 1] == 0 :
                self.m.halls[self.thing[player].x][self.thing[player].y - 1] = player 
                self.m.halls[self.thing[player].x][self.thing[player].y] = 0 
                self.thing[player].y -= 1
                return
        if self.thing[player].direction == WEST:
            if self.m.halls[self.thing[player].x - 1][self.thing[player].y] == 0 :
                self.m.halls[self.thing[player].x - 1][self.thing[player].y] = player 
                self.m.halls[self.thing[player].x][self.thing[player].y] = 0 
                self.thing[player].x -= 1
                return
            
    def back( self, player ):
        global NORTH, EAST, SOUTH, WEST
        
        if self.thing[player].direction == SOUTH:
            if self.m.halls[self.thing[player].x][self.thing[player].y + 1] == 0 :
                self.m.halls[self.thing[player].x][self.thing[player].y + 1] = player 
                self.m.halls[self.thing[player].x][self.thing[player].y] = 0 
                self.thing[player].y += 1
        if self.thing[player].direction == WEST:
            if self.m.halls[self.thing[player].x +1][self.thing[player].y] == 0 :
                self.m.halls[self.thing[player].x + 1][self.thing[player].y] = player 
                self.m.halls[self.thing[player].x][self.thing[player].y] = 0 
                self.thing[player].x += 1
        if self.thing[player].direction == NORTH:
            if self.m.halls[self.thing[player].x][self.thing[player].y - 1] == 0 :
                self.m.halls[self.thing[player].x][self.thing[player].y - 1] = player 
                self.m.halls[self.thing[player].x][self.thing[player].y] = 0 
                self.thing[player].y -= 1
        if self.thing[player].direction == EAST:
            if self.m.halls[self.thing[player].x - 1][self.thing[player].y] == 0 :
                self.m.halls[self.thing[player].x - 1][self.thing[player].y] = player 
                self.m.halls[self.thing[player].x][self.thing[player].y] = 0 
                self.thing[player].x -= 1

    def view( self, player ):
        global WALL, NORTH, EAST, SOUTH, WEST
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
            if self.m.halls[x][y] == WALL:
                DONE = True
            if direc == NORTH:
                view.append((str(cellnum),(self.m.halls[x-1][y],self.m.halls[x][y],self.m.halls[x+1][y])))
                y += 1
            elif direc == EAST:
                view.append((str(cellnum),(self.m.halls[x][y+1],self.m.halls[x][y],self.m.halls[x][y-1])))
                x += 1
            elif direc == SOUTH:
                view.append((str(cellnum),(self.m.halls[x+1][y],self.m.halls[x][y],self.m.halls[x-1][y])))
                y -= 1
            elif direc == WEST:
                view.append((str(cellnum),(self.m.halls[x][y-1],self.m.halls[x][y],self.m.halls[x][y+1])))
                x -= 1

        return view
    
print("before routes")              
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

@app.route('/shoot', methods=['POST'])
def shoot():
    return shoot_thing(1)

def shoot_thing(t):
    global MSRV
    v = MSRV.view(t)
    cno = 0   # cell number of "thing"
    hit = 0
    thing_id = ""
    for d in v:
        if d[1][1] > t:
            thing_id = str(d[1][1])
            hit = 1
            cno = cno
            MSRV.hit_thing(int(d[1][1]))
            break
        cno += 1
    state = 1
    for player in MSRV.thing:
        print("looking for a player.id: " + str(player.id) + ", thing_id: " + str(thing_id))
        
        if str(player.id) == str(thing_id):
            print("found thing: " + str(thing_id))
            state = player.state
            if state == 0:
                v = MSRV.view(1)
            break
    rtndata = {"hit": hit, "cell_number": cno, "id": thing_id, "state": state}
    return jsonify(rtndata, v)

@app.route('/heartbeat', methods=['POST'])
def heartbeat():
    # any dead monsters need to be resurrected?
    # any monsters want to shoot a player or move?
    global MSRV, EMPTY, GREMLIN, NORTH, EAST, SOUTH, WEST

    for thing in MSRV.thing:

        if thing.type != GREMLIN:
            continue
        # resurrect if dead and hallway cell is clear
        if thing.state == EMPTY and MSRV.m.halls[7][7] == EMPTY:
            #print("resurrection should not happen yet!!!!!!!!!!!!!!!")
            thing.state = 1
            thing.hits = 0
            thing.score = 0
            thing.direction = NORTH
            thing.x = 7
            thing.y = 7
            MSRV.m.halls[7][7] = thing.id
            continue
        
        # look down hallway and shoot if gremlin sees a player
        DONE = False
        x = thing.x
        y = thing.y
        shoot_flag = False
        while not DONE:
            if thing.direction == NORTH:
                y += 1
            if thing.direction == EAST:
                x += 1
            if thing.direction == SOUTH:
                y -= 1
            if thing.direction == WEST:
                x -= 1
            if MSRV.m.halls[x][y] == 1:
                shoot_thing(int(thing.id))
                shoot_flag = True
                break
            elif MSRV.m.halls[x][y] != EMPTY:
                break
        if shoot_flag:
            continue

        # if gremlin did not find anything to shoot, look ahead and move
        x = thing.x
        y = thing.y
        if thing.direction == NORTH:
            y += 1
            center = MSRV.m.halls[x][y]
            left =  MSRV.m.halls[x - 1][y]
            right = MSRV.m.halls[x + 1][y]
        if thing.direction == EAST:
            x += 1
            center = MSRV.m.halls[x][y]
            left =  MSRV.m.halls[x ][y + 1]
            right = MSRV.m.halls[x][y - 1]
        if thing.direction == SOUTH:
            y -= 1
            center = MSRV.m.halls[x][y]
            left =  MSRV.m.halls[x + 1][y]
            right = MSRV.m.halls[x - 1][y]
        if thing.direction == WEST:
            x -= 1
            center = MSRV.m.halls[x][y]
            left =  MSRV.m.halls[x][y - 1]
            right = MSRV.m.halls[x][y + 1]
            
        if center != EMPTY:
            # forward is blocked turn left
            MSRV.left(int(thing.id))
            continue
        if left != EMPTY and right != EMPTY:
            #move forward
            MSRV.forward(int(thing.id))
            continue
        
        r = random.random()
        if r < 0.25 and left == EMPTY:
            #move left
            MSRV.left(int(thing.id))
            continue
        if r < 0.25 and right== EMPTY:
            #move right
            MSRV.right(int(thing.id))
            continue
        if center == EMPTY:
            #move forward
            MSRV.forward(int(thing.id))
            continue

    return "Ok"

def main(argv=None):
    import sys
    import getopt
    global MSRV

    if argv is None:
        argv = sys.argv
    MSRV = mazesvr()
    app.run(debug=False, host='0.0.0.0')

if __name__ == "__main__":
    main()
