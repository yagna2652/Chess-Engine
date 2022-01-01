"""
this class is responsible for storing all the information about the current
state of a chess game, it will aslo be responsible for determning the valid
move at the current state. It will also keep a move log
"""
class Gamestate():
    def __init__(self):
        #board is an 8X8 2D list
        #string "--" represents empty space
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        self.moveFunctions = {'p': self.getpawnmoves, 'R': self.getRookmoves, 'N': self.getKnightmoves, 'Q': self.getQueenmoves, 'K': self.getKingMoves, 'B': self.getBishopmoves}

        self.whiteToMove = True
        self.moveLog = []
        self.whitekinglocation = (7,4)
        self.blackkinglocation = (0,4)
        self.inCheck = False
        self.pins = []
        self.check = []
        """
        Takes moves as parameter and executes it
        """
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)  # log the move so we can undo it later
        self.whiteToMove = not self.whiteToMove  # swap players
        if move.pieceMoved == "wk":
           self.whitekinglocation = (move.endRow, move.endCol)
        elif move.pieceMoved == "bk":
            self.blackkinglocation = (move.endRow, move.endCol)

    def undomove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove
            if move.pieceMoved == "wk":
                self.whitekinglocation = (move.startRow, move.startCol)
            elif move.pieceMoved == "bk":
                self.blackkinglocation = (move.startRow, move.startCol)

        """
        all moves considering checks
        """
    def getValidMoves(self):
        moves = []
        self.inCheck, self.pins, self.check = self.checkforpinsandchecks()
        if self.whiteToMove:
            kingrow = self.whitekinglocation[0]
            kingcol = self.whitekinglocation[1]
        else:
            kingrow = self.blackkinglocation[0]
            kingcol = self.blackkinglocation[1]
        if self.inCheck:
            if len(self.checks) == 1:
                moves = self.getAllpossiblemoves()
                check = self.checks[0]
                checkrow = check[0]
                checkcol = check[1]
                piecechecking = self.board[checkrow][checkcol]
                validSquares = []
                if piecechecking[1] == "N":
                    validSquares = [(checkrow,checkcol)]
                else:
                    for i in range(1,0):
                        validSquares = (kingrow + check[2]*i, kingcol + check[3]*i)
                        validSquares.append(validSquares)
                        if validSquares[0] == checkrow and validSquares[1] == checkcol:
                            break
                for i in range(len(moves)-1,-1,-1):
                    if moves[i].pieceMoved[i] != 'K':
                        if not (moves[i].endrows, moves[i].endcol) in validSquares:
                            moves.remove(moves[i])
            else:
                self.getKingMoves(kingrow, kingcol, moves) 
        else:
            moves = self.getAllpossiblemoves()  

        return moves 
                

    def inCheck(self):
        if self.whiteToMove:
            return self.squareunderattack(self.whitekinglocation[0], self.whitekinglocation[1])
        else:
            return self.squareunderattack(self.blackkinglocation[0], self.blackkinglocation[1])
    def squareunderattack(self,r,c):
        self.whiteToMove = not self.whiteToMove
        oppMoves = self.getAllpossiblemoves()
        self.whiteToMove = not self.whiteToMove
        for move in oppMoves:
            if move.endRow == r and move.endCol == c:
                return True
        return False

    def getAllpossiblemoves(self):
        moves = []
        for r in range(len(self.board)):#no of rows
            for c in range(len(self.board[r])):#no of columns
                turn = self.board[r][c][0]
                if(turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r,c, moves) #calls appropriate move function based on the pieces
        return moves
        
    def getpawnmoves(self,r,c,moves):
        if self.whiteToMove:
            if self.board[r-1][c] == "--": #this is just one square advance
                moves.append(Move((r, c),(r-1,c), self.board))
                if r == 6 and self.board[r-2][c] == "--":
                    moves.append(Move((r,c), (r-2,c), self.board))

            if c-1 >= 0:
                if self.board[r-1][c-1][0] == 'b':
                    moves.append(Move((r, c), (r-1, c-1), self.board))
            if c+1 <= 7: #captures to the right
                if self.board[r-1][c+1][0] == 'b':
                    moves.append(Move((r, c), (r-1, c+1), self.board))
        else:
            if self.board[r+1][c] == "--": #this is just one square advance
                moves.append(Move((r, c),(r+1,c), self.board))
                if r == 1 and self.board[r+2][c] == "--":
                    moves.append(Move((r,c), (r+2,c), self.board))

            if c-1 >= 0:
                if self.board[r+1][c-1][0] == 'w':
                    moves.append(Move((r, c), (r+1, c-1), self.board))
            if c+1 <= 7: #captures to the rightc
                if self.board[r+1][c+1][0] == 'w':
                    moves.append(Move((r, c), (r+1, c+1), self.board))
                
    def getRookmoves(self,r,c,moves):
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))  # up, left, down, right
        enemy_color = "b" if self.whiteToMove else "w"
        for direction in directions:
            for i in range(1, 8):
                end_row = r + direction[0] * i
                end_col = c + direction[1] * i
                if 0 <= end_row <= 7 and 0 <= end_col <= 7:  # check for possible moves only in boundaries of the board
                        end_piece = self.board[end_row][end_col]
                        if end_piece == "--":  # empty space is valid
                            moves.append(Move((r, c), (end_row, end_col), self.board))
                        elif end_piece[0] == enemy_color:  # capture enemy piece
                            moves.append(Move((r, c), (end_row, end_col), self.board))
                            break
                        else:  # friendly piece
                            break
                else:  # off board
                    break
                

    def getKnightmoves(self,r,c,moves):
        knight_moves = ((-2, -1), (-2, 1), (-1, 2), (1, 2), (2, -1), (2, 1), (-1, -2),
                        (1, -2))  # up/left up/right right/up right/down down/left down/right left/up left/down
        ally_color = "w" if self.whiteToMove else "b"
        for move in knight_moves:
            end_row = r + move[0]
            end_col = c + move[1]
            if 0 <= end_row <= 7 and 0 <= end_col <= 7:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] != ally_color:  # so its either enemy piece or empty square
                        moves.append(Move((r, c), (end_row, end_col), self.board))
        
    def getBishopmoves(self,r,c,moves):
        directions = ((-1, -1), (-1, 1), (1, 1), (1, -1))  # diagonals: up/left up/right down/right down/left
        enemy_color = "b" if self.whiteToMove else "w"
        for direction in directions:
            for i in range(1, 8):
                end_row = r + direction[0] * i
                end_col = c + direction[1] * i
                if 0 <= end_row <= 7 and 0 <= end_col <= 7:  # check if the move is on board
                    end_piece = self.board[end_row][end_col]
                    if end_piece == "--":  # empty space is valid
                        moves.append(Move((r, c), (end_row, end_col), self.board))
                    elif end_piece[0] == enemy_color:  # capture enemy piece
                        moves.append(Move((r, c), (end_row, end_col), self.board))
                        break
                    else:  # friendly piece
                        break
                else:  # off board
                    break



    def getQueenmoves(self,r,c,moves):
        self.getBishopmoves(r, c, moves)
        self.getRookmoves(r, c, moves)

    def getKingMoves(self,r,c,moves):
        pass

    


class Move():
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}



    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow*1000 + self.startCol*100 + self.endRow*10 + self.endCol

    """
    overriding and equals method
    """
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        # you can add to make this like real chess notation
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
