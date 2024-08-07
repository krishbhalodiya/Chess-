from Chess import chessEngine
import random

pieceScore = {"K": 0, "Q": 9, "R": 5, "B": 3, "N": 3, "P": 1}
checkMate = 999
staleMate = 0
DEPTH = 3
counter = 0


def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves) - 1)]


def findBestMoveNegaMax(gs, validMoves):
    global nextMove
    nextMove = None
    random.shuffle(validMoves)
    findNegaMaxAlphaBeta(gs, validMoves, DEPTH, -checkMate, checkMate, 1 if gs.whiteToMove else -1)
    print(counter)
    return nextMove


def findNegaMaxAlphaBeta(gs, validMoves, depth, alpha, beta, turnMultiplier):
    global nextMove
    global counter
    counter += 1
    if depth == 0:
        return turnMultiplier * scoreMaterial(gs)

    # move ordering - implement later
    maxScore = -checkMate
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findNegaMaxAlphaBeta(gs, nextMoves, depth-1, -beta, -alpha, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gs.undoMove()
        if maxScore > alpha:
            alpha = maxScore
        if alpha >= beta:
            break
    return maxScore


def scoreMaterial(gs):
    if gs.checkmate:
        if gs.whiteToMove:
            return -checkMate
        else:
            return checkMate
    elif gs.stalemate:
        return staleMate

    score = 0
    for row in gs.board:
        for square in row:
            if square[0] == 'w':
                score += pieceScore[square[1]]
            elif square[0] == 'b':
                score -= pieceScore[square[1]]
    return score
