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
    def __init__(self, parentBoard, inDepth = 0, parentState = None) -> None:
        self.parent = parentState
        self.depth = inDepth
        self.currentBoard: board = parentBoard
        self.heuristic = self.determineHeuristic()
        self.move: int #remembering the move to compare it with another state's move in case of a tie

    def getNumOpenSequences(self, seqLen: int, numOpen: int, withSign):
        result = 0
        for i in range(0, len(self.currentBoard.sequences)):
            currSign = self.currentBoard.values[self.currentBoard.sequences[i][0]]
            if currSign == withSign and len(self.currentBoard.sequences[i]) == seqLen:
                if self.currentBoard.sequenceNumOpenSides(i) == numOpen:
                    result += 1
        return result

    def getRootState(self):
        if self.depth == 0: return self
        else:
            return self.parent.getRootState()

    def determineHeuristic(self):
       return 200 * self.getNumOpenSequences(3, 2, X) - 80 * self.getNumOpenSequences(3, 2, O) + 150 * self.getNumOpenSequences(3, 1, X) - 40 * self.getNumOpenSequences(3, 1, O) + 20 * self.getNumOpenSequences(2, 2, X) - 15 * self.getNumOpenSequences(2, 2, O) + 5 * self.getNumOpenSequences(2, 1, X) - 2 * self.getNumOpenSequences(2, 1, O)

class Game:
    def __init__(self, boardW, boardH) -> None:
        self.player = 1
        self.currentPlayerDepth = 0
        self.currentOpponentDepth = 0

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
                    if row == 0 and col == 0: continue
                    neighbor = state.currentBoard.getCellAtDir(cell, row, col)
                    if neighbor != -1 and state.currentBoard.values[neighbor] == EMPTY:
                        actions.append(neighbor)
        
        return actions

    #Determines which player goes next
    def to_move(self):
        if  self.player == 1:
            self.player = 0 #Min player's turn
        else:
            self.player = 1 #Max player's turn

    #Returns true if the game is over
    def is_terminal(self, state: gameState) -> bool:
        if self.utility(state) == MAXINT or self.utility(state) == MININT or self.utility(state) == 0:
            return True
        else: 
            return False
        
    def utility(self, state: gameState):
        for s in state.currentBoard.sequences:
            if len(s) >= WIN_SIZE:
                if state.currentBoard.values[s[0]] == O:
                    return MININT
                else:
                    return MAXINT
        if len(state.currentBoard.findCellsWithSign(EMPTY)) == 0:
            return 0
        return None
    
    def minimax(self, isPlayer: bool, state: gameState, depth: int) -> gameState:
        
        if self.is_terminal(state) or (self.player == 1 and depth >= SEARCH_DEPTH_X) or (self.player == 0 and depth >= SEARCH_DEPTH_O):
            return state

        signToUse: boardSign
        if isPlayer: 
            signToUse = X
            self.currentPlayerDepth = depth + 1
        else: 
            signToUse = O
            self.currentOpponentDepth = depth + 1

        bestState = None
        #stateToReturn = None
        depthToPass = self.currentOpponentDepth
        if not isPlayer: depthToPass = self.currentPlayerDepth
        
        for move in self.actions(state):
                
                boardToTest = deepcopy(state.currentBoard)
                boardToTest.setCellValue(move, signToUse)
                stateToTest = gameState(boardToTest, depth, state)
                stateToTest.move = move
                # nextMoveState = gameState(boardToTest, depth, state)
                # nextMoveState.move = move

                stateToTest = self.minimax(not isPlayer, stateToTest, depthToPass)
                # stateToTest = self.minimax(not isPlayer, nextMoveState, depthToPass)
                #print(stateToTest.depth)

                if bestState == None: bestState = stateToTest
                else:
                    
                    test: bool
                    if isPlayer: test = stateToTest.heuristic > bestState.heuristic
                    else: test = stateToTest.heuristic < bestState.heuristic
                    
                    if test:
                        bestState = stateToTest
                    
                    #breakign the tie
                    elif stateToTest.heuristic == bestState.heuristic:
                        coord1 = bestState.currentBoard.cellToCoord(bestState.move)
                        coord2 = stateToTest.currentBoard.cellToCoord(stateToTest.move)
                        if coord2[1] < coord1[1] and coord2[0] < coord1[0]:
                            bestState = stateToTest
                            #stateToReturn = nextMoveState
                            
        #return stateToReturn
        return bestState

    # def max_value(game, state):
    #     if game.is_terminal(state):
    #         return [game.utility(state, game.player), None]
    #     v = -MAXINT
    #     move = [0,0]
    #     for a in game.actions(state):
    #         [v2, a2] = min_value(game, game.result(state, a))
    #         if v2 > v:
    #             v = v2
    #             move = a
    #     return [v, move]

    # def min_value(game, state):
    #     if game.is_terminal(state):
    #         return [game.utility(state, game.player), None]
    #     v = MAXINT
    #     move = [0,0]
    #     for a in game.actions(state):
    #         [v2, a2] = max_value(game, game.result(state, a))
    #         if v2 < v:
    #             v = v2
    #             move = a
    #     return [v, move]

        
#For terminal nodes, return their utility value: 
#-1000 for lose, 0 for tie, or 1000 for win. 
    
    def run_game(self):
        state = self.initial_state
        player = True
        while not self.is_terminal(state):
            if self.player == 1:
                player = True
            else: player = False
            state.depth = 0
            state = self.minimax(player, state, 0)
            state = state.getRootState()
            self.to_move()
            drawBoardValues(state.currentBoard)