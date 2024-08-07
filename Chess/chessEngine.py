class GameState:
    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.moveFunctions = {'P': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves,
                              'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves}
        self.whiteToMove = True
        self.moveLog = []
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.checkmate = False
        self.stalemate = False

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        if move.isPawnPromotion and move.promotion_choice:
            self.board[move.endRow][move.endCol] = move.promotion_choice
        else:
            self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)

        # Update the king's location
        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == 'bK':
            self.blackKingLocation = (move.endRow, move.endCol)

        self.whiteToMove = not self.whiteToMove

    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured

            # Restore the king's location
            if move.pieceMoved == 'wK':
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == 'bK':
                self.blackKingLocation = (move.startRow, move.startCol)

            self.whiteToMove = not self.whiteToMove
        self.checkmate = False
        self.stalemate = False

    def getValidMoves(self):
        moves = self.getAllPossibleMoves()
        for i in range(len(moves) - 1, -1, -1):
            self.makeMove(moves[i])
            self.whiteToMove = not self.whiteToMove
            if self.inCheck():
                moves.remove(moves[i])
            self.whiteToMove = not self.whiteToMove
            self.undoMove()

        if len(moves) == 0:
            if self.inCheck():
                self.checkmate = True
                self.stalemate = False
            else:
                self.stalemate = True
                self.checkmate = False
        else:
            self.checkmate = False
            self.stalemate = False

        return moves

    def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])

    def squareUnderAttack(self, r, c):
        self.whiteToMove = not self.whiteToMove
        oppMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove
        for move in oppMoves:
            if move.endRow == r and move.endCol == c:
                return True
        return False

    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves)
        return moves

    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove:
            if r - 1 >= 0 and self.board[r - 1][c] == "--":
                self.addPawnMove(r, c, r - 1, c, moves)
                if r == 6 and self.board[r - 2][c] == "--":
                    self.addPawnMove(r, c, r - 2, c, moves)
            if r - 1 >= 0 and c - 1 >= 0 and self.board[r - 1][c - 1][0] == 'b':
                self.addPawnMove(r, c, r - 1, c - 1, moves)
            if r - 1 >= 0 and c + 1 <= 7 and self.board[r - 1][c + 1][0] == 'b':
                self.addPawnMove(r, c, r - 1, c + 1, moves)
        else:
            if r + 1 <= 7 and self.board[r + 1][c] == "--":
                self.addPawnMove(r, c, r + 1, c, moves)
                if r == 1 and self.board[r + 2][c] == "--":
                    self.addPawnMove(r, c, r + 2, c, moves)
            if r + 1 <= 7 and c - 1 >= 0 and self.board[r + 1][c - 1][0] == 'w':
                self.addPawnMove(r, c, r + 1, c - 1, moves)
            if r + 1 <= 7 and c + 1 <= 7 and self.board[r + 1][c + 1][0] == 'w':
                self.addPawnMove(r, c, r + 1, c + 1, moves)

    def addPawnMove(self, startRow, startCol, endRow, endCol, moves):
        if (startRow == 1 and self.board[startRow][startCol] == 'bP') or (
                startRow == 6 and self.board[startRow][startCol] == 'wP'):
            isPawnPromotion = True
        else:
            isPawnPromotion = False
        moves.append(Move((startRow, startCol), (endRow, endCol), self.board, isPawnPromotion, promotion_choice='Q'))

    def getRookMoves(self, r, c, moves):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        self.getDirectionalMoves(r, c, directions, moves)

    def getBishopMoves(self, r, c, moves):
        directions = [(-1, -1), (1, 1), (1, -1), (-1, 1)]
        self.getDirectionalMoves(r, c, directions, moves)

    def getQueenMoves(self, r, c, moves):
        directions = [(-1, -1), (1, 1), (1, -1), (-1, 1), (-1, 0), (1, 0), (0, -1), (0, 1)]
        self.getDirectionalMoves(r, c, directions, moves)

    def getKingMoves(self, r, c, moves):
        king_moves = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for move in king_moves:
            end_row = r + move[0]
            end_col = c + move[1]
            if 0 <= end_row < len(self.board) and 0 <= end_col < len(self.board[0]):
                end_piece = self.board[end_row][end_col]
                if end_piece == "--" or end_piece[0] == ('b' if self.whiteToMove else 'w'):
                    moves.append(Move((r, c), (end_row, end_col), self.board))

    def getKnightMoves(self, r, c, moves):
        knight_moves = [(-2, -1), (-1, -2), (1, -2), (2, -1), (2, 1), (1, 2), (-1, 2), (-2, 1)]
        enemy_color = 'b' if self.whiteToMove else 'w'
        for move in knight_moves:
            end_row = r + move[0]
            end_col = c + move[1]
            if 0 <= end_row < len(self.board) and 0 <= end_col < len(self.board[0]):
                end_piece = self.board[end_row][end_col]
                if end_piece == "--" or end_piece[0] == enemy_color:
                    moves.append(Move((r, c), (end_row, end_col), self.board))

    def getDirectionalMoves(self, r, c, directions, moves):
        enemy_color = 'b' if self.whiteToMove else 'w'
        for d in directions:
            for i in range(1, len(self.board)):
                end_row = r + d[0] * i
                end_col = c + d[1] * i
                if 0 <= end_row < len(self.board) and 0 <= end_col < len(self.board[0]):
                    end_piece = self.board[end_row][end_col]
                    if end_piece == "--":
                        moves.append(Move((r, c), (end_row, end_col), self.board))
                    elif end_piece[0] == enemy_color:
                        moves.append(Move((r, c), (end_row, end_col), self.board))
                        break
                    else:
                        break

    def checkForCheckmate(self):
        if self.inCheck() and not self.getValidMoves():
            return True
        return False

    def checkForStalemate(self):
        if not self.inCheck() and not self.getValidMoves():
            return True
        return False



    def getBoardState(self):
        return str(self.board) + str(self.whiteToMove)

    def checkForFiftyMoveRule(self):
        if len(self.moveLog) >= 50 and all(
                not move.isPawnMove() and not move.isCapture() for move in self.moveLog[-50:]):
            return True
        return False

    def checkForInsufficientMaterial(self):
        pieces = [piece for row in self.board for piece in row if piece != '--']
        if pieces == ['wK', 'bK']:
            return True
        return False

    def checkDrawConditions(self):
        if self.checkForFiftyMoveRule():
            return "Fifty-move rule"
        if self.checkForInsufficientMaterial():
            return "Insufficient material"
        return None


