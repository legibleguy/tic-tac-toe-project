from graph import board, boardSign
from graphDebug import drawBoardValues

X = boardSign.X
O = boardSign.O
EMPTY = boardSign.EMPTY
MAXINT = 1000
MININT = -1000
SEARCH_DEPTH = 2
WIN_SIZE = 4 

class gameState:
    def __init__(self, parentBoard) -> None:
        self.currentBoard: board = parentBoard
        self.heuristic = self.determineHeuristic

    def determineHeuristic(self):
        pass

class Game:

    def __init__(self, boardW, boardH) -> None:
        
        self.player = 1

        startBoard = board(boardW, boardH)
        startBoard.setCellValue(startBoard.coordToCell(2, 3), boardSign.X)
        startBoard.setCellValue(startBoard.coordToCell(2, 2), boardSign.O)
        drawBoardValues(startBoard)
        self.initial_state = gameState(startBoard)

    def actions(self, state: gameState):
        actions = []
        for cell in state.currentBoard.findAllFilledCells():
            for row in range(-1, 2):
                for col in range(-1, 2):
                    if state.currentBoard.getCellAtDir(cell, row, col):
                        actions.append(cell)
        
        return actions

    #Determines which player goes next
    def to_move(self):
        if  self.player == 1:
            self.player = 0 #Min player's turn
        else:
            self.player = 1 #Max player's turn

    #Returns true if the game is over
    def is_terminal(self, state) -> bool:
        if state.heuristic == MAXINT or state.heuristic == MININT or len(self.state.findCellsWithSign(EMPTY)) == 0:
            return True
        else: 
            return False
        
    def utility(state, player):
        re
        
        For terminal nodes, return their utility value: 
-1000 for lose, 0 for tie, or 1000 for win. 
    
    def run_game():
        pass

def minimax(game: Game, state: gameState, depth: int) -> gameState:

    game.to_move() #which player is moving next
    
    bestState = minimax(game, state, depth+1)

    return bestState