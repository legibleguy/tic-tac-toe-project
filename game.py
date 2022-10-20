import time
import sys #this will be used to log the prints into a separate file

# This is the main logic for the program. It has two classes Game and gameState. Game handles all of the global functions of the program such as the turn player, the minimax algorithm, the depth of the current player's minimax tree,
# the winner of the game, and logging the game. The gameState class represents a state that keeps track of its heuristic value and the move used to generate it. The program works by passing in the initial gameState into minimax within
# a loop that then recursively gets the best move for the current player by running minimax on the generated children states up to the globally set depths. This loop continues to get the best possible states following the minimax algorithm
# until a winner is determined.

from copy import deepcopy
from graph import board, boardSign
from graphDebug import drawBoardValues

X = boardSign.X
O = boardSign.O
EMPTY = boardSign.EMPTY
MAXINT = 1000
MININT = -1000
SEARCH_DEPTH_X = 2
SEARCH_DEPTH_O = 4
WIN_SIZE = 4

#This class defines the current game state which includes what the board looks like, the heuristic of the board, information about the parent state, available actions of the state, and if the current state has a winner or a tie.
class gameState:
    def __init__(self, parentBoard, newMove = -1) -> None:
        self.currentBoard: board = parentBoard
        self.move = newMove #remembering the move to compare it with another state's move in case of a tie
        self.heuristic = self.__determine_heuristic()
    
    #This function returns either X or O based on who made the last move
    def __get_last_move_sign(self):
        if self.move != -1:
            return self.currentBoard.values[self.move]
        else: return X #if last move is unknown, we'll just return X as player's sign by default
    
    #This function returns either X or O of the agent's opponent based on who made the last move
    def __get_last_move_sign_opponent(self):
        if self.move != -1:
            if self.currentBoard.values[self.move] == X:
                return O
            else: return X
        else: return O #if last move is unknown, we'll just return O as opponent's sign by default

    #This function will take the current board state and calculate a heuristic based on it
    #It will return the calculated heuristic
    def __determine_heuristic(self):

        if self.is_terminal(): return self.__utility()

        mySign = self.__get_last_move_sign()
        theirSign = self.__get_last_move_sign_opponent()
        
        return (
            200 * self.currentBoard.get_num_open_sequences(3, 2, mySign) - 
            80 * self.currentBoard.get_num_open_sequences(3, 2, theirSign) + 
            150 * self.currentBoard.get_num_open_sequences(3, 1, mySign) - 
            40 * self.currentBoard.get_num_open_sequences(3, 1, theirSign) + 
            20 * self.currentBoard.get_num_open_sequences(2, 2, mySign) - 
            15 * self.currentBoard.get_num_open_sequences(2, 2, theirSign) + 
            5 * self.currentBoard.get_num_open_sequences(2, 1, mySign) - 
            2 * self.currentBoard.get_num_open_sequences(2, 1, theirSign)
        )
    
    #Returns true if the game is over in this state
    def is_terminal(self) -> bool:
        return self.__utility() == MAXINT or self.__utility() == MININT or self.__utility() == 0
        
    #Returns a number corresponding to terminal game states. 
    # It will return 1000 if current agent is winning, -1000 if its opponent is winning, 0 for a tie, and None if the game state is not terminal.
    def __utility(self):
        for s in self.currentBoard.sequences:
            if len(s) >= WIN_SIZE:
                if self.currentBoard.values[s[0]] == self.__get_last_move_sign():
                    return MAXINT
                else:
                    return MININT
        if self.currentBoard.get_num_empty_cells() == 0:
            return 0
        return None
    
    #Will travers through all previous moves and find adjacent cells
    #Those adjacent cells represent currently available actions
    def actions(self):
        actions = []
        for cell in self.currentBoard.find_all_filled_cells():
            for row in range(-1, 2):
                for col in range(-1, 2):
                    if row == 0 and col == 0: continue
                    neighbor = self.currentBoard.get_cell_at_dir(cell, row, col)
                    if neighbor != -1 and self.currentBoard.values[neighbor] == EMPTY and neighbor not in actions:
                        actions.append(neighbor)
        
        return actions

