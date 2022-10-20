from game import make_move, Game, X, O

#This creates a Game object with the specified dimensions
game = Game(6, 5)

#Point (2,3) is basically point (3,4) from the homework outline. 
#Our board starts at point (0,0) so we have to use one number less for both X and Y
#Same deal with point (2,2) - this is basically point (3,3) if the board started at point (1,1

#Now we set the initial game configuration
make_move(game, 2, 3, X)
make_move(game, 2, 2, O)

#Now we run the game using the set configurations
game.run_game()