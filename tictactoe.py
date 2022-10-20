from game import make_move, Game, X, O

BOARD_SIZE_X = 6
BOARD_SIZE_Y = 5

game = Game(BOARD_SIZE_X, BOARD_SIZE_Y)
make_move(game, 2, 3, X)
make_move(game, 2, 2, O)
game.run_game()