#!/usr/bin/python3

from tkinter import *
import requests
import re
import json
import time
import sys
import argparse

root = Tk()

PLAYER = 1   #default value

# first, a row for start and stop buttons
fram = Frame(root)
clearbutt = Button(fram, text='Clear')
clearbutt.pack(side=LEFT)
Label(fram,text=' FDRs version of MAZEWAR! ').pack(side=LEFT)
butt = Button(fram, text='Start')
butt.pack(side=RIGHT)
anotherbutt = Button(fram, text='Stop')
anotherbutt.pack(side=RIGHT)

offset = 10
#spacing: 100, 170, 220, 256, 282, 302, 318, 331
roof = [[100 + offset, 100 + offset], [170 + offset, 170 + offset], [220 + offset, 220 + offset], [256 + offset, 256 + offset], [ 282 + offset, 282 + offset], [302 + offset, 302 + offset], [318 + offset, 318 + offset], [ 331 + offset, 331+ offset]]
baseline = (331 * 2) + 5 + offset
    
floor = [[100 + offset, baseline -100], [170 + offset, baseline - 170], [220 + offset, baseline - 220], [256 + offset, baseline - 256], [ 282 + offset, baseline - 282], [302 + offset, baseline - 302], [318 + offset, baseline - 318], [ 331 + offset, baseline - 331]]

def keydown(e):
    global CAN
    #CAN.delete(ALL)
    #print("keydown function")
    if e.char == "l":
        #print("l, i.e., left button")
        left()        
    if e.char == "r":
        right()
    if e.char == "f":
        forward()
    if e.char == "b":
        back()
    if e.char == "x":
        quit_game()
    if e.char == "s":
        shoot()
    if e.char == "g":
        start_game()
    if e.char == "i":
        info()
    if e.char == "d":
        display()
    if e.keysym == "Left":
        left()
    if e.keysym == "Right":
        right()
    if e.keysym == "Up":
        forward()
    if e.keysym == "Down":
        back()
    print("e.keysym : " + str(e.keysym))
    print("button pressed = ", e.char)

# and finally the canvas
CAN = Canvas(root, height=800, width=600)
fram.bind("<KeyPress>", keydown)
fram.pack(side=TOP)
fram.focus_set()
CAN.pack(side=TOP, fill=BOTH, expand=1)

def draw_eye(cno):
    global CAN
    global offset, roof, baseline, floor

    CAN.create_oval(roof[cno][0], roof[cno][1], baseline - floor[cno][0], floor[cno][1], fill='#fff')
    #(ry-fy)*(3/4) + fy
    topy = (roof[cno][1] -floor[cno][1]) * (3/4) + floor[cno][1]
    #(ry-fy)*(1/4) + fy
    bottomy = (roof[cno][1] -floor[cno][1]) * (1/4) + floor[cno][1]
    CAN.create_arc(roof[cno][0], topy, baseline - floor[cno][0], bottomy,start=0, extent=180, style=ARC)
    CAN.create_arc(roof[cno][0], topy, baseline - floor[cno][0], bottomy,start=180, extent=180, style=ARC)
    #(eastx - westx) * (1/4) + westx
    #(eastx - westx) * (3/4) + westx
    irisroofx = (baseline - floor[cno][0] - roof[cno][0]) * (1/4) + roof[cno][0]
    irisfloorx = (baseline - floor[cno][0] - roof[cno][0]) * (3/4) + roof[cno][0]
    CAN.create_oval(irisroofx, topy, irisfloorx, bottomy, fill='#999')
    pupilroofx = (baseline - floor[cno][0] - roof[cno][0]) * (1/3) + roof[cno][0]
    pupilfloorx = (baseline - floor[cno][0] - roof[cno][0]) * (2/3) + roof[cno][0]
    pupiltopy = (roof[cno][1] -floor[cno][1]) * (2/3) + floor[cno][1]
    #(ry-fy)*(1/4) + fy
    pupilbottomy = (roof[cno][1] -floor[cno][1]) * (1/3) + floor[cno][1]
    CAN.create_oval(pupilroofx, pupiltopy, pupilfloorx, pupilbottomy, fill='#000')

