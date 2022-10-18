from graph import board, boardSign
from game import gameState, Game 
from graphDebug import drawBoardIndeces, drawBoardValues

BOARD_SIZE_X = 6
BOARD_SIZE_Y = 5

def max_value(game, state):
    if game.is_terminal(state):
        return [game.utility(state, game.player), None]
    v = -MAXINT
    move = [0,0]
    for a in game.actions(state):
        [v2, a2] = min_value(game, game.result(state, a))
        if v2 > v:
            v = v2
            move = a
    return [v, move]

def min_value(game, state):
    if game.is_terminal(state):
        return [game.utility(state, game.player), None]
    v = MAXINT
    move = [0,0]
    for a in game.actions(state):
        [v2, a2] = max_value(game, game.result(state, a))
        if v2 < v:
            v = v2
            move = a
    return [v, move]


game = Game(BOARD_SIZE_X, BOARD_SIZE_Y)
game.run_game()