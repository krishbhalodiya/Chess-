import random

piece_score = {"K": 0, "Q": 9, "R": 5, "B": 3, "N": 3, "P": 1, }

knight_scores = [[0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0],
                 [0.1, 0.3, 0.5, 0.5, 0.5, 0.5, 0.3, 0.1],
                 [0.2, 0.5, 0.6, 0.65, 0.65, 0.6, 0.5, 0.2],
                 [0.2, 0.55, 0.65, 0.7, 0.7, 0.65, 0.55, 0.2],
                 [0.2, 0.5, 0.65, 0.7, 0.7, 0.65, 0.5, 0.2],
                 [0.2, 0.55, 0.6, 0.65, 0.65, 0.6, 0.55, 0.2],
                 [0.1, 0.3, 0.5, 0.55, 0.55, 0.5, 0.3, 0.1],
                 [0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0]]

bishop_scores = [[0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0],
                 [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
                 [0.2, 0.4, 0.5, 0.6, 0.6, 0.5, 0.4, 0.2],
                 [0.2, 0.5, 0.5, 0.6, 0.6, 0.5, 0.5, 0.2],
                 [0.2, 0.4, 0.6, 0.6, 0.6, 0.6, 0.4, 0.2],
                 [0.2, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.2],
                 [0.2, 0.5, 0.4, 0.4, 0.4, 0.4, 0.5, 0.2],
                 [0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0]]

rook_scores = [[0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
               [0.5, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.5],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.25, 0.25, 0.25, 0.5, 0.5, 0.25, 0.25, 0.25]]

queen_scores = [[0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0],
                [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
                [0.2, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
                [0.3, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
                [0.4, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
                [0.2, 0.5, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
                [0.2, 0.4, 0.5, 0.4, 0.4, 0.4, 0.4, 0.2],
                [0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0]]

pawn_scores = [[0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8],
               [0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7],
               [0.3, 0.3, 0.4, 0.5, 0.5, 0.4, 0.3, 0.3],
               [0.25, 0.25, 0.3, 0.45, 0.45, 0.3, 0.25, 0.25],
               [0.2, 0.2, 0.2, 0.4, 0.4, 0.2, 0.2, 0.2],
               [0.25, 0.15, 0.1, 0.2, 0.2, 0.1, 0.15, 0.25],
               [0.25, 0.3, 0.3, 0.0, 0.0, 0.3, 0.3, 0.25],
               [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2]]

king_middle_scores = [[-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
                      [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
                      [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
                      [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
                      [-2.0, -3.0, -3.0, -4.0, -4.0, -3.0, -3.0, -2.0],
                      [-1.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -1.0],
                      [2.0, 2.0, 0.0, 0.0, 0.0, 0.0, 2.0, 2.0],
                      [2.0, 3.0, 1.0, 0.0, 0.0, 1.0, 3.0, 2.0]]

king_endgame_scores = [[-5.0, -4.0, -3.0, -2.0, -2.0, -3.0, -4.0, -5.0],
                       [-3.0, -2.0, -1.0, 0.0, 0.0, -1.0, -2.0, -3.0],
                       [-3.0, -1.0, 2.0, 3.0, 3.0, 2.0, -1.0, -3.0],
                       [-3.0, -1.0, 3.0, 4.0, 4.0, 3.0, -1.0, -3.0],
                       [-3.0, -1.0, 3.0, 4.0, 4.0, 3.0, -1.0, -3.0],
                       [-3.0, -1.0, 2.0, 3.0, 3.0, 2.0, -1.0, -3.0],
                       [-3.0, -3.0, 0.0, 0.0, 0.0, 0.0, -3.0, -3.0],
                       [-5.0, -3.0, -3.0, -3.0, -3.0, -3.0, -3.0, -5.0]]

piece_position_scores = {"wN": knight_scores,
                         "bN": knight_scores[::-1],
                         "wB": bishop_scores,
                         "bB": bishop_scores[::-1],
                         "wQ": queen_scores,
                         "bQ": queen_scores[::-1],
                         "wR": rook_scores,
                         "bR": rook_scores[::-1],
                         "wP": pawn_scores,
                         "bP": pawn_scores[::-1],
                         "wK": king_middle_scores,
                         "bK": king_middle_scores[::-1]}

CHECKMATE = 1000
STALEMATE = 0
DEPTH = 3
ENDGAME_MATERIAL_THRESHOLD = 13  # Considered endgame if material score is below this threshold

# Track repeated moves
move_counts = {}


def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves) - 1)]


def findBestMove(gs, validMoves):
    global nextMove, boardStates
    nextMove = None
    boardStates = {}  # Initialize board states for threefold repetition check
    random.shuffle(validMoves)
    iterativeDeepening(gs, validMoves, DEPTH)

    # Check for repeated moves
    move_str = str(nextMove)
    if move_str in move_counts:
        move_counts[move_str] += 1
        if move_counts[move_str] >= 3:
            # Find second best move
            validMoves.sort(key=lambda move: scoreMove(gs, move), reverse=True)
            if len(validMoves) > 1:
                nextMove = validMoves[1]
    else:
        move_counts[move_str] = 1

    return nextMove


def iterativeDeepening(gs, validMoves, depth):
    for d in range(1, depth + 1):
        findNegaMaxAlphaBeta(gs, validMoves, d, -CHECKMATE, CHECKMATE, 1 if gs.whiteToMove else -1)


def findNegaMaxAlphaBeta(gs, validMoves, depth, alpha, beta, turnMultiplier):
    global nextMove, boardStates
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)

    # Avoid repeated moves
    currentState = str(gs.board)
    if currentState in boardStates:
        boardStates[currentState] += 1
    else:
        boardStates[currentState] = 1

    if boardStates[currentState] >= 3:
        return 0  # Threefold repetition, return draw score

    # Order moves to optimize pruning
    validMoves.sort(key=lambda move: move.isCapture(), reverse=True)

    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findNegaMaxAlphaBeta(gs, nextMoves, depth - 1, -beta, -alpha, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gs.undoMove()
        if maxScore > alpha:
            alpha = maxScore
        if alpha >= beta:
            break

    # Decrement the board state count after move
    boardStates[currentState] -= 1
    if boardStates[currentState] == 0:
        del boardStates[currentState]

    return maxScore


def scoreBoard(gs):
    """
    Score the board. A positive score is good for white, a negative score is good for black.
    """
    if gs.checkmate:
        if gs.whiteToMove:
            return -CHECKMATE  # black wins
        else:
            return CHECKMATE  # white wins
    elif gs.stalemate:
        return STALEMATE
    score = 0
    piece_counts = {"w": 0, "b": 0}
    for row in range(len(gs.board)):
        for col in range(len(gs.board[row])):
            piece = gs.board[row][col]
            if piece != "--":
                piece_position_score = 0
                if len(piece) == 2 and piece[1] != "K":  # Check if piece is valid and not a king
                    piece_position_score = piece_position_scores[piece][row][col]
                if piece[0] == "w":
                    piece_counts["w"] += piece_score[piece[1]]
                    score += piece_score[piece[1]] + piece_position_score
                if piece[0] == "b":
                    piece_counts["b"] += piece_score[piece[1]]
                    score -= piece_score[piece[1]] + piece_position_score

    # Use endgame evaluation if material is low
    if piece_counts["w"] <= ENDGAME_MATERIAL_THRESHOLD and piece_counts["b"] <= ENDGAME_MATERIAL_THRESHOLD:
        score += evaluateKingEndgame(gs)

    return score


def evaluateKingEndgame(gs):
    """
    In endgame, the king should be more active.
    """
    score = 0
    for row in range(len(gs.board)):
        for col in range(len(gs.board[row])):
            piece = gs.board[row][col]
            if piece == "wK":
                score += king_endgame_scores[row][col]
            elif piece == "bK":
                score -= king_endgame_scores[row][col]
    return score


def scoreMove(gs, move):
    """
    Score a move based on the current game state.
    """
    gs.makeMove(move)
    score = scoreBoard(gs)
    gs.undoMove()
    return score