def draw_player(cno):
    global CAN
    global offset, roof, baseline, floor

    topy = (roof[cno][1] -floor[cno][1]) * (3/4) + floor[cno][1]
    bottomy = (roof[cno][1] -floor[cno][1]) * (1/4) + floor[cno][1]
    CAN.create_oval(roof[cno][0], roof[cno][1], baseline - floor[cno][0], floor[cno][1], fill='#0ff')
    CAN.create_arc(roof[cno][0], topy, baseline - floor[cno][0], bottomy,start=220, extent=100, style=ARC, width=2)
    # l_eye
    irisroofx = (baseline - floor[cno][0] - roof[cno][0]) * (1/4) + roof[cno][0]
    irisfloorx = (baseline - floor[cno][0] - roof[cno][0]) * (1/3) + roof[cno][0]
    pupiltopy = (roof[cno][1] -floor[cno][1]) * (2/3) + floor[cno][1]
    pupilbottomy = (roof[cno][1] -floor[cno][1]) * (2/3) + floor[cno][1]
    CAN.create_oval(irisroofx, topy, irisfloorx, pupilbottomy, fill='#000')
    # r_eye
    r_irisroofx = (baseline - floor[cno][0] - roof[cno][0]) * (3/4) + roof[cno][0]
    r_irisfloorx = (baseline - floor[cno][0] - roof[cno][0]) * (2/3) + roof[cno][0]
    CAN.create_oval(r_irisroofx, topy, r_irisfloorx, pupilbottomy, fill='#000')
    
    #bottomy = (roof[cno][1] -floor[cno][1]) * (1/4) + floor[cno][1]
    #bottomy = floor[cno][1]
    #CAN.create_arc(roof[cno][0], topy, baseline - floor[cno][0], bottomy,start=0, extent=180, style=CHORD, fill='#00f')
    #headroofx = (baseline - floor[cno][0] - roof[cno][0]) * (1/3) + roof[cno][0]
    #headfloorx = (baseline - floor[cno][0] - roof[cno][0]) * (2/3) + roof[cno][0]
    #CAN.create_oval(headroofx, roof[cno][1], headfloorx, topy, fill='#00f')
"""
    CAN.create_arc(roof[cno][0], topy, baseline - floor[cno][0], bottomy,start=0, extent=180, style=ARC)
    CAN.create_arc(roof[cno][0], topy, baseline - floor[cno][0], bottomy,start=180, extent=180, style=ARC)
    #(eastx - westx) * (1/4) + westx
    #(eastx - westx) * (3/4) + westx
    irisroofx = (baseline - floor[cno][0] - roof[cno][0]) * (1/4) + roof[cno][0]
    irisfloorx = (baseline - floor[cno][0] - roof[cno][0]) * (3/4) + roof[cno][0]
    CAN.create_oval(irisroofx, topy, irisfloorx, bottomy, fill='#999')
    pupilroofx = (baseline - floor[cno][0] - roof[cno][0]) * (1/3) + roof[cno][0]
    pupilfloorx = (baseline - floor[cno][0] - roof[cno][0]) * (2/3) + roof[cno][0]
    pupiltopy = (roof[cno][1] -floor[cno][1]) * (2/3) + floor[cno][1]
    #(ry-fy)*(1/4) + fy
    pupilbottomy = (roof[cno][1] -floor[cno][1]) * (1/3) + floor[cno][1]
    CAN.create_oval(pupilroofx, pupiltopy, pupilfloorx, pupilbottomy, fill='#000')
    """
    
