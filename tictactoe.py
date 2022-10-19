from graph import board, boardSign
from game import gameState, Game 
from graphDebug import drawBoardIndeces, drawBoardValues

BOARD_SIZE_X = 6
BOARD_SIZE_Y = 5

game = Game(BOARD_SIZE_X, BOARD_SIZE_Y)
game.run_game()
# drawBoardIndeces(game.initial_state.cur
# rentBoard)
# print(game.actions(game.initial_state))