class Move:
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board, isCastleMove=False, promotion_choice=None):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.isPawnPromotion = (self.pieceMoved == 'wP' and self.endRow == 0) or (self.pieceMoved == 'bP' and self.endRow == 7)
        self.promotion_choice = promotion_choice
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
        self.isCastleMove = isCastleMove

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def isPawnMove(self):
        return self.pieceMoved[1] == 'P'

    def isCapture(self):
        return self.pieceCaptured != '--'

    def isCheck(self, gameState):
        # Temporarily make the move
        self.makeMove(gameState)
        inCheck = gameState.inCheck()
        # Undo the move
        self.undoMove(gameState)
        return inCheck

    def makeMove(self, gameState):
        gameState.board[self.startRow][self.startCol] = "--"
        gameState.board[self.endRow][self.endCol] = self.pieceMoved
        if self.pieceMoved == 'wK':
            gameState.whiteKingLocation = (self.endRow, self.endCol)
        elif self.pieceMoved == 'bK':
            gameState.blackKingLocation = (self.endRow, self.endCol)
        gameState.whiteToMove = not gameState.whiteToMove

    def undoMove(self, gameState):
        gameState.board[self.startRow][self.startCol] = self.pieceMoved
        gameState.board[self.endRow][self.endCol] = self.pieceCaptured
        if self.pieceMoved == 'wK':
            gameState.whiteKingLocation = (self.startRow, self.startCol)
        elif self.pieceMoved == 'bK':
            gameState.blackKingLocation = (self.startRow, self.startCol)
        gameState.whiteToMove = not gameState.whiteToMove

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
