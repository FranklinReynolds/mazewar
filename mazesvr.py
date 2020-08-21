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
from flask import request

import argparse
import random
import thing as THING

import threading
import time

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

class mazesvr:

    import maze
    m = maze.Maze()
    thing = {}
    LASTPLAYER = 0
    NumOfPlayers = 4

    def __init__(self):
        global NORTH, EAST, SOUTH, WEST

        random.seed()
        # create monsters and players
        count = 1
        self.thing[str(count)] = THING.Thing(1, 1, self.m.PLAYER, "PlayerOne", "", NORTH, count)
        count += 1
        self.thing[str(count)] = THING.Thing(2, 1, self.m.PLAYER, "PlayerTwo", "", EAST, count)
        count += 1
        self.thing[str(count)] = THING.Thing(1, 5, self.m.GREMLIN, "Gremlin 1", "", NORTH, count)
        count += 1
        self.thing[str(count)] = THING.Thing(7, 5, self.m.GREMLIN, "Gremlin 2", "", EAST, count)
        count += 1
        self.thing[str(count)] = THING.Thing(13, 13, self.m.GREMLIN, "Gremlin 3", "", SOUTH, count)
        count += 1
        self.thing[str(count)] = THING.Thing(13, 5, self.m.GREMLIN, "Gremlin 4", "", WEST, count)
        count += 1
        self.thing[str(count)] = THING.Thing(5, 13, self.m.GREMLIN, "Gremlin 5", "", NORTH, count)
        count += 1
        self.thing[str(count)] = THING.Thing(3, 11, self.m.GREMLIN, "Gremlin 6", "", EAST, count)
        count += 1
        self.thing[str(count)] = THING.Thing(11, 9, self.m.GREMLIN, "Gremlin 7", "", SOUTH, count)
        count += 1
        self.thing[str(count)] = THING.Thing(9, 1, self.m.GREMLIN, "Gremlin 8", "", WEST, count)

        #place monsters and players in the maze
        for k,v in self.thing.items():
            self.m.halls[v.x][v.y] = int(k)

        print("mazesvr view of maze")
        self.m.display()
        return

    def hit_thing(self, in_id):
        id = str(in_id)
        self.thing[id].hits += 1
        if self.thing[id].hits > self.thing[id].MAX_HITS:
            self.thing[id].state = 0                   # killed
            self.m.halls[self.thing[id].x][self.thing[id].y] = 0  # remove from maze
            self.thing[id].x = -1
            self.thing[id].y = -1
            return 1
        return 0
                
    def poll( self, in_player ):
        player = str(in_player)
        x = self.thing[player].x
        y = self.thing[player].y
        type = self.thing[player].type
        return x,y,type

    def display(self):
        self.m.display()
        for k,i in self.thing.items():
            print("id: " + str(i.id) + " x,y: " + str(i.x) + ", " + str(i.y) + ", state: " + str(i.state) + ", score: " + str(i.score) + ", hits: " + str(i.hits))
        return
    
    def info( self,in_player ):
        global MSRV
        player = str(in_player)
        v = MSRV.view(player)
        playerdata = {'player_number':player, 'player_id':self.thing[player].id, 'direction': self.thing[player].direction, 'x':self.thing[player].x, 'y':self.thing[player].y, 'hits':self.thing[player].hits, 'score':self.thing[player].score}
        return jsonify((playerdata, v))
    
    def left( self, in_player ):
        player = str(in_player)
        self.thing[player].direction -= 1
        if self.thing[player].direction == 0 :
            self.thing[player].direction = 4

    def right( self, in_player ):
        player = str(in_player)
        self.thing[player].direction += 1
        if self.thing[player].direction == 5 :
            self.thing[player].direction = 1

    def forward( self, in_player ):
        global NORTH, EAST, SOUTH, WEST
        player = str(in_player)
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
            
    def back( self, in_player ):
        global NORTH, EAST, SOUTH, WEST
        player = str(in_player)
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

    def view( self, in_player ):
        global WALL, NORTH, EAST, SOUTH, WEST
        player = str(in_player)
        direc = self.thing[player].direction
        x = self.thing[player].x
        y = self.thing[player].y
        view = []
        cellnum = 0
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


@app.route('/')
def hw():
    global MSRV    
    return 'Hello World'