# This is the Game class that initializes the game and keeps track of the current game's board state. 
# It also keeps track of whose turn it is and the number of state generated. Game also has many functions that help run the game.
class Game:
    def __init__(self, boardW, boardH) -> None:
        self.__playingAsX = True
        self.__numStatesGenerated = 0

        startBoard = board(boardW, boardH)
        self.currentState = gameState(startBoard)
    
    def get_winner(self):
        for s in self.currentState.currentBoard.sequences:
            if len(s) == WIN_SIZE:
                return self.currentState.currentBoard.get_value_at(s[0])
        return None

    # This function determines which player goes next
    def __to_move(self):
        if  self.__playingAsX == True:
            self.__playingAsX = False #Min player's turn
        else:
            self.__playingAsX = True #Max player's turn
    
    # This function will take in a game object, a boolean if it is predicting X, the current game state, and the current depth
    # This will run through possible game states and chooses the best option for the current player
    # It will also look ahead game states based on who's turn it is
    # This will return the best state
    def minimax(self, isPredictingX: bool, state: gameState, depth: int) -> gameState:
        if state.is_terminal() or depth >= self.__get_current_depth_limit():
            return state

        signToUse: boardSign
        if isPredictingX: 
            signToUse = X
        else: 
            signToUse = O

        bestState = None
        stateToReturn = None
        
        for move in state.actions():
                
                boardToTest = deepcopy(state.currentBoard)
                boardToTest.set_cell_value(move, signToUse)
                nextMoveState = gameState(boardToTest, move)
                self.__numStatesGenerated += 1

                stateToTest = self.minimax(not isPredictingX, nextMoveState, depth + 1)

                #Preserves the current best state as well as the depth 1 state that lead to the best state to be returned for the current players move
                if bestState == None: 
                    bestState = stateToTest
                    stateToReturn = nextMoveState
                else:
                    if stateToTest.heuristic > bestState.heuristic:
                        bestState = stateToTest
                        stateToReturn = nextMoveState
                    
                    #breaking the tie
                    elif stateToTest.heuristic == bestState.heuristic:
                        coord1 = bestState.currentBoard.cell_to_coord(bestState.move)
                        coord2 = stateToTest.currentBoard.cell_to_coord(stateToTest.move)
                        if coord2[1] < coord1[1] and coord2[0] < coord1[0]:
                            bestState = stateToTest
                            stateToReturn = nextMoveState
                            
        return stateToReturn
    
    #This function will return the minimax search depth limit of the current player
    def __get_current_depth_limit(self):
        if self.__playingAsX: return SEARCH_DEPTH_X
        else: return SEARCH_DEPTH_O
    
    #This function will take a game object and run a game
    #It will print out the game's information in tictactoe_report.log
    def run_game(self, logIntoFile = True):
        if logIntoFile:
            print("Game reports will be stored in tictactoe_report.log")
            print("Now give the AI some time to play")

            #creates the log file to write the game to
            old_stdout = sys.stdout
            log_file = open("tictactoe_report.log","w")
            sys.stdout = log_file

        gameStartTime = time.time()

        print("Starting the game of Tic-Tac-Toe \nInitial state: \n")
        drawBoardValues(self.currentState.currentBoard)
        while not self.currentState.is_terminal():

            if self.__playingAsX:
                print("\nX's turn")
            else:
                print("\nO's turn")

            #making the best move with the minimax algorithm
            minimaxStartTime = time.time()
            self.currentState = self.minimax(self.__playingAsX, self.currentState, 0)
            print("CPU execution time: " + str(round(time.time() - minimaxStartTime, 4)) + " seconds")

            #the summary of this turn
            print(str(self.__numStatesGenerated) + " nodes generated")
            self.__numStatesGenerated = 0
            drawBoardValues(self.currentState.currentBoard)
            print("\n")

            #ending this turn
            self.__to_move()
        
        winner = self.get_winner()
        if winner == None: print("\nIt's a tie")
        else: print("\n" + winner + " is the winner")

        print("Total game time: " + str(round(time.time() - gameStartTime, 4)) + " seconds")

        if logIntoFile:
            sys.stdout = old_stdout
            log_file.close()
            print("Game is finished, check the log file")

#Used just for the initializing of the board 
def make_move(inGame: Game, row: int, col: int, sign: boardSign):
    asIndex = inGame.currentState.currentBoard.coord_to_cell(row, col)
    inGame.currentState.currentBoard.set_cell_value(asIndex, sign)