def hit(cno, blinkcount, target):
    global CAN
    global offset, roof, baseline, floor

    if blinkcount < 1:
        draw_eye(cno) if target > 2 else draw_player(cno)
        return
    for i in range(blinkcount):
        CAN.create_oval(roof[cno][0], roof[cno][1], baseline - floor[cno][0], floor[cno][1], fill='#f00')
        CAN.update()
        time.sleep(0.5)
        draw_eye(cno)
        CAN.update()
    return

def show(v):
    #view = json.loads(v)
    view = v
    global CAN
    global offset, roof, baseline, floor
    CAN.delete(ALL)
    cno = 0
    num = 0
    preroofx = offset
    preroofy = offset
    prefloorx = offset
    prefloory = baseline
    monster_list = []
    
    while num < len(view):
        # skip view[0] cuz that contains the player
        # and we only want to draw what is in front of the player
        l = view[num][1][0]
        c = view[num][1][1]
        r = view[num][1][2]
        cno = num

        # wall in center hallway
        if l == -1 and c != -1:
            # draw slanted roof on left
            CAN.create_line(preroofx, preroofy, roof[cno][0], roof[cno][1])
            # floor line
            CAN.create_line(prefloorx, prefloory, floor[cno][0], floor[cno][1])
            # farthest vertical wall line for the cell
            #CAN.create_line(roof[cno][0],roof[cno][1], floor[cno][0], floor[cno][1])
            if view[num -1][1][0] != -1:
                # prev left cell not WALL, so draw beginning of current wall
                CAN.create_line(preroofx, preroofy, prefloorx, prefloory)

        if l != -1 and c == -1 and view[num - 1][1][0] != -1:
            # draw slanted roof on left
            CAN.create_line(preroofx, preroofy, roof[cno][0], preroofy)
            # floor line
            CAN.create_line(prefloorx, prefloory, floor[cno][0], prefloory)
            
        if l != -1 and c != -1:
            # left hallway; horizontal roof line
            CAN.create_line(preroofx, roof[cno][1], roof[cno][0], roof[cno][1])
            # floor line
            CAN.create_line(prefloorx, floor[cno][1], floor[cno][0], floor[cno][1])
            if view[num - 1][1][0] == -1 and cno > 0:
                # prev left cell not WALL, so draw beginning of current wall
                CAN.create_line(preroofx,preroofy, prefloorx, prefloory)
                
        if c == -1 :
            print("draw central wall")
            # draw roof
            CAN.create_line(preroofx, preroofy, baseline - preroofx, preroofy)
            # draw floor
            CAN.create_line(prefloorx, prefloory, baseline - prefloorx, prefloory)
            # draw left veritical edge
            CAN.create_line(preroofx, preroofy,  prefloorx, prefloory)
            # draw right vertical edge
            CAN.create_line(baseline - preroofx, preroofy, baseline - prefloorx, prefloory)
            
        if c > 0 and cno != 0:
            print("draw monster")
            # monster or other player (current player is at home cell)
            #CAN.create_oval(roof[cno][0], roof[cno][1], baseline - floor[cno][0], floor[cno][1], fill='#fff')
            #hit(cno, 0)
            monster_list.append((cno, 0, c))
            
        # wall in center hallway
        if r == -1 and c != -1:
            print("wall to right, no wall in center")
            # slanted roof line
            CAN.create_line(baseline - preroofx, preroofy, baseline - roof[cno][0], roof[cno][1])
            # floor line
            CAN.create_line(baseline - prefloorx, prefloory, baseline - floor[cno][0], floor[cno][1])
            # farthest vertical wall line for the cell
            #CAN.create_line(roof[cno][0],roof[cno][1], floor[cno][0], floor[cno][1])
            if view[num -1][1][2] != -1:
                print("prev right cell not WALL, so draw beginning of current wall")
                #CAN.create_line(baseline - roof[cno][0],roof[cno][1], baseline - floor[cno][0], floor[cno][1])
                CAN.create_line(baseline - preroofx,preroofy, baseline - prefloorx, prefloory)
        if r != -1 and c == -1 and view[num - 1][1][2] != -1:
            print("right NOT wall and center is wall and prev right not wall, parallel hallway")
            # end of hallway
            # draw slanted roof on right
            CAN.create_line(baseline - preroofx, preroofy, baseline - roof[cno][0], preroofy)
            # floor line
            CAN.create_line(baseline - prefloorx, prefloory, baseline - floor[cno][0], prefloory)
        if r != -1 and c != -1:
            print("right not wall, center not wall == right hallway")
            # horizontal roof line
            CAN.create_line(baseline - preroofx, roof[cno][1], baseline - roof[cno][0], roof[cno][1])
            # floor line
            CAN.create_line(baseline - prefloorx, floor[cno][1], baseline - floor[cno][0], floor[cno][1])
            if view[cno - 1][1][2] == -1 and cno > 0:
                print("right cell not WALL and prev right cell WAS wall and not first cell, so draw ending of current wall")
                CAN.create_line(baseline - preroofx, preroofy, baseline - prefloorx, prefloory)
        
        preroofx = roof[cno][0]
        preroofy = roof[cno][1]
        prefloorx = floor[cno][0]
        prefloory = floor[cno][1]
        num += 1
        continue
    
    #drain and display items in  the monster list
    while monster_list:
        m = monster_list.pop()
        hit(m[0],m[1], m[2])