@app.route('/start')
def start():
    global MSRV
    player = int(request.form['player'])
    return "start"

@app.route('/info', methods=["POST"])
def info():
    global MSRV
    player = int(request.form['player'])
    v = MSRV.info(player)
    return v

@app.route('/display', methods=["POST"])
def display():
    global MSRV
    player = int(request.form['player'])
    v = MSRV.display()
    return "ok"

@app.route('/left', methods=["GET","POST"])
def left():
    global MSRV
    player = int(request.form['player'])
    MSRV.left(player)
    v = MSRV.view(player)
    return jsonify(v)

@app.route('/right', methods = ['GET', 'POST'])
def right():
    global MSRV
    player = int(request.form['player'])
    MSRV.right(player)
    v = MSRV.view(player)
    return jsonify(v)

@app.route('/forward', methods=["GET","POST"])
def forward():
    global MSRV
    player = int(request.form['player'])
    MSRV.forward(player)
    v = MSRV.view(player)
    return jsonify(v)

@app.route('/back', methods=['POST'])
def back():
    global MSRV
    player = int(request.form['player'])
    MSRV.back(player)
    v = MSRV.view(player)
    return jsonify(v)

@app.route('/status')
def status():
    global MSRV
    player = int(request.form['player'])
    return "status"

@app.route('/shoot', methods=['POST'])
def shoot():
    player = int(request.form['player'])
    return shoot_thing(player)

def shoot_thing(shooter):
    r, v = thread_shoot(shooter)
    return jsonify(r, v)

def thread_shoot(in_shooter):
    global MSRV
    shooter = str(in_shooter)

    v = MSRV.view(shooter)
    cno = 0   # cell number of "thing"
    hit = 0
    thing_id = ""
    for d in v:
        if int(d[1][1]) > 0:
            # found something to shoot
            thing_id = str(d[1][1])
            if thing_id == shooter:
                # cannot shoot yourself
                cno += 1
                continue
            hit = 1
            MSRV.hit_thing(int(thing_id))
            if MSRV.thing[str(thing_id)].type == 2:  # gremlin
                MSRV.thing[shooter].score += 1
            elif MSRV.thing[str(thing_id)].type == 1:  # player
                MSRV.thing[shooter].score -= 1
            break
        cno += 1
    state = 1

    if MSRV.thing[thing_id].state == 0: #i.e., dead
        v = MSRV.view(shooter)
    """
    for player in MSRV.thing:
        if str(player.id) == str(thing_id):
            state = player.state
            if state == 0:
                v = MSRV.view(1)
            break
    """
    rtndata = {"hit": hit, "cell_number": cno, "id": thing_id, "type": MSRV.thing[thing_id].type, "state": state}
    return rtndata, v

@app.route('/heartbeat', methods=['POST'])
def heartbeat():
    # any dead monsters need to be resurrected?
    # any monsters want to shoot a player or move?
    global MSRV, EMPTY, GREMLIN, NORTH, EAST, SOUTH, WEST

    for id, thing in MSRV.thing.items():

        if thing.type != GREMLIN:
            continue
        # resurrect if dead and hallway cell is clear
        if thing.state == EMPTY and MSRV.m.halls[7][7] == EMPTY:
            thing.state = 1
            thing.hits = 0
            thing.score = 0
            thing.direction = NORTH
            thing.x = 7
            thing.y = 7
            MSRV.m.halls[7][7] = int(thing.id)
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
                thread_shoot(int(thing.id))
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

@app.before_first_request
def activate_job():
    global HEARTBEAT
    
    def run_job():
        while True:
            time.sleep(HEARTBEAT)
            heartbeat()
            
    if HEARTBEAT == 0:
        return
    thread = threading.Thread(target=run_job)
    thread.start()

def cliparse(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--heartbeat', type=int, default=2, help=' n == seconds between heartbeats; 0 == no heartbeat')
    return parser.parse_args()

def main(argv=None):
    import sys
    global MSRV, HEARTBEAT

    args = cliparse(sys.argv[:1])
    HEARTBEAT = args.heartbeat
    
    #if argv is None:
    #    argv = sys.argv
    MSRV = mazesvr()
    app.run(debug=False, host='0.0.0.0')

if __name__ == "__main__":
    main()
