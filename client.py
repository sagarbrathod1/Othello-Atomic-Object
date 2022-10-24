#!/usr/bin/python

import sys
import json
import socket
import math

# game variables
turn = 0
board_width = 8
board_height = 8
me = None

# game constants
DIRECTIONS = [(i, j) for i in range(-1, 2) for j in range(-1, 2) if i != 0 or j != 0]
MIN_MAX_TREE_MAX_DEPTH = 5
MIN_TURNS_CHIP_COUNT = 20

# lists of cells to consider when evaluating the board - initialized when the game starts
corner_positions = []
edge_positions = []
corner_adj_positions = []
middle_positions = []

# weights for board/score evaluations
CORNER = 100000
EDGE = 20
CORNER_ADJ = -100000
MIDDLE = 20
CHIP_COUNT = 10

def initialize(game_data):
    """
    Initializes the game constants/variables and board positions.
    game_data: game data provided by server (decoded JSON string)
    """
    global board_height, board_width, me, corner_positions, edge_positions, corner_adj_positions, middle_positions
    
    board = game_data['board']

    # identify board dimensions
    board_height = len(board)
    board_width = len(board[0])

    # assigned player number for the automated player
    me = game_data['player']
    
    rowBound = [0, board_height - 1]
    colBound = [0, board_width - 1]

    # identify the corners of the board
    corner_positions = [(r, c) for r in rowBound for c in colBound]

    # identify the cells surrounding the 4 corners
    corner_adj_positions = [(r, c) for rowB, colB in [[0, 0], [0, board_width - 2], [board_height - 2, 0], [board_height - 2, board_width - 2]] \
        for r in range(rowB, rowB + 2) \
            for c in range(colB, colB + 2) \
                if (r, c) not in corner_positions]

    # identify the edge cells of the board excluding the corner cells
    edge_positions = [(r, c) for r in range(0, board_height) for c in range(0, board_width) \
        if (r in rowBound or c in colBound) and (r, c) not in corner_positions]

    # identify the 4 center cells in the board
    middle_positions = [(r, c) for r in [board_height//2 - 1, board_height//2] \
            for c in [board_width//2 - 1, board_width//2]]

def eval(board, agent, turn):
    """
    Evaluates the board for the given agent.
    board: (2D array)
    agent: player or opponent (int)
    turn: (int)
    Returns: score (int)
    """
    def check_positions(board, positions, score):
        """
        Helper function to check if the agent is present in any of the positions on the board and returns the associated score for it.
        board: (2D array)
        positions: areas on the board (list of cells/coordinates)
        score: weights for the score scaling (int)
        Returns: score (int)
        """
        if any(board[r][c] == agent for r, c in positions):     # if at least 1 position has an agent present
            return score
        return 0     # else no score to evaluate

    # calculate the evaluation scores for board cell locations 
    result = check_positions(board, corner_positions, CORNER)
    result += check_positions(board, corner_adj_positions, CORNER_ADJ)
    result += check_positions(board, edge_positions, EDGE)

    # if the game still hasn't reached the halfway point, calculate how well the agent is dominating the center of the board
    if turn < MIN_TURNS_CHIP_COUNT:
        result += check_positions(board, middle_positions, MIDDLE)
    else:
        # if we are past the game's halfway point, calculate how much ahead the agent is compared to their opponent
        score_diff = sum(1 if board[r][c] == agent else -1 for r in range(board_height) \
            for c in range(board_width) if board[r][c] != 0)
        result += score_diff * CHIP_COUNT
    
    # if the agent is our opponent, the evaluation score needs to be negative
    if me != agent:
        result = -result

    return result

def is_valid_move(board, agent, move):
    """
    Returns a list of available board positions if the move is valid.
    board: (2D array)
    agent: player or opponent (int)
    move: coordinate (list)
    Returns: all possible opponent positions that can be flipped (list)
    """
    def is_inside(r, c):
        """
        Helper function to check if the coordinates are inside the board.
        r, c = coordinates of the move (ints)
        Returns: (bool)
        """
        return r >= 0 and r < board_height and c >= 0 and c < board_width

    r, c = move

    # collect all the tiles that can be flipped
    opponent_tiles = []

    # the given position should be empty in order to place a chip corresponding to the agent
    if board[r][c] == 0:     
        opponent = get_opponent(agent)

        # we will travel along all directions from the given position until we find a cell which contains agent chip with opponent chips in between
        for delta_r, delta_c in DIRECTIONS:

            # calculate the next cell location in the direction 
            new_r, new_c = r + delta_r, c + delta_c
            
            # collect the tile positions that contain opponent chips
            tiles = []
            while is_inside(new_r, new_c) and board[new_r][new_c] == opponent:
                tiles.append([new_r, new_c])
                new_r, new_c = new_r + delta_r, new_c + delta_c

            # if we find a tile with an agent chip, add the list of tiles collected to the total opponent tiles list
            if is_inside(new_r, new_c) and board[new_r][new_c] == agent: 
                opponent_tiles += tiles

    return opponent_tiles

def pick_max(score, pos, best_score, best_pos, alpha, beta):
    """
    Returns the maximum score and alpha for minimax algorithm.
    score, pos, best_score, best_pos, alpha, beta: (ints)
    Returns: (ints)
    """
    if best_score is None or score > best_score:
        best_score, best_pos = score, pos

    return best_score, best_pos, max(alpha, score), beta

def pick_min(score, pos, best_score, best_pos, alpha, beta):
    """
    Returns the minimum score and beta for minimax algorithm.
    score, pos, best_score, best_pos, alpha, beta: (ints)
    Returns: (ints)
    """
    if best_score is None or score < best_score:
        best_score, best_pos = score, pos

    return best_score, best_pos, alpha, min(beta, score)

def run_minimax(board, depth, agent, turn, alpha, beta):
    """
    Minimax algorithm to find the next best move for the given agent.
    board, depth, agent, turn, alpha, beta: (ints)
    Returns: best score (int) and position (list)
    """
    # identify all valid possible locations on the board the agent could play
    valid_positions = [(r, c) for r in range(board_height) \
        for c in range(board_width) if is_valid_move(board, agent, (r, c))]

    # if there are no positions left to play or the minimax tree has reached its maximum allowed depth, return the board score
    if (not valid_positions or depth == 0):
        return eval(board, agent, turn), None

    # keep track of the best move and best score found so far
    best_move, best_score = None, None 
    
    # the turns are switched each time the opponent plays
    if not me == agent:
        turn += 1
    opponent = get_opponent(agent)

    # select which function to run whether we want to minimize or maximize the result
    minimax_func = pick_max if me == agent else pick_min
    
    # go through each possible location, get the score, and record the best
    for r, c in valid_positions:
        # get positions that would be flipped if this move is played
        positions = is_valid_move(board, agent, (r, c))

        # set the board as if this move was played
        board[r][c] = agent
        for rr, cc in positions:
            board[rr][cc] = agent
        
        # find the minimax for the other agent
        score, _ = run_minimax(board, depth - 1, opponent, turn, alpha, beta)

        # reset the board as if that move was never played
        board[r][c] = 0
        for rr, cc in positions:
            board[rr][cc] = opponent
        if score is None:
            continue

        # check if the latest minimax run found a better score - if so, update accordingly
        best_score, best_move, alpha, beta = \
            minimax_func(score, [r, c], best_score, best_move, alpha, beta)

        # stop search if we reach the alpha-beta pruning values
        if beta <= alpha:
            break

    return best_score, best_move

def get_opponent(agent):
    """
    Determines the opponent for the given agent (player or opponent).
    agent: (int)
    Returns: (int)
    """
    return 3 - agent

def get_move(player, board):
    """
    Calculates the next best move for the player.
    player: (int)
    board: (2D array)
    Returns: coordinates of best move (list)
    """
    score, pos = run_minimax(board, MIN_MAX_TREE_MAX_DEPTH, player, turn, -math.inf, math.inf)

    if score is None:
        print('No best move possible.')
        pos = [-1, -1]

    print(f'{turn}: Move = {pos}, Score = {score}')

    return pos

def prepare_response(move):
    response = '{}\n'.format(move).encode()
    # print('sending {!r}'.format(response))
    return response

if __name__ == "__main__":
    port = int(sys.argv[1]) if (len(sys.argv) > 1 and sys.argv[1]) else 1337
    host = sys.argv[2] if (len(sys.argv) > 2 and sys.argv[2]) else socket.gethostname()
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((host, port))
        data = sock.recv(1024)

        if data:
            initialize(json.loads(str(data.decode('UTF-8'))))

        turn = 0

        while data:
            json_data = json.loads(str(data.decode('UTF-8')))
            board = json_data['board']
            maxTurnTime = json_data['maxTurnTime']
            player = json_data['player']
            # print(player, maxTurnTime, board)

            move = get_move(player, board)
            response = prepare_response(move)
            sock.sendall(response)

            turn += 2
            data = sock.recv(1024)
        print('connection to server closed')
    finally:
        sock.close()
