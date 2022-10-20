from enum import Enum

class boardSign(Enum):
    EMPTY = 0,
    X = 1,
    O = 2

signValues = {
    boardSign.EMPTY : " ",
    boardSign.X : "X",
    boardSign.O : "O"
}

class board:
    def __init__(self, width, height) -> None:
        self.w = width
        self.h = height
        self.values = [boardSign.EMPTY] * (width*height)
        self.sequences = []

    def find_all_filled_cells(self):
        result = []
        for cell in range(0, len(self.values)):
            if self.values[cell] != boardSign.EMPTY:
                result.append(cell)

        return result
    
    def get_num_empty_cells(self):
        count = 0
        for cell in self.values:
            if cell == boardSign.EMPTY: count += 1
        return count
    
    def get_value_at(self, idx: int) -> str:
        if idx < len(self.values):
            return signValues[self.values[idx]]
        else: return " "
    
    def set_cell_value(self, cell, sign = boardSign.X):
        if cell < len(self.values) and self.values[cell] != sign:
            self.values[cell] = sign
            self.__sequence_check(cell, sign)
            
    #check for neighbours and remember sequences on the board
    def __sequence_check(self, atCell: int, sign: boardSign):
        sequencesModified = []
        for row in range(-1,2): 
            for col in range(-1,2):
                if row == 0 and col == 0: continue
                neighb = self.get_cell_at_dir(atCell, row, col)
                if neighb != -1 and self.values[neighb] == sign:
                    newSequence = True
                    for s in range(0, len(self.sequences)):
                        if neighb in self.sequences[s]:
                            direction = self.__get_sequence_direction(s)

                            if direction == max(atCell, neighb) - min(atCell, neighb):

                                if atCell > self.sequences[s][len(self.sequences[s])-1]:
                                    self.sequences[s].append(atCell)
                                elif atCell < self.sequences[s][0]:
                                    self.sequences[s].insert(0, atCell)
                                else:
                                    self.sequences[s].insert(len(self.sequences[s])-2, atCell)

                                newSequence = False
                                sequencesModified.append(s)
                                break
                    
                    if newSequence: 
                        self.sequences.append([min(atCell, neighb), max(atCell, neighb)])
                        sequencesModified.append(len(self.sequences)-1)
        
        #merging sequences where start == end and direction is equal
        toRemove = []
        for s in sequencesModified:
            for otherS in sequencesModified:
                if s == otherS: continue
                tailIsHead = self.sequences[s][len(self.sequences[s])-1] == self.sequences[otherS][0]
                sameDirection = self.__get_sequence_direction(s) == self.__get_sequence_direction(otherS)
                if  tailIsHead and sameDirection:
                    self.sequences[otherS].pop(0)
                    toRemove.append(otherS)
                    self.sequences[s] = self.sequences[s] + self.sequences[otherS]
        
        #cleaning up 
        toRemove.sort()
        for i in reversed(range(0, len(toRemove))):
            self.sequences.pop(toRemove[i])

    
    def __get_sequence_direction(self, seqIdx: int) -> int:
        lastIdx = len(self.sequences[seqIdx])-1
        maxIdx = max(self.sequences[seqIdx][lastIdx], self.sequences[seqIdx][lastIdx-1])
        minIdx = min(self.sequences[seqIdx][lastIdx], self.sequences[seqIdx][lastIdx-1])
        return maxIdx - minIdx
    
    def cell_to_coord(self, cell: int):
        return [int(cell / self.w), cell % self.w]
    
    def coord_to_cell(self, row: int, col: int):
        return (row * self.w) + col
        
    def get_cell_at_dir(self, fromPoint: int, toX: int, toY: int):
        asCoord = self.cell_to_coord(fromPoint)
        asCoord[0] += toY
        asCoord[1] += toX
        if asCoord[0] < 0 or asCoord[0] >= self.h: return -1
        elif asCoord[1] < 0 or asCoord[1] >= self.w: return -1
        else: return self.coord_to_cell(asCoord[0], asCoord[1])
    
    def sequence_num_open_sides(self, seqIdx: int) -> int:
        numOpen = 0
        seq = self.sequences[seqIdx]

        c1 = self.cell_to_coord(seq[len(seq)-2])
        c2 = self.cell_to_coord(seq[len(seq)-1])
        dir = [c2[1]-c1[1], c2[0] - c1[0]]

        if self.values[self.get_cell_at_dir(seq[len(seq)-1], dir[0], dir[1])] == boardSign.EMPTY:
            numOpen += 1
        
        c1 = self.cell_to_coord(seq[1])
        c2 = self.cell_to_coord(seq[0])
        dir = [c2[1]-c1[1], c2[0] - c1[0]]

        if self.values[self.get_cell_at_dir(seq[0], dir[0], dir[1])] == boardSign.EMPTY:
            numOpen += 1
        
        return numOpen
    
    def get_num_open_sequences(self, seqLen: int, numOpen: int, withSign):
        result = 0
        for i in range(0, len(self.sequences)):
            currSign = self.values[self.sequences[i][0]]
            if currSign == withSign and len(self.sequences[i]) == seqLen:
                if self.sequence_num_open_sides(i) == numOpen:
                    result += 1
        return result