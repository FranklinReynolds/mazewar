# mazewar

This version of mazewar has been inspired by my memory of Maze War, the first 3D first-peron shooter. I believe it was developed in the early 1970s (72-73?). Game play was quite simple by tody's standards. Players wander the maze looking for monsters to shoot at. The game used a very simple, tile based movement where players move from tile to tile by moving one step forward or backward at a time. Players can rotate right or left 90 degrees.

For more information, check out the wikipedia article:
https://en.wikipedia.org/wiki/Maze_War

To launch (don't forget source venv/bin/activate) python3 mazasrv.py
followed by python3 client.py

If you want the monsters to move, you need to run the heartbeat.py (python3 heartbeat.py).

Dependencies:
   mazesrv:
     flask
     random
     jsonify
   client:
     requests
     time
     random
     json

To Do:
- refactor everything to make it less horrible	
- back and side views of beholder
- multiple player support
- start/stop
- login/logout
- make port selection optional
- add better wsgi component
- clean up UI