def forward():
    #r = requests.post('http://localhost:5000/forward', data = {'key': 'value'})
    r = requests.post('http://localhost:5000/forward', data = {'player': str(PLAYER)})
    #r = requests.post('http://localhost:5000/forward')
    show(json.loads(r.text))

def left():
    #r = requests.post('http://localhost:5000/forward', data = {'key': 'value'})
    print("left")
    r = requests.post('http://localhost:5000/left', data = {'player': str(PLAYER)})
    print(r.text)
    #show(r.text)
    show(json.loads(r.text))

def right():
    print("right")
    r = requests.post('http://localhost:5000/right', data = {'player': str(PLAYER)})
    show(json.loads(r.text))

def back():
    print("back")
    r = requests.post('http://localhost:5000/back', data = {'player': str(PLAYER)})
    show(json.loads(r.text))
    
def info():
    global CAN
    r = requests.post('http://localhost:5000/info', data = {'player': str(PLAYER)})
    print("info dump")
    print(r.text)
    rtn_args = json.loads(r.text)
    show(rtn_args[1])
    txt = "hits = " + str(rtn_args[0]['hits']) + ', score = ' + str(rtn_args[0]['score'])
    CAN.delete("tmp_txt")
    CAN.create_text(100,750,anchor='sw', text=txt, tag="tmp_txt")
    return

def ping():
    info()
    root.after(1000, ping)
    
def display():
    print("display halls on the server")
    r = requests.post('http://localhost:5000/display', data = {'player': str(PLAYER)})
    
def start():
    mazewar()

def stop():
    return

def clear():
    return

def shoot():
    print("shoot")
    r = requests.post('http://localhost:5000/shoot', data = {'player': str(PLAYER)})
    print(r.text)
    rtn_args = json.loads(r.text)
    if rtn_args[0]['hit'] == 1:
        hit(rtn_args[0]['cell_number'], 1,rtn_args[0]['id'])
        if rtn_args[0]['state'] == 0:
            show(rtn_args[1])
    return

def do_mouse(eventname):
    global CAN

    def mouse_binding(event):
        global CAN
        shoot()
            
    CAN.bind('<Button-1>', mouse_binding)

butt.config(command=start)
anotherbutt.config(command=stop)
clearbutt.config(command=clear)
do_mouse('Button-1')


def cliparse(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--player', type=int, default=1, help=" n == player number (1..7)")
    return parser.parse_args()

def main():
    global root, PLAYER
    args = cliparse(sys.argv[1:])
    PLAYER = args.player
    root.after(1000, ping)
    root.mainloop()

if __name__ == "__main__":
    main()
