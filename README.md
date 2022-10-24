# AOthello

I enjoyed this year's Atomic Accelerator challenge. I created a bot to play the game [Othello](https://www.ultraboardgames.com/othello/game-rules.php)!

Please feel free to contact me via the links in my [profile](https://github.com/sagarbrathod1) if you have any questions about the code or how to get the game started.

To begin, clone this repository.

## Usage

Use a terminal/command line tool to invoke the game (this will run my client as a remote player and a random player for the opponent):

    $ java -jar othello.jar --p1-type remote --p2-type random
  
In another terminal, run the client:

    $ python3 client.py

Version of Java used for this project:

    openjdk 17.0.3 2022-04-19
    OpenJDK Runtime Environment Temurin-17.0.3+7 (build 17.0.3+7)
    OpenJDK 64-Bit Server VM Temurin-17.0.3+7 (build 17.0.3+7, mixed mode, sharing)
    
Version of Python used for this project:

    Python 3.10.6

## Game Flow

The game listens for players to connect over tcp sockets by default. You can also specify options to have the game use a built-in player that generates "random" correct moves for either or both players.

The game waits for players to connect. It listens on a tcp server socket for remote players - the `client.py` file contains code for an automated remote player. 

Once both players have connected, it starts asking players for moves. The game keeps track of whose turn it is, sends the correct player the board state, and waits for a response. The game will not ask a player for a move if the player has no valid move available. It expects a response within a given time limit.

The game will detect when a player has won, or when the game ends in a tie.

## Console Run

### Server Side

```
% java -jar othello.jar --p1-type remote --p2-type random
INFO  othello.server.http-server: Started othello http server on port: 8080
INFO  othello.server.text-ui: Player one | Starting...
INFO  othello.server.text-ui: Player two | Starting...
INFO  othello.server.text-ui: Player one | Idle...
INFO  othello.server.text-ui: Player two | Idle...
INFO  othello.server.text-ui: Player two | Connected...
INFO  othello.server.text-ui: Othello | Waiting for clients...
INFO  othello.server.player.remote: Listening for player one on port 1337
INFO  othello.server.text-ui: Player one | Connected...
INFO  othello.server.text-ui: Othello | Running...
INFO  othello.server.text-ui: Player one played: [2 4]
INFO  othello.server.text-ui: Player two played: [4 5]
INFO  othello.server.text-ui: Player one played: [5 2]
INFO  othello.server.text-ui: Player two played: [2 2]
INFO  othello.server.text-ui: Player one played: [2 3]
INFO  othello.server.text-ui: Player two played: [1 2]
INFO  othello.server.text-ui: Player one played: [1 1]
INFO  othello.server.text-ui: Player two played: [2 1]
INFO  othello.server.text-ui: Player one played: [2 0]
INFO  othello.server.text-ui: Player two played: [3 2]
INFO  othello.server.text-ui: Player one played: [0 1]
INFO  othello.server.text-ui: Player two played: [1 3]
INFO  othello.server.text-ui: Player one played: [0 2]
INFO  othello.server.text-ui: Player two played: [1 0]
INFO  othello.server.text-ui: Player one played: [5 5]
INFO  othello.server.text-ui: Player two played: [3 0]
INFO  othello.server.text-ui: Player one played: [2 5]
INFO  othello.server.text-ui: Player two played: [5 3]
INFO  othello.server.text-ui: Player one played: [6 3]
INFO  othello.server.text-ui: Player two played: [3 5]
INFO  othello.server.text-ui: Player one played: [4 2]
INFO  othello.server.text-ui: Player two played: [5 4]
INFO  othello.server.text-ui: Player one played: [4 6]
INFO  othello.server.text-ui: Player two played: [1 4]
INFO  othello.server.text-ui: Player one played: [0 3]
INFO  othello.server.text-ui: Player two played: [0 4]
INFO  othello.server.text-ui: Player one played: [0 5]
INFO  othello.server.text-ui: Player two played: [5 7]
INFO  othello.server.text-ui: Player one played: [3 7]
INFO  othello.server.text-ui: Player two played: [1 6]
INFO  othello.server.text-ui: Player one played: [1 5]
INFO  othello.server.text-ui: Player two played: [7 2]
INFO  othello.server.text-ui: Player one played: [7 3]
INFO  othello.server.text-ui: Player two played: [7 4]
INFO  othello.server.text-ui: Player one played: [0 0]
INFO  othello.server.text-ui: Player two played: [5 6]
INFO  othello.server.text-ui: Player one played: [4 0]
INFO  othello.server.text-ui: Player two played: [4 1]
INFO  othello.server.text-ui: Player one played: [3 1]
INFO  othello.server.text-ui: Player two played: [2 6]
INFO  othello.server.text-ui: Player one played: [5 0]
INFO  othello.server.text-ui: Player two played: [4 7]
INFO  othello.server.text-ui: Player one played: [6 7]
INFO  othello.server.text-ui: Player two played: [3 6]
INFO  othello.server.text-ui: Player one played: [6 5]
INFO  othello.server.text-ui: Player two played: [6 6]
INFO  othello.server.text-ui: Player one played: [6 4]
INFO  othello.server.text-ui: Player two played: [6 2]
INFO  othello.server.text-ui: Player one played: [7 7]
INFO  othello.server.text-ui: Player two played: [7 5]
INFO  othello.server.text-ui: Player one played: [0 7]
INFO  othello.server.text-ui: Player two played: [7 6]
INFO  othello.server.text-ui: Player one played: [1 7]
INFO  othello.server.text-ui: Player two played: [0 6]
INFO  othello.server.text-ui: Player one played: [2 7]
INFO  othello.server.text-ui: Player two played: [5 1]
INFO  othello.server.text-ui: Player one played: [7 1]
INFO  othello.server.text-ui: Player two played: [6 1]
INFO  othello.server.text-ui: Player one played: [6 0]
INFO  othello.server.text-ui: Player two played: [7 0]
INFO  othello.server.text-ui: Othello | Game over...
INFO  othello.server.text-ui: Player One moves: [[2 4] [5 2] [2 3] [1 1] [2 0] [0 1] [0 2] [5 5] [2 5] [6 3] [4 2] [4 6] [0 3] [0 5] [3 7] [1 5] [7 3] [0 0] [4 0] [3 1] [5 0] [6 7] [6 5] [6 4] [7 7] [0 7] [1 7] [2 7] [7 1] [6 0]]
INFO  othello.server.text-ui: Player Two moves: [[4 5] [2 2] [1 2] [2 1] [3 2] [1 3] [1 0] [3 0] [5 3] [3 5] [5 4] [1 4] [0 4] [5 7] [1 6] [7 2] [7 4] [5 6] [4 1] [2 6] [4 7] [3 6] [6 6] [6 2] [7 5] [7 6] [0 6] [5 1] [6 1] [7 0]]
INFO  othello.server.text-ui: Game Result: Player one won
INFO  othello.server.text-ui: Player 1 Score: 52
INFO  othello.server.text-ui: Player 1 Score: 12
INFO  othello.server.text-ui: Final board:
 [[1 1 1 1 1 1 2 1]
 [1 1 2 1 1 2 1 1]
 [1 1 1 1 2 1 1 1]
 [1 1 1 2 1 1 1 1]
 [1 1 2 1 1 1 1 1]
 [1 2 2 1 1 1 2 1]
 [1 2 1 1 1 1 2 1]
 [2 1 1 1 1 1 1 1]]

INFO  othello.server.text-ui: Player one | Disconnected...
INFO  othello.server.text-ui: Othello | Disconnecting players...
INFO  othello.server.text-ui: Player two | Disconnected...
INFO  othello.server.text-ui: Othello | Idle...
INFO  othello.server.text-ui: Player one | Idle...
INFO  othello.server.text-ui: Player two | Idle...
INFO  othello.server.text-ui: Player two | Connected...
INFO  othello.server.text-ui: Othello | Waiting for clients...
INFO  othello.server.player.remote: Listening for player one on port 1337
.
.
.
```

### Client Side

```
% python3 client.py
0: Move = [2, 4], Score = -20
2: Move = [5, 2], Score = -20
4: Move = [2, 3], Score = -20
6: Move = [1, 1], Score = -20
8: Move = [2, 0], Score = -20
10: Move = [0, 1], Score = -20
12: Move = [0, 2], Score = -20
14: Move = [5, 5], Score = 99960
16: Move = [2, 5], Score = 99960
18: Move = [6, 3], Score = 100050
20: Move = [4, 2], Score = 130
22: Move = [4, 6], Score = 100090
24: Move = [0, 3], Score = 100070
26: Move = [0, 5], Score = 100090
28: Move = [3, 7], Score = 100090
30: Move = [1, 5], Score = 100110
32: Move = [7, 3], Score = 100090
34: Move = [0, 0], Score = 100070
36: Move = [4, 0], Score = 100090
38: Move = [3, 1], Score = 100190
40: Move = [5, 0], Score = 100210
42: Move = [6, 7], Score = 100250
44: Move = [6, 5], Score = 100270
46: Move = [6, 4], Score = 100290
48: Move = [7, 7], Score = 100270
50: Move = [0, 7], Score = 100270
52: Move = [1, 7], Score = 100350
54: Move = [2, 7], Score = 100410
56: Move = [7, 1], Score = 420
58: Move = [6, 0], Score = 420
connection to server closed
```

## Options

You can specify that the server should invoke your player, use a "robot" player with a predetermined set of moves, or use a random player for one or both players.

The player can be one of three types:
 * remote - the game will listen for a player to connect to the server
 * random - the game will make a random valid move for the player
 * robot - the game use moves specified in the `--p1-moves` or `--p2-moves` argument
 
The game will log moves to the console and run a webserver at localhost on port 8080 for a UI (http://localhost:8080).
 
Use the `--ui-port` to specify a different UI port.
Pass the `--wait-for-ui` option in order to have the server wait for a UI connection before starting the game.

By default the game will time out if a player has not responeded within 15 seconds.
You can change this with the `--max-turn-time arg` (`--max-turn-time 20000` for 20 seconds).

Options:
```
      --p1-type TYPE          remote     Player one's type - remote, random, or robot
      --p2-type TYPE          remote     Player two's type - remote, random, or robot
      --p1-name NAME          Player One  Player one's team name
      --p2-name NAME          Player Two  Player two's team name
      --p1-moves MOVES        []          Moves for a P1 robot player
      --p2-moves MOVES        []          Moves for a P2 robot player
      --p1-port PORT          1337        Port number for the P1 client
      --p2-port PORT          1338        Port number for the P2 client
      --ui-port PORT          8080        Port number for UI clients
  -w, --wait-for-ui                       Wait for a UI client to connect before starting game
  -m, --min-turn-time MILLIS  1000        Minimum amount of time to wait between turns
  -x, --max-turn-time MILLIS  15000       Maximum amount of time to allow an AI for a turn
  -h, --help
```

## client.py

This file will connect to the game server, analyze the board state, and then send an optimal move.

### _Important Note_

You must start running the game server before instantiating your client from the sdk. If you try to start your client first, it will fail to connect (because the server isn't running) and will not try to reconnect. If you'd like, you can add connection retry functionality to your client, but it isn't necessary for this assessment.

## Moves

When the game server starts, it will wait for players to connect, then begin executing moves until it determines a winner.

When the game server needs a move from your client it will send the game state as JSON, followed by a newline. For example:

`{"board":[[0,0,0,0,0,0,0,0],[0,0,0,0,2,0,0,0],[0,0,0,0,2,0,0,0],[0,0,0,1,2,0,0,0],[0,0,0,1,2,2,0,0],[0,0,0,1,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]],"maxTurnTime":15000,"player":1}\n`

The "board" data structure is a list of game board rows, from the top to the bottom of the game board. A "0" indicates an empty square, a "1" indicates a player one piece, and a "2" indicates a player two piece.

Note the "player" field - read this field to determine if you are player one or player two. Your client should not assume that it always plays as player 1 or 2, however when you test it you as shown above you will explicitly choose which player it is assigned.

When you've computed a move, return it as a JSON array, followed by a newline, for example:

`"[1,2]\n"`

The coordinate system begins at the top left of the board. The coordinates are in [row, column] format. So [7,0] would indicate the lower left corner of the board. [0,0] indicates the top left corner and [7,7] indicates the bottom right corner.

Be sure to terminate your response with the newline, otherwise your move will timeout.

Returning an invalid move will forfeit the game. Timing out (the default timeout is 15 seconds) will also forfeit the game.

## License

Copyright © 2018

Distributed under the Eclipse Public License either version 1.0 or (at
your option) any later version.

