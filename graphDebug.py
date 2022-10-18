from graph import board

def drawBoardIndeces(inBoard: board):
    count = 0
    toPrint = ""
    for y in range(0, inBoard.h):
        for x in range(0, inBoard.w):
            toPrint += "| " + str(count) + " |\t"
            count += 1
        toPrint += "\n"
    print(toPrint)

def drawBoardValues(inBoard: board):
    count = 0
    toPrint = ""
    for y in range(0, inBoard.h):
        for x in range(0, inBoard.w):
            toPrint += "| " + str(inBoard.getValueAt(count)) + " |\t"
            count += 1
        toPrint += "\n"
    print(toPrint)

