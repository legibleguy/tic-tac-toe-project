import time
import sys #this is just to log the prints into a file

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

class gameState:
    def __init__(self, parentBoard, newMove = -1) -> None:
        self.currentBoard: board = parentBoard
        self.move = newMove #remembering the move to compare it with another state's move in case of a tie
        self.heuristic = self.__determine_heuristic()
    
    def get_last_move_sign(self):
        if self.move != -1:
            return self.currentBoard.values[self.move]
        else: return X #if last move is unknown, we'll just return X as a player sign by default
    
    def get_last_move_sign_opponent(self):
        if self.move != -1:
            if self.currentBoard.values[self.move] == X:
                return O
            else: return X
        else: return O #if last move is unknown, we'll just return O as an opponent sign by default

    #if isPlayersTurn is true, we'll be looking for a best solution for X (and vice versa if it's opponent's turn)
    def __determine_heuristic(self):

        mySign = self.get_last_move_sign()
        theirSign = self.get_last_move_sign_opponent()
        
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
    
    #Returns true if the game is over
    def is_terminal(self) -> bool:
        return self.utility() == MAXINT or self.utility() == MININT or self.utility() == 0
        
    def utility(self):

        for s in self.currentBoard.sequences:
            if len(s) >= WIN_SIZE:
                if self.currentBoard.values[s[0]] == self.get_last_move_sign():
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

class Game:
    def __init__(self, boardW, boardH) -> None:
        self.playersTurn = True
        self.__numStatesGenerated = 0

        startBoard = board(boardW, boardH)
        self.currentState = gameState(startBoard)
    
    def get_winner(self):
        for s in self.currentState.currentBoard.sequences:
            if len(s) == WIN_SIZE:
                return self.currentState.currentBoard.get_value_at(s[0])
        return None

    #Determines which player goes next
    def to_move(self):
        if  self.playersTurn == True:
            self.playersTurn = False #Min player's turn
        else:
            self.playersTurn = True #Max player's turn
    
    def minimax(self, isPredictingX: bool, state: gameState, depth: int) -> gameState:
        if state.is_terminal() or depth >= self.get_current_depth_limit():
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
    
    def get_current_depth_limit(self):
        if self.playersTurn: return SEARCH_DEPTH_X
        else: return SEARCH_DEPTH_O
    
    def run_game(self, logIntoFile = True):
        if logIntoFile:
            print("Game reports will be stored in tictactoe_report.log")
            old_stdout = sys.stdout
            log_file = open("tictactoe_report.log","w")
            sys.stdout = log_file

        gameStartTime = time.time()

        print("Starting the game of Tic-Tac-Toe \nInitial state: \n")
        drawBoardValues(self.currentState.currentBoard)
        while not self.currentState.is_terminal():

            if self.playersTurn:
                print("\nX's turn")
            else:
                print("\nO's turn")

            minimaxStartTime = time.time()
            self.currentState = self.minimax(self.playersTurn, self.currentState, 0)
            print("CPU execution time: " + str(round(time.time() - minimaxStartTime, 4)) + " seconds")
            self.to_move()

            print(str(self.__numStatesGenerated) + " nodes generated")
            self.__numStatesGenerated = 0
            drawBoardValues(self.currentState.currentBoard)
            print("\n")
        
        winner = self.get_winner()
        if winner == None: print("\nIt's a tie")
        else: print("\n" + winner + " is the winner")

        print("Total game time: " + str(round(time.time() - gameStartTime, 4)) + " seconds")

        if logIntoFile:
            sys.stdout = old_stdout
            log_file.close()
            print("Game is finished, check the log file")

        

def make_move(inGame: Game, row: int, col: int, sign: boardSign):
    asIndex = inGame.currentState.currentBoard.coord_to_cell(row, col)
    inGame.currentState.currentBoard.set_cell_value(asIndex, sign)