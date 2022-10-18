from copy import deepcopy
import random
from graph import board, boardSign
from graphDebug import drawBoardValues, drawBoardIndeces

X = boardSign.X
O = boardSign.O
EMPTY = boardSign.EMPTY
BOARD_SIZE_X = 6
BOARD_SIZE_Y = 5
SEARCH_DEPTH = 2
WIN_SIZE = 4


class state:
    def __init__(self, inBoard: board) -> None:
        self.currBoard: board = inBoard

        self.Owins: bool = False
        self.Xwins: bool = False
        self.heuristic: float

        for s in self.currBoard.sequences:
            if len(s) >= WIN_SIZE:
                if self.currBoard.values[s[0]] == O:
                    self.Owins = True
                else:
                    self.Xwins = True
                break
        
        self.__updateHeuristic__()
    
    def __updateHeuristic__(self):
        if self.Xwins: self.heuristic = 1000
        elif self.Owins: self.heuristic = -1000
        elif len(self.currBoard.findCellsWithSign(EMPTY)) == 0: return 0
        else:
            self.heuristic = (
                200 * self.getNumOpenSequences(3, 2, X) -
                80 * self.getNumOpenSequences(3, 2, O) +
                150 * self.getNumOpenSequences(3, 1, X) -
                40 * self.getNumOpenSequences(3, 1, O) +
                20 * self.getNumOpenSequences(2, 2, X) -
                15 * self.getNumOpenSequences(2, 2, O) +
                5 * self.getNumOpenSequences(2, 1, X) -
                2 * self.getNumOpenSequences(2, 1, O)
            )
    
    def isTerminal(self) -> bool:
        return self.Xwins or self.Owins or len(self.currBoard.findCellsWithSign(EMPTY)) == 0

    def getNumOpenSequences(self, seqLen: int, numOpen: int, withSign):
        result = 0
        for i in range(0, len(self.currBoard.sequences)):
            currSign = self.currBoard.values[self.currBoard.sequences[i][0]]
            if currSign == withSign and len(self.currBoard.sequences[i]) == seqLen:
                if self.currBoard.sequenceNumOpenSides(i) == numOpen:
                    result += 1
        return result

def expandState(isPlayer: bool, currState: state, depth: int = 0) -> state:
    if depth >= SEARCH_DEPTH or currState.isTerminal(): return currState

    sign = O
    if isPlayer: sign = X

    newStates = []
    heuristics = []

    
    for cell in currState.currBoard.findCellsWithSign(EMPTY):
        newBoard = deepcopy(currState.currBoard)
        newBoard.setCellValue(cell, sign)
        newState = state(newBoard)
        
        expanded = expandState(not isPlayer, newState, depth+1)
        newStates.append(expanded)
        heuristics.append(expanded.heuristic)
    
    targetValue: float
    if isPlayer: targetValue = max(heuristics)
    else: targetValue = min(heuristics)

    suitableNodes = []

    for i in range (0, len(heuristics)):
        if heuristics[i] == targetValue:
            suitableNodes.append(i)
    
    return newStates[random.choice(suitableNodes)]

startBoard = board(BOARD_SIZE_X, BOARD_SIZE_Y)
startBoard.setCellValue(startBoard.coordToCell(2, 3), X) #coordinate (2,3) is basically (3,4) because our start point is (0,0)
drawBoardValues(startBoard)

game = state(startBoard)
game = expandState(False, game, 1)

while not game.isTerminal():
    game = expandState(True, game, 0)

drawBoardValues(game.currBoard)
if game.Owins:
    print("opponent wins")
elif game.Xwins:
    print("player wins")
else:
    print("tie")
